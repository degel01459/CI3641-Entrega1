/**
 * P1MatrixProduct.kt
 * Calcular A x A^T para matriz cuadrada A (N x N).
 * 
 * Kevin Briceño 15-11661
 * 
 * Uso: ejecutar main con un ejemplo.
 */

fun multiplyMatrixByTranspose(A: Array<IntArray>): Array<LongArray> {
    val n = A.size
    // Validación explícita de cuadratura:
    // Se requiere que A sea N x N porque la fórmula (A × A^T) asume que
    // cada fila tiene exactamente n elementos para que el producto punto
    // entre filas (índice k de 0..n-1) sea bien definido.
    // Si hubiera filas de distinta longitud, el bucle sobre k fallaría
    // o produciría resultados incorrectos. Por eso usamos require.
    require(A.all { it.size == n }) { "A debe ser cuadrada (N x N)" }
    // Usamos Long en el resultado y en las operaciones intermedias porque:
    // 1) Producto de dos Int puede exceder el rango de Int si los valores son grandes.
    // 2) La suma acumulada de hasta n productos puede desbordar Int incluso cuando
    //    cada producto individual quepa en Int.
    // Convertir a Long antes de multiplicar y acumular garantiza corrección
    // para matrices con elementos intensos o dimensiones mayores.
    val result = Array(n) { LongArray(n) { 0L } }
    for (i in 0 until n) {
        for (j in 0 until n) {
            var sum = 0L
            for (k in 0 until n) {
                // Convertimos cada operando a Long antes de multiplicar para:
                // - evitar overflow en la multiplicación A[i][k] * A[j][k]
                // - mantener la suma en rango Long durante la acumulación
                sum += A[i][k].toLong() * A[j][k].toLong() // A^T element (k,j) == A[j][k]
            }
            result[i][j] = sum
        }
    }
    return result
}

// Utilidades para imprimir
fun printMatrixLong(mat: Array<LongArray>) {
    for (row in mat) {
        println(row.joinToString(prefix = "[", postfix = "]") { it.toString() })
    }
}

fun main() {
    val A = arrayOf(
        intArrayOf(1, 2, 3),
        intArrayOf(4, 5, 6),
        intArrayOf(7, 8, 9)
    )
    println("Matriz A:")
    A.forEach { println(it.joinToString(prefix = "[", postfix = "]")) }
    val P = multiplyMatrixByTranspose(A)
    println("\nA x A^T:")
    printMatrixLong(P)
}
