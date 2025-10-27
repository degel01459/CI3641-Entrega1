# test_buddy.py
# Kevin Briceño 15-11661
# Pruebas unitarias para buddy.py usando pytest.

"""
Cubre casos de inicialización, reserva, liberación, merge, errores y CLI.
"""

import pytest
import builtins
from buddy import BuddyAllocator, BuddyError, run_cli

def test_init_invalid():
    # total <= 0 o no potencia de dos
    with pytest.raises(BuddyError):
        BuddyAllocator(0)
    with pytest.raises(BuddyError):
        BuddyAllocator(3)

def test_find_suitable_order_and_errors():
    b = BuddyAllocator(16)
    assert b._find_suitable_order(1) == 0
    assert b._find_suitable_order(2) == 1
    assert b._find_suitable_order(3) == 2
    assert b._find_suitable_order(16) == 4
    with pytest.raises(BuddyError):
        b._find_suitable_order(0)

def test_reserve_and_basic_split_free():
    b = BuddyAllocator(8)
    s = b.reserve(3, "X")  # necesita order 2 (size 4)
    assert s[1] == 2 and "X" in b.allocated
    s2 = b.reserve(1, "Y")
    assert s2[1] == 0 and "Y" in b.allocated
    # liberar y luego reservar todo
    b.free("X")
    b.free("Y")
    big = b.reserve(8, "ALL")
    assert big == (0, 3)
    b.free("ALL")

def test_duplicate_name_and_invalid_reserve_and_free_unknown():
    b = BuddyAllocator(4)
    b.reserve(1, "A")
    with pytest.raises(BuddyError):
        b.reserve(1, "A")  # mismo nombre
    with pytest.raises(BuddyError):
        b.reserve(-1, "neg")
    with pytest.raises(BuddyError):
        b.free("NO_EXISTE")

def test_coalescing_multiple_levels():
    b = BuddyAllocator(16)
    # reservar 4 bloques (quarters) y luego liberar para que combinen
    ids = ["P0", "P1", "P2", "P3"]
    for i in range(4):
        b.reserve(4, ids[i])
    for nid in ids:
        b.free(nid)
    # al final debería existir un bloque libre al inicio de order max
    assert 0 in b.free_lists[b.max_order]

def test_show_and_allocations_listing():
    b = BuddyAllocator(8)
    b.reserve(1, "uno")
    out = b.show()
    assert "Allocations:" in out and "uno" in out and "Free lists" in out

def test_cli_basic_flow(monkeypatch, capsys):
    # simulamos entrada del usuario para la CLI
    inputs = iter(["MOSTRAR", "RESERVAR 1 foo", "RESERVAR 2 bar", "LIBERAR foo", "MOSTRAR", "SALIR"])
    def fake_input(prompt=""):
        try:
            return next(inputs)
        except StopIteration:
            raise EOFError
    monkeypatch.setattr(builtins, "input", fake_input)
    # ejecutar CLI con 8 bloques
    run_cli(8)
    captured = capsys.readouterr()
    assert "Buddy allocator iniciado" in captured.out
    assert "Reservado 'foo'" in captured.out
    assert "Liberado 'foo'" in captured.out

# escenario más complejo: splits y merges en secuencia
def test_split_merge_sequence():
    b = BuddyAllocator(8)
    b.reserve(2, "A")
    b.reserve(2, "B")
    b.free("A")
    b.reserve(1, "C")
    # verificar consistencia de asignaciones
    assert "B" in b.allocated and "C" in b.allocated

# asegurar que reservar todo y fallar cuando no hay espacio
def test_reserve_full_and_fail():
    b = BuddyAllocator(8)
    b.reserve(8, "all")
    with pytest.raises(BuddyError):
        b.reserve(1, "x")  # sin espacio
    b.free("all")
    # ahora reservar múltiples pequeños
    for i in range(8):
        b.reserve(1, f"n{i}")
    # liberar algunos y reservar par
    b.free("n0"); b.free("n1")
    b.reserve(2, "pair")
