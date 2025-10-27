#### Información del Autor
-   **Nombre**: Kevin Briceño
-   **Carnet**: 15-11661
-   **Email**: 15-11661@usb.ve

# **Ejercicio 1**

Escoja algún lenguaje de programación de alto nivel y de propósito general cuyo nombre empiece con la misma letra que su nombre: 
**K (Kotlin)**

## Parte A: Análisis del Lenguaje Kotlin

### Descripción del Lenguaje Escogido
Kotlin es un lenguaje de alto nivel, estáticamente tipado y de propósito general desarrollado por JetBrains. Se ejecuta principalmente sobre la JVM mediante compilación a bytecode, y también soporta compilación a JavaScript y a código nativo con Kotlin/Native. Integra características de programación orientada a objetos y funcional: lambdas, extensiones, null-safety, data classes, coroutines y una interoperabilidad casi total con Java.

## Alcances y Asociaciones (Bindings)
### Tipo de Alcance

*   **Alcance léxico (estático)**: Las referencias a nombres se resuelven por la estructura del código en tiempo de compilación.

### Tiempos de Binding

*   **Design / Implementation time**: Definiciones del lenguaje y representación en la JVM.
*   **Compile time**: Verificación de tipos, resoluciones léxicas y offsets relativos.
*   **Run time**: Valores concretos y despacho dinámico de métodos cuando corresponde.

### Observaciones sobre Late Binding

Los métodos son finales por defecto; para permitir despacho dinámico un método debe declararse `open` o ser parte de una interfaz. El diseño combina seguridad estática con la capacidad de despacho dinámico donde es necesario.

### Ventajas

*   Detección temprana de errores por tipado estático y mecanismos de seguridad frente a nulos.
*   Eficiencia por la compilación a bytecode de la JVM y optimizaciones del runtime.
*   Predictibilidad para razonar el código por su alcance léxico.
*   Interoperabilidad sólida con el ecosistema Java.

### Desventajas

*   Mayor rigidez para programadores procedentes de lenguajes dinámicos.
*   Cierta dependencia en el comportamiento de la JVM para aspectos de runtime.
*   Curva de aprendizaje en detalles como `open`/`override` y la distinción `val`/`var`.

## Módulos, Importación y Exportación

### Concepto de Módulo

*   A nivel de lenguaje existen `packages` para agrupar nombres.
*   A nivel de proyecto, módulos son artefactos gestionados por Gradle/Maven.
*   En plataformas que lo soportan puede interoperar con el sistema de módulos de Java.

### Formas de Importar y Exportar Nombres

*   Declaración de paquete con `package`.
*   Import con `import` y wildcard `*`.
*   Import con alias `as` para renombrar al importar.
*   Símbolos públicos se exportan por defecto; visibilidad controlada por `public`, `internal`, `protected` y `private`. `internal` es visible dentro del módulo de compilación.

### Tipos de Módulos Soportados

*   Módulos JVM empaquetados como JAR.
*   Proyectos Kotlin Multiplatform que comparten código entre JVM, JS y Native.
*   Namespaces organizados por `packages` y `subpackages`.

## Aliases, Sobrecarga y Polimorfismo

### Aliases

*   Soporta `typealias` para sinónimos de tipos que no crean tipos nuevos:
    ```kotlin
    typealias UserId = Int
    ```
*   También se pueden crear alias de import:
    ```kotlin
    import com.lib.LongName as LN
    ```

### Sobrecarga

*   Kotlin permite sobrecargar funciones y constructores por firma (tipo / número de parámetros). Dispone de mecanismos que reducen la necesidad de sobrecarga, como parámetros con valores por defecto y `named arguments`.
    ```kotlin
    fun suma(a: Int, b: Int): Int = a + b
    fun suma(a: Double, b: Double): Double = a + b
    ```

### Polimorfismo

*   **Polimorfismo de inclusión** por herencia y dispatch dinámico en métodos `open`/`override`:
    ```kotlin
    open class A { open fun f() = println("A") }
    class B: A() { override fun f() = println("B") }
    ```
*   **Polimorfismo paramétrico** mediante genéricos:
    ```kotlin
    class Box<T>(val value: T)
    ```
*   Soporta **funciones de orden superior y lambdas**, donde funciones son valores de primera clase.

## Herramientas y Ecosistema

*   **Compiladores y runtimes**: `kotlinc` para outputs JVM, JS y Native. Kotlin/Native y Kotlin/JS como backends alternativos. Kotlin REPL para ejecución interactiva.
*   **IDEs, debugging y profiling**: Soporte completo en IntelliJ IDEA y Android Studio, con debugger integrado. Profilers compatibles: VisualVM, YourKit, JProfiler, Java Flight Recorder.
*   **Build, frameworks y testing**: Integración con Gradle (Kotlin DSL) y Maven. Frameworks: Ktor, Spring Boot con Kotlin. Concurrencia: coroutines. Testing: JUnit, Kotest. Análisis estático: ktlint, detekt.

