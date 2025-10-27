#### Información del Autor

-   **Nombre**: Kevin Briceño
-   **Carnet**: 15-11661
-   **Email**: 15-11661@usb.ve


# **Ejercicio 2**

## Análisis de Alcance y Asociación en Pseudo-código

Este documento presenta definiciones claras, notación explícita y trazas paso a paso para el mismo programa en pseudocódigo, bajo las cuatro combinaciones de reglas solicitadas:

- a) alcance estático + asociación profunda
- b) alcance dinámico + asociación profunda
- c) alcance estático + asociación superficial
- d) alcance dinámico + asociación superficial

Se muestran los marcos, valores intermedios y las salidas print exactas para cada caso.

## Programa en Pseudo-código

El análisis se basa en el siguiente programa, que utiliza subrutinas anidadas y las pasa como parámetros.

```c
// Variables globales
int a = Y + Z + 1, b = X + Y + 1, c = Z + Y + 1;
// Subrutinas globales
sub R (int b) {
	a := b + c - 1;
}
sub Q (int a, sub r) {
	b := a + 1;
	r(c);
} 
// Subrutina principal con subrutinas anidadas
sub P(int a, sub s, sub t) {
	sub R(int a) { 
		b := c + a + 1;
	}
	sub Q (int b, sub r) {
		c := a + b;
		r(c + a);
		t(c + b);
	}
	int c := a + b;
	if (a < 2 * (Y + Z + 1)) {
		P(a + 2 * (Y + Z + 1), s, R); 
	} else { 
		int a := c + 1;
		s(c * a, R); 
		Q(c * b, t);
	}
	print(a, b, c);
}

// Punto de entrada del programa
P(a, Q, R);
print(a, b, c);
```

## Valores Iniciales

Según las instrucciones, se utilizan los valores `X = 6`, `Y = 6`, `Z = 1`. Esto define las siguientes variables globales iniciales:

-   `global.a = Y + Z + 1 = 8`
-   `global.b = X + Y + 1 = 13`
-   `global.c = Z + Y + 1 = 8`
-   El umbral de recursión es `T = 2 * (Y + Z + 1) = 16`

## Análisis de Ejecución

La estructura de llamadas principal es la misma en todos los casos:
1.  Se invoca `P(8, Q_root, R_root)`, creando el marco `P1`.
2.  Dentro de `P1`, se cumple la condición del `if` y se realiza una llamada recursiva a `P(24, Q_root, R_local1)`, creando el marco `P2`.
3.  Dentro de `P2`, se ejecuta la rama `else`, que desencadena una secuencia de llamadas a las subrutinas `Q` y `R` pasadas como parámetros.

Lo que varía en cada caso es el entorno (contexto de variables) que se utiliza para resolver las referencias a variables libres (`a`, `b`, `c`) en el cuerpo de las subrutinas.

---

### a) Alcance Estático y Asociación Profunda

-   **Alcance Estático**: cada referencia libre se resuelve en el entorno léxico donde la subrutina fue *definida*.
-   **Asociación Profunda**: cuando pasas una subrutina como parámetro, el entorno que acompaña a esa subrutina se fija **en el momento del pase** (se crea un closure con el entorno del activador que pasa la subrutina).

**Traza de Ejecución:**
0.  **Estado Global Inicial**: `(a=8, b=13, c=8)`
1.  **Llamada inicial `P(a, Q, R) -> P1 = (a=8, s=Q_root, t=R_root)`**:
    -   Evaluación de c en P1: `P1.c := P1.a + global.b = 8 + 13 = 21`
    -   `if (8 < 16)` -> verdadero, se llama recursivamente
    -   `P(8 + 16, Q_root, R_local1) -> P2 = P(a=8+16=24, s=Q_root, t=R_local1_closure)`.
    -   `R_local1` es la R definida dentro de `P1` y el closure captura el entorno léxico de `P1` (por asociación profunda).
3.  **En `P2` se crea su `c` local: `P.c := P2.a + global.b = 24 + 13= 37`**.
    -   `if (24 < 16)` -> falso, se ejecuta la rama `else`.
    -   Declaración a local en else: `a_local := c + 1` -> dentro de P2, `a_local = 37 + 1 = 38`
    -   Llamada `s(c * a_local, R)` -> donde s = `Q_root(global)` y R = `R_local2_closure`. Se evalúan los argumentos:
    -   primer argumento =`P2.c*a_local = 37 * 38 = 1406`.
    -   segundo argumento = `R_local2_closure` (captura entorno léxico de `P2` por asociación profunda).
4.  **`Q_root(a=1406, r=R_local2_closure)`**:
    -   Q_root definido en el ámbito global: body `b := a + 1; r(c);`
    -   `global.b := 1406 + 1 = 1407`
    -   Q_root hace `r(c)` -> aquí `c` en `Q_root=global.c=8`. Por tanto `R_local2_closure(global.c=8)`.
