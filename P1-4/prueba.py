# prueba.py
# Kevin Briceño 15-11661
# Script de prueba para el módulo vector3d.py

from vector3d import Vector3D

a = Vector3D(1,2,3)
b = Vector3D(4,5,6)
c = Vector3D(0,1,0)

# suma / resta
r1 = b + c
print(r1)
r2 = a - 1
print(r2)

# producto cruz y punto
cross = a * b     # vector
print(cross)
dot   = a % b     # número
print(dot)

# norma
n1 = abs(b)
print(n1)
n2 = ~b           # sinónimo de abs
print(n2)
n3 = 0 & b        # hack que devuelve norma (documentado)
print(n3)

# expresiones compuestas
expr = a * 3.0 + ~b
print(expr)
expr2 = (b + b) * (c - a)
print(expr2)
expr3 = a % (c * b)   # primero c*b (cross), luego dot con a
print(expr3)