## Referencias Bibliográficas

*   Kotlin Documentation https://kotlinlang.org/docs/reference/
*   Kotlin Coroutines Guide https://kotlinlang.org/docs/coroutines-overview.html
*   Kotlin Multiplatform https://kotlinlang.org/docs/multiplatform.html
*   Kotlin/Native y Kotlin/JS https://kotlinlang.org/docs/native-overview.html https://kotlinlang.org/docs/js-overview.html
*   Kotlin Style Guide https://kotlinlang.org/docs/coding-conventions.html

# Parte B: Ejercicios en Kotlin

Este repositorio contiene las soluciones en Kotlin para dos problemas: rotación de cadenas y multiplicación de una matriz por su transpuesta.

## Ejercicio 1: Rotación de Cadenas (`P1Rotar.kt`)

### Descripción del Problema

Dada una cadena de caracteres `w` y un entero no–negativo `k`, calcular la rotación de `k` posiciones de la cadena `w`. Utilice la siguiente fórmula como referencia:

```
rotar(w,k) = 
  w                                  si k = 0 ∨ |w| = 0
  rotar(x ++ [a], k - 1)             si k > 0 ∧ w = ax ∧ a es un caracter
```
donde el operador `++` corresponde a la concatenación de cadenas de caracteres.

**Ejemplo:**

- rotar("hola", 0) = "hola" 
- rotar("hola", 1) = "olah" 
- rotar("hola", 2) = "laho" 
- rotar("hola", 3) = "ahol" 
- rotar("hola", 4) = "hola" 
- rotar("hola", 5) = "olah" 


### Implementación

El archivo `P1Rotar.kt` contiene dos implementaciones:

1.  `rotarRec(w: String, k: Int)`: Una función recursiva que sigue la definición formal del problema, moviendo el primer carácter al final en cada llamada.
2.  `rotarIter(w: String, k: Int)`: Una función iterativa más eficiente que calcula la posición final de la rotación y reconstruye la cadena usando `substring`.

Ambas funciones normalizan `k` para manejar rotaciones mayores que la longitud de la cadena.

### Cómo Compilar y Ejecutar

1.  **Compilar el código en un archivo JAR:**

    ```bash
    kotlinc P1Rotar.kt -include-runtime -d P1Rotar.jar
    ```

2.  **Ejecutar el programa:**

    ```bash
    java -jar P1Rotar.jar
    ```

### Salida de Ejemplo

```
rotarRec("hola", 0) = "hola"
rotarRec("hola", 1) = "olah"
rotarRec("hola", 2) = "laho"
rotarRec("hola", 3) = "ahol"
rotarRec("hola", 4) = "hola"
rotarRec("hola", 5) = "olah"
```

## Ejercicio 2: Producto de Matriz por su Transpuesta (`P1MatrixProduct.kt`)

### Descripción del Problema

Dada una matriz cuadrada `A` de dimensión `N x N`, calcular el producto `A × A^T`, donde `A^T` es la transpuesta de `A`.

La fórmula del producto es: `\forall i,j\in{1..N}:(A × B)_ij = Σ_(k\in{1..N})(A_ik * B_kj)`
La transpuesta se define como: `\forall i,j\in{1..N}:A^T_ij = A_ji`

Por lo tanto, el elemento `(i, j)` del resultado es: `Σ_(k\in{1..N})(A_ik * A_jk)`

### Implementación

El archivo `P1MatrixProduct.kt` contiene la función `multiplyMatrixByTranspose(A: Array<IntArray>)`.

-   Valida que la matriz de entrada sea cuadrada.
-   Calcula el producto `A × A^T` de manera eficiente sin generar explícitamente la matriz transpuesta.
-   Utiliza el tipo `Long` para los elementos de la matriz resultante para prevenir desbordamientos (`overflow`) durante la suma de productos.

### Cómo Compilar y Ejecutar

1.  **Compilar el código en un archivo JAR:**

    ```bash
    kotlinc P1MatrixProduct.kt -include-runtime -d P1MatrixProduct.jar
    ```

2.  **Ejecutar el programa:**

    ```bash
    java -jar P1MatrixProduct.jar
    ```

### Salida de Ejemplo

```
Matriz A:
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]

A x A^T:
[14, 32, 50]
[32, 77, 122]
[50, 122, 194]
```