5.  **`R_local2(a_param=8)`** (entorno léxico de `P2`):
    -   `global.b := P2.c(37) + a_param(8) + 1 = 46`
6.  **Regreso a `P2`**:
    -   `global.b` es ahora `46`.
    -   Llamada `Q_local2(c * global.b, t)` -> `Q_local2(37 * 46 = 1702, R_local1_closure)`.
7.  **`Q_local2(b_param=1702, r=R_local1_closure)`** (entorno léxico de `P2`):
    -   `P2.c := P2.a(24) + b_param(1702) = 1726`
    -   `Q_local2` hace `r(c+a)` -> c+a = 1726 + 24 = 1750. Por tanto, `R_local1_closure(1750)`.
8.  **`R_local1(a_param=1750)`** (entorno léxico de `P1`):
    -   `global.b := P1.c(21) + a_param(1750) + 1 = 1772`
9.  **Regreso a `Q_local2`**:
    -   Llamada `t(c+b)` -> `R_local1_closure(1726 + 1702 = 3428)`.
10. **`R_local1(a_param=3428)`** (entorno léxico de `P1`):
    -   `global.b := P1.c(21) + a_param(3428) + 1 = 3450`

**Salida Impresa:**
-   `print` en `P2`: `(a=24, b=3450, c=1726)`
-   `print` en `P1`: `(a=8, b=3450, c=21)`
-   `print` global: `(a=8, b=3450, c=8)`

---

### b) Alcance Dinámico y Asociación Profunda

-   **Alcance Dinámico**: referencias libres se resuelven recorriendo la cadena de llamadas en tiempo de ejecución (llamador más cercano).
-   **Asociación Profunda (deep binding)**: cuando se pasa una subrutina como argumento, se captura la cadena dinámica en el momento del pase; esa cadena será la que se use para resolver referencias libres dentro de la subrutina cuando se invoque más tarde.

**Traza de Ejecución:**
0.  **Estado Global Inicial**: `(a=8, b=13, c=8)`
1.  **`P1:P1.a = 8`**: `P1.c := P1.a + global.b = 8 + 13 = 21`
    -   `if (8 < 16)` -> verdadero, se llama recursivamente 
    -   `P2(24, Q_root, R_local1_closure)`; `R_local1_closure` captura la cadena dinámica hasta `P1`.
2.  **`P2:P2.a = 24`**: `P2.c := 24 + global.b = 24 + 13 = 37`
3.  `if (24 < 16)` -> falso, se ejecuta la rama `else`.
    -   `a_local := P2.c + 1` -> dentro de P2, `a_local = 37 + 1 = 38`
    -   Llamada `s(c * a_local, R_local2_closure)`; `R_local2_closure` captura la cadena dinámica hasta `P2`.
    -   primer argumento =`P2.c*a_local = 37 * 38 = 1406`.
    -   segundo argumento = `R_local2_closure`.
4.  **`Q_root(a=1406, r=R_local2_closure)`**:
    -   `global.b := a + 1 = 1406 + 1 = 1407`
    -   Llamada `r(c)`. La `c` libre se resuelve en el entorno del llamador (`P2`), así que `c = P2.c = 37`. Se llama a `R_local2_closure(37)`.
5.  **`R_local2(a_param=37)`** R definida en P2, pero con deep binding: su cadena dinámica fue capturada en el pase (cadena: global -> P1 -> P2), por lo que las referencias libres se resuelven en esa cadena capturada:
    -   Cuerpo: `global.b := P2.c(37) + a_param(37) + 1 = 75`
6.  **Regreso a `P2`**:
    -   `global.b` es ahora `75`.
    -   Llamada `Q_local2(c * global.b, R_local1_closure)` -> `Q_local2(37 * 75 = 2775, R_local1_closure)`.
7.  **`Q_local2(b_param=2775, r=R_local1_closure)`** (entorno dinámico de `P2`):
    -   `P2.c := P2.a(24) + b_param(2775) = 2799`
    -   `Q_local2` hace `r(c+a)` -> `R_local1_closure(2799 + 24 = 2823)`.
8.  **`R_local1(a_param=2823)`** (entorno dinámico de `P1`):
    -   La `c` libre se resuelve en el entorno de `P1`, así que `c = P1.c = 21`.
    -   `global.b := P1.c(21) + a_param(2823) + 1 = 2845`
9.  **Regreso a `Q_local2`**:
    -   Llamada `t(c+b)` -> `R_local1_closure(2799 + 2775 = 5574)`.
10. **`R_local1(a_param=5574)`** (entorno dinámico de `P1`):
    -   `global.b := P1.c(21) + a_param(5574) + 1 = 5596`

**Salida Impresa:**
-   `print` en `P2`: `(a=24, b=5596, c=2799)`
-   `print` en `P1`: `(a=8, b=5596, c=21)`
-   `print` global: `(a=8, b=5596, c=8)`

---

### c) Alcance Estático y Asociación Superficial

