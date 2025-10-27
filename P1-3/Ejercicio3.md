#### Información del Autor
- **Nombre**: Kevin Briceño
- **Carnet**: 15-11661
- **Email**: 15-11661@usb.ve

# Simulador del Buddy System

Este ejercicio implementa un simulador simple del algoritmo de gestión de memoria **Buddy System** en Python. Proporciona una clase `BuddyAllocator` y una interfaz de línea de comandos (CLI) para interactuar con el asignador de memoria.

## Archivos del Ejercicio 3

- `buddy.py`: Contiene la implementación de la clase `BuddyAllocator` y la función `run_cli` para la interfaz interactiva.
- `test_buddy.py`: Pruebas unitarias utilizando `pytest` para validar el comportamiento del asignador.
- `Ejercicio3.md`: Este archivo.

## Características

- **Inicialización**: El asignador se inicia con un número total de bloques, que debe ser una potencia de dos.
- **Interfaz Interactiva**: Un bucle de comandos permite al usuario realizar operaciones de reserva, liberación y visualización del estado de la memoria.
- **Validación de Entradas**: Todos los comandos y sus argumentos son validados para prevenir errores.
- **Pruebas Unitarias**: El proyecto incluye un conjunto de pruebas con `pytest` y está configurado para medir la cobertura de código.

## Comandos de la CLI

La interfaz interactiva soporta los siguientes comandos:

- `RESERVAR <cantidad> <nombre>`: Reserva un bloque de memoria de al menos `<cantidad>` unidades y lo asocia a un `<nombre>`.
- `LIBERAR <nombre>`: Libera el bloque de memoria asociado al `<nombre>`.
- `MOSTRAR`: Muestra el estado actual de las listas de bloques libres y las asignaciones activas.
- `SALIR`: Termina la ejecución del programa.

## Diseño y Algoritmo

### Representación de la Memoria

- `total_blocks`: Número total de bloques de memoria (`N`), debe ser una potencia de dos.
- `order`: El tamaño de un bloque se define como `2**order`. Un `order = 0` corresponde a un bloque de tamaño unitario.
- `free_lists`: Un diccionario donde `free_lists[order]` contiene una lista con los índices de inicio de los bloques libres de tamaño `2**order`.
- `allocated`: Un diccionario que mapea un `nombre` de asignación a una tupla `(start, order)` que representa el bloque asignado.

### Algoritmo de Reserva (`reserve`)

1.  Dado un número de bloques `k`, se calcula el `order` mínimo tal que `2**order >= k`.
2.  Se busca un bloque libre en `free_lists` comenzando desde el `order` calculado hacia órdenes mayores.
3.  Si no se encuentra un bloque lo suficientemente grande, se reporta un error.
4.  Si se encuentra un bloque en un `order` superior, se divide recursivamente (split) hasta alcanzar el `order` deseado. En cada división, un "buddy" se añade a la lista de bloques libres del `order` inferior.
5.  La asignación se registra en el diccionario `allocated`.

### Algoritmo de Liberación (`free`)

1.  Se obtiene el `start` y `order` del bloque a liberar desde el diccionario `allocated`.
2.  Se calcula la dirección de su "buddy" usando la operación `buddy = start ^ (1 << order)`.
3.  Se comprueba si el buddy está en la lista de bloques libres del mismo `order`.
4.  **Si el buddy está libre**: se fusionan (merge) ambos bloques en uno de `order + 1`. Este proceso se repite recursivamente para órdenes superiores.
5.  **Si el buddy no está libre**: el bloque recién liberado simplemente se añade a la lista de bloques libres de su `order`.

## Instrucciones de Uso

### 1. Preparar el Entorno

Se recomienda usar un entorno virtual.

```bash
python -m venv venv

# En Linux / macOS
source venv/bin/activate

# En Windows
.\venv\Scripts\Activate
```

### 2. Instalar Dependencias

Las dependencias son necesarias para ejecutar las pruebas.

```bash
pip install pytest pytest-cov
```

### 3. Ejecutar la Interfaz (CLI)

Para iniciar el simulador con un total de 16 bloques:

```bash
python -c "from buddy import run_cli; run_cli(16)"
```

Esto iniciará el prompt `ACTION>`.

### Ejemplo de Sesión

```
$ python -c "from buddy import run_cli; run_cli(8)"
Buddy allocator iniciado con 8 bloques (unidad)
ACTION> MOSTRAR
Total blocks: 8 (orders 0..3)
Free lists:
  order 3 (size=8): [0]
  order 2 (size=4): []
  order 1 (size=2): []
  order 0 (size=1): []
Allocations:
ACTION> RESERVAR 3 foo
Reservado 'foo' en start 0, size 4 (order 2)
ACTION> MOSTRAR
Total blocks: 8 (orders 0..3)
Free lists:
  order 3 (size=8): []
  order 2 (size=4): [4]
  order 1 (size=2): []
  order 0 (size=1): []
Allocations:
  foo: start=0, size=4 (order 2)
ACTION> LIBERAR foo
Liberado 'foo'
ACTION> MOSTRAR
Total blocks: 8 (orders 0..3)
Free lists:
  order 3 (size=8): [0]
  order 2 (size=4): []
  order 1 (size=2): []
  order 0 (size=1): []
Allocations:
ACTION> SALIR
Bye
```

## Pruebas y Cobertura

El archivo `test_buddy.py` contiene pruebas unitarias que cubren:
- Inicialización (válida e inválida).
- Reservas con y sin división (split).
- Liberaciones con y sin fusión (merge).
- Casos de error (nombres duplicados, memoria insuficiente, etc.).
- Simulación de la interacción con la CLI.

### Ejecutar Pruebas

Para ejecutar todas las pruebas:

```bash
pytest -q
```

### Medir Cobertura de Código

Para generar un reporte de cobertura en la terminal que muestre las líneas no cubiertas:

```bash
pytest --cov=buddy --cov-report=term-missing
```
