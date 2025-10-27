#### Información del Autor
-   **Nombre**: Kevin Briceño
-   **Carnet**: 15-11661
-   **Email**: 15-11661@usb.ve

# Ejercicio 5: Simulación de Programas, Intérpretes y Traductores en Python

Este documento describe la implementación de un programa en Python que simula programas, intérpretes y traductores, como en los diagramas de T. El programa debe permitir definir:

**PROGRAMA** <"nombre"><"lenguaje">
**INTERPRETE** <"lenguaje_base"><"lenguaje">
**TRADUCTOR** <"lenguaje_base"><"lenguaje_origen"><"lenguaje_destino">

Debe manejar el lenguaje especial LOCAL, correspondiente al lenguaje ejecutable por la máquina local.

Debe permitir acciones del usuario:

DEFINIR <"tipo">[<"argumentos">]
EJECUTABLE <"nombre">
SALIR

### Contenido principal:

-   simlang.py — implementación del Simulator (API + CLI).
-   test_simlang.py — pruebas unitarias con pytest.
-   prueba.py — script demostrativo.
-   Ejercicio5.md — este documento.

### Descripción del Programa
Este es un simulador en Python para razonar sobre programas, intérpretes y traductores (modelo de los diagramas de T). El simulador construye, cuando existe, un plan de ejecución (secuencia de pasos interpret / translate) que lleva el lenguaje del programa hasta LOCAL.

El programa está estructurado para manejar definiciones de programas, intérpretes y traductores, permitiendo al usuario definir y ejecutar programas en diferentes lenguajes. Se incluyen validaciones de error para asegurar que las definiciones y ejecuciones sean coherentes con las reglas establecidas.

### Explicación del Código

#### Estructuras principales

-   Program(name, language) — dato inmutable para programas.
-   Interpreter(impl_lang, target_lang) — intérprete que ejecuta target_lang implementado en impl_lang.
-   Translator(impl_lang, from_lang, to_lang) — traductor from_lang -> to_lang implementado en impl_lang.
-   LANG_LOCAL = "LOCAL" — literal que indica ejecución nativa.

#### Almacenamiento interno

-   self.programs: Dict[name, Program]
-   self.interpreters: Dict[target_lang, List[Interpreter]] — indexado por lenguaje interpretado para búsqueda eficiente.
-   self.translators: List[Translator] — lista simple (suficiente en el ejercicio).

Núcleo: búsqueda de plan ejecutable
-   Funcion publica: executable_plan_for_program(name) -> (bool, Optional[List[PlanStep]])
-   Delegación: _can_execute_language(lang, memo, path) -> (bool, Optional[plan])

Algoritmo principal en _can_execute_language:
1.  Caso base: si lang == LOCAL, retornar (True, []).
2.  Memoización: si lang en memo, retornar memo[lang].
3.  Detección de ciclos: si lang en path, retornar (False, None) si hay ciclo.
4.  Prioridad de busqueda:
    a.  Buscar intérpretes para lang. recursivamente intentar ejecutar impl_lang 
        - si éxito, retornar (True, [InterpretStep] + plan_impl).
    b.  Para cada traductor que produce lang, intentar traducir desde from_lang 
        - si éxito, retornar plan_impl + [translate step] + plan_to.
5.  Si no se encuentra plan, memoizar (False, None).

Formato del plan (lista de pasos)
-   Interpretación{"action": "interpret", "interpreted": <lang>, "implemented_in": <impl_lang>}
-   Traducción{"action": "translate", "from": <lang>, "to": <to_lang>, "implemented_in": <impl_lang>}
Nota de diseño: la búsqueda prioriza intérpretes frente a traductores. Esta elección debe quedar explícita en la documentación porque cambia el plan resultante en escenarios con alternativas.

### Complejidad y aspectos técnicos

Complejidad: cada lenguaje se explora a lo sumo una vez gracias a la memoización; el coste principal viene de iterar intérpretes/traductores registrados. En práctica para cantidades moderadas la solución es eficiente.

Ciclos: detectados vía path (DFS). Cuando se detecta un ciclo, esa rama devuelve (False, None) y se memoiza.

Duplicados: las funciones de definición (define_*) detectan duplicados y lanzan SimulatorError — esto mantiene consistencia y evita ambigüedades.


### Ejemplos, Validaciones de Error y Pruebas Unitarias.
El programa incluye ejemplos de uso, validaciones de error para entradas incorrectas y pruebas unitarias con una cobertura mayor al 80%. Las pruebas aseguran que todas las funcionalidades del programa se comporten como se espera bajo diferentes escenarios.


### Ejecución del Programa

#### Preparar entorno:
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

#### Instalar dependencias:
pip install pytest pytest-cov

#### Ejecutar pruebas:
pytest -q
pytest --cov=simlang --cov-report=term-missing

#### Ejecutar script demostrativo:
python prueba.py


#### Salida esperada:
=== EJEMPLO 1 ===
Programa: P1
Lenguaje: PYTHON
¿Ejecutable? True
Plan:
  1. interpretar PYTHON usando intérprete implementado en LOCAL

Contenido (ejemplo) del programa P1:
print("Hola desde PYTHON (P1)")


=== EJEMPLO 2 ===
Programa: P2
Lenguaje: RUBY
¿Ejecutable? True
Plan:
  1. interpretar PYTHON usando intérprete implementado en LOCAL
  2. interpretar RUBY usando intérprete implementado en PYTHON

#### Usar la CLI de simlang.py (interactivo):
python -c "from simlang import Simulator; Simulator().run_cli()"

#### Ejemplo de sesión:
>>> DEFINIR PROGRAMA "P1" "PYTHON"
Definido PROGRAMA 'P1' en lenguaje 'PYTHON'
>>> DEFINIR INTERPRETE "LOCAL" "PYTHON"
Definido INTERPRETE para 'PYTHON' implementado en 'LOCAL'
>>> EJECUTABLE "P1"
Programa 'P1' es EJECUTABLE. Plan:
  1. interpretar PYTHON usando intérprete implementado en LOCAL
>>> SALIR
Bye

#### Cobertura de pruebas y qué valida test_simlang.py
Las pruebas cubren:
-   Ejecución nativa (lang == LOCAL).
-   Intérpretes directos y cadenas de intérpretes.
-   Traducciones directas y cadenas de traducciones.
-   Combinaciones traductor → intérprete.
-   Fallos cuando la implementación del intérprete/traductor no es ejecutable.
-   Detección de ciclos entre traductores.
-   Errores por definiciones duplicadas.
-   Tokenización y utilidades del CLI.