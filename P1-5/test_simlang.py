# test_simlang.py
# Kevin Briceño 15-11661
# Pruebas unitarias para simlang.py
import pytest
from simlang import Simulator, SimulatorError, LANG_LOCAL

def test_define_and_execute_local():
    s = Simulator()
    s.define_program("P1", LANG_LOCAL)
    ok, plan = s.executable_plan_for_program("P1")
    assert ok is True
    assert plan == []  # ejecución nativa

def test_simple_interpreter_impl_local():
    s = Simulator()
    s.define_program("p", "L1")
    s.define_interpreter(LANG_LOCAL, "L1")  # intérprete de L1 implementado en LOCAL
    ok, plan = s.executable_plan_for_program("p")
    assert ok
    assert plan == [{"action":"interpret","interpreted":"L1","implemented_in":LANG_LOCAL}]

def test_interpreter_chain_impl_in_other_language():
    s = Simulator()
    s.define_program("p", "Lx")
    # intérprete de Lx implementado en Ly, y Ly interpretado por LOCAL
    s.define_interpreter("Ly", "Lx")   # Ly implementa intérprete para Lx
    s.define_interpreter(LANG_LOCAL, "Ly")  # LOCAL interpreta Ly
    ok, plan = s.executable_plan_for_program("p")
    assert ok
    # plan debe ejecutar intérprete de Ly (local) luego interpretar Lx via Ly
    # primera: interpret Ly using LOCAL, then interpret Lx using impl Ly
    assert plan[0]["action"] == "interpret" and plan[0]["interpreted"] == "Ly"
    assert plan[1]["action"] == "interpret" and plan[1]["interpreted"] == "Lx"

def test_translator_then_interpreter():
    s = Simulator()
    s.define_program("p", "A")
    # traductor A -> B implementado en LOCAL
    s.define_translator(LANG_LOCAL, "A", "B")
    # intérprete de B implementado en LOCAL
    s.define_interpreter(LANG_LOCAL, "B")
    ok, plan = s.executable_plan_for_program("p")
    assert ok
    # plan: translate A->B (impl LOCAL) then interpret B (impl LOCAL)
    assert plan[0]["action"] == "translate" and plan[0]["from"] == "A" and plan[0]["to"] == "B"
    assert plan[1]["action"] == "interpret" and plan[1]["interpreted"] == "B"

def test_unexecutable_program_due_to_impl_missing():
    s = Simulator()
    s.define_program("p", "A")
    # traductor A -> B implemented in X (not executable)
    s.define_translator("X", "A", "B")
    # no way to execute X or B
    ok, plan = s.executable_plan_for_program("p")
    assert not ok
    assert plan is None

def test_cycle_detection_no_local_path():
    s = Simulator()
    s.define_program("p", "A")
    # translators A->B, B->A implemented in some non-local L1
    s.define_translator("L1", "A", "B")
    s.define_translator("L1", "B", "A")
    # L1 not executable -> cycle without LOCAL
    ok, plan = s.executable_plan_for_program("p")
    assert not ok

def test_missing_program_error():
    s = Simulator()
    with pytest.raises(SimulatorError):
        s.executable_plan_for_program("noexist")

def test_duplicate_definitions_error():
    s = Simulator()
    s.define_program("p", "A")
    with pytest.raises(SimulatorError):
        s.define_program("p", "A")
    s.define_interpreter("L0", "A")
    with pytest.raises(SimulatorError):
        s.define_interpreter("L0", "A")  # duplicado
    s.define_translator("L0", "A", "B")
    with pytest.raises(SimulatorError):
        s.define_translator("L0", "A", "B")  # duplicado

def test_cli_tokenize_and_strip():
    s = Simulator()
    toks = s._tokenize('DEFINIR PROGRAMA "p" "L1"')
    assert toks == ["DEFINIR", "PROGRAMA", '"p"', '"L1"']
    assert s._strip_quotes('"ABC"') == "ABC"
