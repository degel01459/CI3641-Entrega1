# test_vector3d.py
# Pruebas unitarias para Vector3D
import pytest
import math
from vector3d import Vector3D

EPS = 1e-9

def test_construct_and_repr():
    v = Vector3D(1, 2, 3)
    assert v.to_tuple() == (1.0, 2.0, 3.0)
    assert "Vector3D" in repr(v)

def test_add_vector_and_scalar():
    a = Vector3D(1, 2, 3)
    b = Vector3D(4, 5, 6)
    assert a + b == Vector3D(5, 7, 9)
    assert a + 10 == Vector3D(11, 12, 13)
    assert 10 + a == Vector3D(11, 12, 13)

def test_sub_vector_and_scalar():
    a = Vector3D(5, 6, 7)
    b = Vector3D(1, 2, 3)
    assert a - b == Vector3D(4, 4, 4)
    assert a - 1 == Vector3D(4, 5, 6)
    assert 10 - b == Vector3D(9, 8, 7)

def test_scalar_mult_and_commutativity():
    a = Vector3D(1, 2, 3)
    assert a * 3 == Vector3D(3, 6, 9)
    assert 3 * a == Vector3D(3, 6, 9)

def test_cross_product():
    # cross product of (1,0,0) x (0,1,0) = (0,0,1)
    i = Vector3D(1,0,0)
    j = Vector3D(0,1,0)
    k = Vector3D(0,0,1)
    assert i * j == k
    # anti-commutativity: j * i == -k
    minus_k = Vector3D(0,0,-1)
    assert j * i == minus_k

def test_dot_product_mod_operator():
    a = Vector3D(1,2,3)
    b = Vector3D(4,5,6)
    # dot = 1*4 + 2*5 + 3*6 = 32
    assert a % b == 32
    # symmetry: a%b == b%a
    assert (a % b) == (b % a)

def test_norm_via_abs_and_invert_and_rand_and_examples():
    v = Vector3D(3, 4, 0)
    assert math.isclose(abs(v), 5.0, rel_tol=1e-9)
    # ~v as sinónimo de norma
    assert math.isclose(~v, 5.0, rel_tol=1e-9)
    # 0 & v deberá devolver la norma (hack documentado)
    assert math.isclose((0 & v), 5.0, rel_tol=1e-9)

def test_complex_expressions():
    a = Vector3D(1,0,0)
    b = Vector3D(0,1,0)
    c = Vector3D(0,0,1)
    # a * b + c  -> (a cross b) + c = (0,0,1)+(0,0,1) = (0,0,2)
    res = (a * b) + c
    assert res == Vector3D(0,0,2)
    # (b + b) * (c - a)  -> cross product
    r = (b + b) * (c - a)
    # compute expected manually:
    # b+b = (0,2,0) ; c-a = (-1,0,1) ; cross = (2*1 - 0*0, 0*(-1) - 0*1, 0*0 - 2*(-1)) = (2,0,2)
    assert r == Vector3D(2,0,2)

def test_errors_and_type_resilience():
    a = Vector3D(1,2,3)
    with pytest.raises(TypeError):
        _ = a % 3  # producto punto requiere Vector3D
    with pytest.raises(TypeError):
        _ = a * "x"  # multiplicación por cadena no soportada
