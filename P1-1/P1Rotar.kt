/**
 * P1Rotar.kt
 * Implementación de rotar(w,k) en Kotlin (recursiva y segura).
 *
 * Kevin Briceño 15-11661
 *
 * Observación: la rotación es "izquierda" por 1 posición en cada paso:
 * rotar("hola",1) = "olah"  // mueve 'h' al final
 */

fun rotarRec(w: String, k: Int): String {
    if (k == 0 || w.isEmpty()) return w
    val normalizedK = if (w.isEmpty()) 0 else (k % w.length)
    if (normalizedK == 0) return w
    // Caso recursivo: extraer primer char y concatenarlo al final
    fun helper(s: String, steps: Int): String {
        if (steps == 0) return s
        val a = s[0]
        val x = s.substring(1)
        return helper(x + a, steps - 1)
    }
    return helper(w, normalizedK)
}

// versión iterativa (más eficiente)
fun rotarIter(w: String, k: Int): String {
    if (w.isEmpty() || k == 0) return w
    val n = w.length
    val r = ((k % n) + n) % n
    // rotación izquierda por r => take substring from r..end + substring 0..r-1
    return w.substring(r) + w.substring(0, r)
}

fun main() {
    val tests = listOf(
        "hola" to 0,
        "hola" to 1,
        "hola" to 2,
        "hola" to 3,
        "hola" to 4,
        "hola" to 5
    )
    for ((s, k) in tests) {
        println("rotarRec(\"$s\", $k) = \"${rotarRec(s,k)}\"")
        // println("rotarIter(\"$s\", $k) = \"${rotarIter(s,k)}\"")
    }
}