-   **Alcance Estático**: Las variables libres se resuelven buscando en el entorno léxico donde la función fue *definida*.
-   **Asociación Superficial (shallow)**: el entorno asociado a la subrutina pasada se determina en el momento de *invocación* — se usa el *entorno léxico del punto de invocación* para resolver referencias libres.

**Traza de Ejecución:**
1.  **Estado Global Inicial**: `(a=8, b=13, c=8)`
2.  **`P1` y `P2`** se ejecutan como antes. `P1.c=21`, `P2.c=37`.
3.  **`Q_root(a=1406, r=R_local2)`**:
    -   `global.b := 1407`
    -   Llamada `r(c)` -> `R_local2(global.c=8)`. Punto clave (shallow + static): el punto de invocación es `Q_root` (ámbito léxico = global), por tanto la `c` libre que se pasa a `R_local2` se resuelve como `global.c = 8`.
    -   Se invoca `R_local2(a_param=8)`.
4.  **`R_local2(a_param=8)`**:
    -   (R definida en P2, pero bajo shallow usamos el entorno léxico del punto de invocación — aquí: global):
    -   `global.b := global.c(8) + a_param(8) + 1 = 17`
5.  **Regreso a `P2`**:
    -   `global.b` es ahora `17`.
    -   Llamada `Q_local2(37 * 17 = 629, R_local1)`.
6.  **`Q_local2(b_param=629, r=R_local1)`** (entorno léxico de `P2`):
    -   `P2.c := P2.a(24) + b_param(629) = 653`
    -   Llamada `r(c+a)` -> `R_local1(653 + 24 = 677)`.
7.  **`R_local1(a_param=677)`**:
    -   El punto de invocación es `Q_local2`, cuyo entorno léxico es `P2`. La `c` libre en `R_local1` se resuelve a `P2.c`.
    -   `global.b := P2.c(653) + a_param(677) + 1 = 1331`
8.  **Regreso a `Q_local2`**:
    -   Llamada `t(c+b)` -> `R_local1(653 + 629 = 1282)`.
9.  **`R_local1(a_param=1282)`**:
    -   El entorno sigue siendo el de `P2`.
    -   `global.b := P2.c(653) + a_param(1282) + 1 = 1936`

**Salida Impresa:**
-   `print` en `P2`: `(a=24, b=1936, c=653)`
-   `print` en `P1`: `(a=8, b=1936, c=21)`
-   `print` global: `(a=8, b=1936, c=8)`

---

### d) Alcance Dinámico y Asociación Superficial

-   **Alcance Dinámico**: Las variables libres se resuelven buscando en la cadena de llamadas.
-   **Asociación Superficial (shallow)**: el entorno asociado a la subrutina pasada se determina en el momento de *invocación* — se usa el *entorno léxico del punto de invocación* para resolver referencias libres.

**Traza de Ejecución:**
1.  **Estado Global Inicial**: `(a=8, b=13, c=8)`
2.  **`P1` y `P2`** se ejecutan como antes. `P1.c=21`, `P2.c=37`.
3.  **`Q_root(a=1406, r=R_local2)`**:
    -   `global.b := 1407`
    -   `Q_root` hace `r(c)`. Dinámico + shallow: la `c` libre en el punto de invocación `Q_root` se resuelve en la cadena de llamadas actual, la cual incluye a `P2`; por eso `c = P2.c = 37`.
    -   Se invoca `R_local2(a_param)`.
4.  **`R_local2(a_param=37)`**:
    -   El entorno dinámico es el de `Q_root -> P2 -> ...`. Las variables libres `c` y `a` se resuelven en `P2`.
    -   `global.b := P2.c(37) + a_param(37) + 1 = 75`
5.  **Regreso a `P2`**:
    -   `global.b` es ahora `75`.
    -   Llamada `Q_local2(37 * 75 = 2775, R_local1)`.
6.  **`Q_local2(b_param=2775, r=R_local1)`**:
    -   `P2.c := P2.a(24) + b_param(2775) = 2799`
    -   Llamada `r(c+a)` -> `R_local1(2799 + 24 = 2823)`.
7.  **`R_local1(a_param=2823)`**:
    -   El punto de invocación es `Q_local2`, cuya cadena de llamadas es `Q_local2 -> P2 -> ...`. La `c` libre se resuelve a `P2.c`.
    -   `global.b := P2.c(2799) + a_param(2823) + 1 = 5623`
8.  **Regreso a `Q_local2`**:
    -   Llamada `t(c+b)` -> `R_local1(2799 + 2775 = 5574)`.
9.  **`R_local1(a_param=5574)`**:
    -   El entorno dinámico sigue siendo el de `Q_local2 -> P2 -> ...`.
    -   `global.b := P2.c(2799) + a_param(5574) + 1 = 8374`

**Salida Impresa:**
-   `print` en `P2`: `(a=24, b=8374, c=2799)`
-   `print` en `P1`: `(a=8, b=8374, c=21)`
-   `print` global: `(a=8, b=8374, c=8)`
