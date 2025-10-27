# simlang.py
# Kevin Briceño 15-11661
# Simulador de programas / intérpretes / traductores.

"""
Permite definir:
  PROGRAMA "nombre" "lenguaje"
  INTERPRETE "lenguaje_impl" "lenguaje_objetivo"
  TRADUCTOR "lenguaje_impl" "lenguaje_origen" "lenguaje_destino"

La lengua especial "LOCAL" corresponde al lenguaje ejecutable por la máquina local.
Acciones del usuario:
  DEFINIR <TIPO> [ARGUMENTOS]
  EJECUTABLE "nombre"
  SALIR

La función principal para decidir si un programa es ejecutable es
buscar una secuencia de pasos (usar traductores/interpretes) que permita
llegar desde el lenguaje del programa hasta LOCAL.
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass

LANG_LOCAL = "LOCAL"

# --- Estructuras de datos ---
@dataclass(frozen=True)
class Program:
    name: str
    language: str

@dataclass(frozen=True)
class Interpreter:
    impl_lang: str   # lenguaje en el que está implementado el intérprete
    target_lang: str # lenguaje que interpreta

@dataclass(frozen=True)
class Translator:
    impl_lang: str   # lenguaje en el que está implementado el traductor
    from_lang: str   # lenguaje origen
    to_lang: str     # lenguaje destino

# Paso en un plan de ejecución
# tipo: "interpret" | "translate"
# contenido variable según tipo
PlanStep = Dict[str, str]

class SimulatorError(Exception):
    """Errores del simulador (definición inválida, búsqueda fallida, etc.)."""
    pass

class Simulator:
    """Clase principal que mantiene definiciones y decide ejecutabilidad."""

    def __init__(self):
        # programas por nombre
        self.programs: Dict[str, Program] = {}
        # intérpretes indexados por lenguaje interpretado -> list of Interpreter
        self.interpreters: Dict[str, List[Interpreter]] = {}
        # lista de traductores
        self.translators: List[Translator] = []

    # --- API de definiciones ---
    def define_program(self, name: str, language: str) -> None:
        if name in self.programs:
            raise SimulatorError(f"Programa '{name}' ya definido")
        self.programs[name] = Program(name, language)

    def define_interpreter(self, impl_lang: str, target_lang: str) -> None:
        it = Interpreter(impl_lang=impl_lang, target_lang=target_lang)
        self.interpreters.setdefault(target_lang, [])
        if it in self.interpreters[target_lang]:
            raise SimulatorError("Intérprete duplicado")
        self.interpreters[target_lang].append(it)

    def define_translator(self, impl_lang: str, from_lang: str, to_lang: str) -> None:
        tr = Translator(impl_lang=impl_lang, from_lang=from_lang, to_lang=to_lang)
        if tr in self.translators:
            raise SimulatorError("Traductor duplicado")
        self.translators.append(tr)

    # --- consulta / utilidades ---
    def list_programs(self) -> List[Program]:
        return list(self.programs.values())

    def list_interpreters(self) -> List[Interpreter]:
        out = []
        for lst in self.interpreters.values():
            out.extend(lst)
        return out

    def list_translators(self) -> List[Translator]:
        return list(self.translators)

    # --- búsqueda de plan de ejecución ---
    def executable_plan_for_program(self, name: str) -> Tuple[bool, Optional[List[PlanStep]]]:
        """
        Para el programa 'name', devuelve (True, plan) si es ejecutable;
        plan es una lista de pasos ordenados para ejecutar (o traducir/interpretar).
        Si no es ejecutable devuelve (False, None).
        """
        if name not in self.programs:
            raise SimulatorError(f"Programa '{name}' no definido")
        program = self.programs[name]
        memo = {}  # memo[lang] = (bool, plan)
        ok, plan = self._can_execute_language(program.language, memo, path=set())
        return ok, plan

    def _can_execute_language(self, lang: str, memo: Dict[str, Tuple[bool, Optional[List[PlanStep]]]],
                              path: Set[str]) -> Tuple[bool, Optional[List[PlanStep]]]:
        """
        Decide si un código en 'lang' puede ser ejecutado por la máquina local.
        Devuelve (True, plan) si es posible, plan es secuencia de pasos.
        path se usa para detectar ciclos (idiomático DFS).
        """
        # Caso trivial
        if lang == LANG_LOCAL:
            return True, []

        if lang in memo:
            return memo[lang]

        if lang in path:
            # ciclo detectado -> no seguir por esta rama
            memo[lang] = (False, None)
            return False, None

        # marcar en camino
        path.add(lang)

        # 1) intentamos usar intérpretes que interpreten 'lang'
        interpreters_for_lang = self.interpreters.get(lang, [])
        for it in interpreters_for_lang:
            impl = it.impl_lang
            # necesitamos ejecutar el intérprete (impl)
            ok_impl, plan_impl = self._can_execute_language(impl, memo, set(path))
            if ok_impl:
                # ejecutar plan_impl para el impl_lang, luego ejecutar el intérprete
                plan = []
                if plan_impl:
                    plan.extend(plan_impl)
                plan.append({"action": "interpret", "interpreted": lang, "implemented_in": impl})
                memo[lang] = (True, plan)
                path.remove(lang)
                return True, plan

        # 2) intentamos usar traductores que partan de 'lang'
        for tr in self.translators:
            if tr.from_lang != lang:
                continue
            impl = tr.impl_lang
            to_lang = tr.to_lang
            # primero necesitamos poder ejecutar el traductor (impl)
            ok_impl, plan_impl = self._can_execute_language(impl, memo, set(path))
            if not ok_impl:
                continue
            # si podemos ejecutar el traductor, al usarlo convertimos a 'to_lang'
            # ahora necesitamos poder ejecutar to_lang
            ok_to, plan_to = self._can_execute_language(to_lang, memo, set(path))
            if ok_to:
                plan = []
                if plan_impl:
                    plan.extend(plan_impl)
                plan.append({"action": "translate", "from": lang, "to": to_lang, "implemented_in": impl})
                if plan_to:
                    plan.extend(plan_to)
                memo[lang] = (True, plan)
                path.remove(lang)
                return True, plan

        # no encontramos forma de ejecutar lang
        memo[lang] = (False, None)
        path.remove(lang)
        return False, None

    # --- interfaz conversacional mínima ---
    def run_cli(self):
        """Bucle interactivo de definición y consulta."""
        print("Simulador de Programas / Intérpretes / Traductores")
        print("Comandos:")
        print('  DEFINIR PROGRAMA "nombre" "lenguaje"')
        print('  DEFINIR INTERPRETE "leng_impl" "lenguaje"')
        print('  DEFINIR TRADUCTOR "leng_impl" "origen" "destino"')
        print('  EJECUTABLE "nombre"')
        print('  LISTAR')
        print('  SALIR')
        while True:
            try:
                line = input(">>> ").strip()
            except EOFError:
                break
            if not line:
                continue
            toks = self._tokenize(line)
            if not toks:
                print("Entrada no reconocida.")
                continue
            cmd = toks[0].upper()
            try:
                if cmd == "DEFINIR":
                    self._handle_definir(toks[1:])
                elif cmd == "EJECUTABLE":
                    if len(toks) != 2:
                        print("Uso: EJECUTABLE \"nombre\"")
                        continue
                    name = self._strip_quotes(toks[1])
                    ok, plan = self.executable_plan_for_program(name)
                    if ok:
                        print(f"Programa '{name}' es EJECUTABLE. Plan:")
                        for i, step in enumerate(plan, 1):
                            if step["action"] == "interpret":
                                print(f"  {i}. interpretar {step['interpreted']} usando intérprete implementado en {step['implemented_in']}")
                            else:
                                print(f"  {i}. traducir {step['from']} -> {step['to']} usando traductor implementado en {step['implemented_in']}")
                        if not plan:
                            print("  (ejecución nativa en LOCAL)")
                    else:
                        print(f"Programa '{name}' NO es ejecutable con las definiciones actuales.")
                elif cmd == "LISTAR":
                    self._print_all()
                elif cmd == "SALIR":
                    print("Bye")
                    break
                else:
                    print("Comando desconocido. Use DEFINIR / EJECUTABLE / LISTAR / SALIR")
            except SimulatorError as e:
                print("ERROR:", e)
            except Exception as e:
                print("ERROR inesperado:", e)

    # --- helpers del CLI ---
    def _handle_definir(self, args: List[str]):
        if not args:
            raise SimulatorError("DEFINIR requiere subcomando (PROGRAMA/INTERPRETE/TRADUCTOR)")
        kind = args[0].upper()
        if kind == "PROGRAMA":
            if len(args) != 3:
                raise SimulatorError('Uso: DEFINIR PROGRAMA "nombre" "lenguaje"')
            name = self._strip_quotes(args[1])
            lang = self._strip_quotes(args[2])
            self.define_program(name, lang)
            print(f"Definido PROGRAMA '{name}' en lenguaje '{lang}'")
        elif kind == "INTERPRETE":
            if len(args) != 3:
                raise SimulatorError('Uso: DEFINIR INTERPRETE "leng_impl" "lenguaje"')
            impl = self._strip_quotes(args[1])
            target = self._strip_quotes(args[2])
            self.define_interpreter(impl, target)
            print(f"Definido INTERPRETE para '{target}' implementado en '{impl}'")
        elif kind == "TRADUCTOR":
            if len(args) != 4:
                raise SimulatorError('Uso: DEFINIR TRADUCTOR "leng_impl" "origen" "destino"')
            impl = self._strip_quotes(args[1])
            origen = self._strip_quotes(args[2])
            destino = self._strip_quotes(args[3])
            self.define_translator(impl, origen, destino)
            print(f"Definido TRADUCTOR {origen} -> {destino} implementado en {impl}")
        else:
            raise SimulatorError("Subcomando DEFINIR desconocido. Use PROGRAMA / INTERPRETE / TRADUCTOR")

    def _tokenize(self, line: str) -> List[str]:
        """
        Tokeniza una línea simple suponiendo que los argumentos entre comillas
        deben considerarse como un único token.
        Ejemplo: DEFINIR PROGRAMA "p" "L1" -> ["DEFINIR","PROGRAMA","\"p\"","\"L1\""]
        """
        tokens = []
        i = 0
        n = len(line)
        while i < n:
            if line[i].isspace():
                i += 1
                continue
            if line[i] == '"':
                j = i + 1
                while j < n and line[j] != '"':
                    j += 1
                if j >= n:
                    raise SimulatorError("Comillas sin cerrar")
                tokens.append(line[i:j+1])
                i = j + 1
            else:
                j = i
                while j < n and not line[j].isspace():
                    j += 1
                tokens.append(line[i:j])
                i = j
        return tokens

    def _strip_quotes(self, token: str) -> str:
        if token.startswith('"') and token.endswith('"') and len(token) >= 2:
            return token[1:-1]
        return token

    def _print_all(self):
        print("Programas definidos:")
        for p in self.programs.values():
            print(f"  {p.name} : {p.language}")
        print("Intérpretes definidos:")
        for lst in self.interpreters.values():
            for it in lst:
                print(f"  interpreta {it.target_lang} implementado en {it.impl_lang}")
        print("Traductores definidos:")
        for tr in self.translators:
            print(f"  traduce {tr.from_lang} -> {tr.to_lang} implementado en {tr.impl_lang}")
