# prueba.py (variante: un Simulator por ejemplo)
# Kevin Briceño 15-11661

from simlang import Simulator, LANG_LOCAL, SimulatorError

SAMPLE_PROGRAMS = {
    "P1": {"language": "PYTHON", "code": 'print("Hola desde PYTHON (P1)")\n'},
    "P2": {"language": "RUBY",   "code": "puts 'Hola desde RUBY (P2)'\n"}
}

def pretty_print_plan(plan):
    if not plan:
        print("  (ejecución nativa en LOCAL)")
        return
    for i, step in enumerate(plan, 1):
        if step.get("action") == "interpret":
            print(f"  {i}. interpretar {step['interpreted']} usando intérprete implementado en {step['implemented_in']}")
        elif step.get("action") == "translate":
            print(f"  {i}. traducir {step['from']} -> {step['to']} usando traductor implementado en {step['implemented_in']}")
        else:
            print(f"  {i}. paso desconocido: {step}")

def example1():
    sim = Simulator()
    sim.define_program("P1", SAMPLE_PROGRAMS["P1"]["language"])
    sim.define_interpreter(LANG_LOCAL, "PYTHON")
    ok, plan = sim.executable_plan_for_program("P1")
    print("=== EJEMPLO 1 ===")
    print("Programa: P1")
    print("Lenguaje:", SAMPLE_PROGRAMS["P1"]["language"])
    print("¿Ejecutable?", ok)
    print("Plan:")
    pretty_print_plan(plan)
    if ok:
        print("\nContenido (ejemplo) del programa P1:")
        print(SAMPLE_PROGRAMS["P1"]["code"])
    print()

def example2():
    sim = Simulator()   # <-- instancia nueva, sin definiciones previas
    sim.define_program("P2", SAMPLE_PROGRAMS["P2"]["language"])
    sim.define_interpreter("PYTHON", "RUBY")    # intérprete de RUBY implementado en PYTHON
    sim.define_interpreter(LANG_LOCAL, "PYTHON")# intérprete de PYTHON implementado en LOCAL
    ok, plan = sim.executable_plan_for_program("P2")
    print("=== EJEMPLO 2 ===")
    print("Programa: P2")
    print("Lenguaje:", SAMPLE_PROGRAMS["P2"]["language"])
    print("¿Ejecutable?", ok)
    print("Plan:")
    pretty_print_plan(plan)
    if ok:
        print("\nContenido (ejemplo) del programa P2:")
        print(SAMPLE_PROGRAMS["P2"]["code"])
    print()

if __name__ == "__main__":
    example1()
    example2()
