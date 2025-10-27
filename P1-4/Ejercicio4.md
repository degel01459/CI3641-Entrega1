#### Información del Autor

-   **Nombre**: Kevin Briceño
-   **Carnet**: 15-11661
-   **Email**: 15-11661@usb.ve

# Ejercicio 4: Operaciones con Vectores Tridimensionales en Python

Este documento describe la implementación de un módulo en Python que define un tipo de vectores tridimensionales y operadores aritméticos sobre estos, cumpliendo con las características solicitadas.

### Implementación del Módulo de Vectores Tridimensionales
El módulo `vector3d.py` define una clase `Vector3D` que soporta las operaciones aritméticas solicitadas: suma, resta, producto cruz, producto punto y norma. Además, permite operaciones con escalares por la derecha.

### Características del Módulo
-   **Operaciones Soportadas**: 
- suma (+)
-   resta (-)
-   producto cruz (*)
-   producto punto (%)
-   norma (&)
-   **Expresiones Naturales**: Permite expresiones como:
-   `b + c`
-   `a * b + c`
-   `(b + b) * (c - a)`
-   `a % (c * b)`
-   **Operaciones con Escalares por la Derecha**:
-   `b + 3`
-   `a * 3.0 + &b`
-   `(b + b) * (c % a)`
-   donde `(x,y,z) ⊕ n = (x⊕n, y⊕n, z⊕n)`.
-   **Pruebas Unitarias**: Incluye pruebas unitarias con una cobertura mayor al 80%.
-   

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install pytest
pytest -q
pip install pytest-cov
pytest --cov=vector3d --cov-report=term-missing
