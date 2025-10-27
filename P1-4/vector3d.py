# vector3d.py
# Implementación de un tipo Vector3D con operadores aritméticos
# Autor: Kevin Briceño

from math import sqrt, isclose
from typing import Union, Tuple

Number = Union[int, float]

EPS = 1e-9

class Vector3D:
    """Vector tridimensional con operaciones sobrecargadas:
    - suma / resta con Vector3D y con escalares (elementwise)
    - multiplicación '*':
        - Vector3D * Vector3D -> producto cruz (Vector3D)
        - Vector3D * escalar    -> multiplicación escalar (Vector3D)
    - módulo '%' -> producto punto (retorna float)
    - norma: usar abs(v) o ~v (retorna float)
    Nota: Python no permite operador unario '&', por eso ofrecemos ~v y abs(v).
    También se admite '0 & v' como atajo para norm(v) (ver __rand__).
    """

    def __init__(self, x: Number, y: Number, z: Number):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # Representaciones
    def __repr__(self) -> str:
        return f"Vector3D({self.x:.6g}, {self.y:.6g}, {self.z:.6g})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    # Comparación aproximada (útil para tests)
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector3D):
            return False
        return (isclose(self.x, other.x, rel_tol=1e-9, abs_tol=EPS) and
                isclose(self.y, other.y, rel_tol=1e-9, abs_tol=EPS) and
                isclose(self.z, other.z, rel_tol=1e-9, abs_tol=EPS))

    # Helper para detectar número
    @staticmethod
    def _is_number(value) -> bool:
        return isinstance(value, (int, float))

    # Suma
    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        if self._is_number(other):
            # suma escalar elemento a elemento
            return Vector3D(self.x + other, self.y + other, self.z + other)
        return NotImplemented

    def __radd__(self, other):
        # permite 3 + v  (será tratado como suma escalar elemento a elemento)
        return self.__add__(other)

    # Resta
    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        if self._is_number(other):
            return Vector3D(self.x - other, self.y - other, self.z - other)
        return NotImplemented

    def __rsub__(self, other):
        # permite escalar - vector -> (n-x, n-y, n-z)
        if self._is_number(other):
            return Vector3D(other - self.x, other - self.y, other - self.z)
        return NotImplemented

    # Multiplicación: sobrecargada para producto cruz (Vector x Vector) y escalar
    def __mul__(self, other):
        # Vector x Vector => producto cruz
        if isinstance(other, Vector3D):
            cx = self.y * other.z - self.z * other.y
            cy = self.z * other.x - self.x * other.z
            cz = self.x * other.y - self.y * other.x
            return Vector3D(cx, cy, cz)
        # Vector * escalar => multiplicación escalar
        if self._is_number(other):
            return Vector3D(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other):
        # escalar * Vector
        if self._is_number(other):
            return Vector3D(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    # Producto punto usando operador '%' (módulo)
    def __mod__(self, other):
        if not isinstance(other, Vector3D):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __rmod__(self, other):
        # en la práctica no se usa other % vector para punto, pero implementamos simetría
        return NotImplemented

    # Norma:
    def __abs__(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    # Permitimos usar ~v como sinónimo de norma (porque no existe & unario)
    def __invert__(self) -> float:
        return abs(self)

    # Para proporcionar una forma (hack) de usar '&' como en tu notación &v,
    # podemos soportar el caso: 0 & v  -> devuelve la norma de v.
    # Python evalúa 0 & v primero como int.__and__(0, v) -> NotImplemented -> llama v.__rand__(0)
    def __rand__(self, other):
        # si alguien escribe "0 & v", devolvemos la norma
        if other == 0:
            return abs(self)
        # si left operand es número distinto de 0, tratamos '&' como elemento-a-elemento bitwise no soportado
        return NotImplemented

    # Otros: convert to tuple y utilidades
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    @classmethod
    def from_iterable(cls, it):
        x, y, z = it
        return cls(x, y, z)
