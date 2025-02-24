# I Will Find a Way

Una aplicación gráfica en Python para visualizar y comparar en tiempo real los algoritmos de búsqueda de caminos **A\*** y **Dijkstra**. La herramienta permite experimentar con diferentes funciones heurísticas y configuraciones de movimiento (con o sin diagonales), facilitando el aprendizaje y análisis de estos algoritmos.

---

## Características

- **Comparación de algoritmos:**  
  - **A\***: Utiliza una función heurística para guiar la búsqueda hacia la meta, acelerando la exploración en grafos grandes.
  - **Dijkstra:** Emplea únicamente el costo acumulado, expandiendo los nodos de forma más uniforme en todas las direcciones.

- **Configuración personalizable:**  
  - Selección de función heurística: Manhattan o Euclidiana.
  - Control exclusivo de los movimientos diagonales mediante un checkbox.
  - Edición interactiva del terreno: modifica celdas para crear obstáculos, agua, aire, etc.
  - Selección de puntos de inicio y meta mediante clics en la cuadrícula.

- **Visualización en tiempo real:**  
  - **Nodos expandidos:** Se marcan en gris claro.
  - **Nodos agregados a la frontera:** Se destacan en cian.
  - **Ruta final:** Se visualiza en color naranja.

---

## Instalación y Requisitos

### Requisitos

- Python 3.x
- Librerías:
  - Tkinter (generalmente incluida en la instalación de Python)
  - NumPy

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/i-will-find-a-way.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd i-will-find-a-way
   ```
3. (Opcional) Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```
4. Instala NumPy (si no lo tienes instalado):
   ```bash
   pip install numpy
   ```

---

## Uso

1. Ejecuta el script principal:
   ```bash
   python pathfinding_app.py
   ```
2. Interactúa con la interfaz:
   - **Selecciona puntos de inicio y meta:** Haz clic en la cuadrícula para establecerlos.
   - **Modifica el terreno:** Selecciona el tipo de terreno (grass, water, wall, air) desde el menú y haz clic en las celdas correspondientes.
   - **Configura el algoritmo:** Elige entre **A\*** y **Dijkstra** mediante el menú desplegable.
   - **Elige la heurística:** Selecciona entre **Manhattan** y **Euclidiana**.  
     _Nota:_ La heurística influye únicamente en el cálculo del costo estimado, mientras que la opción "Permitir diagonales" controla las direcciones de movimiento.
   - **Visualiza la búsqueda:** Pulsa el botón "Find Path" para iniciar la visualización en tiempo real del proceso de búsqueda.
   - **Otras opciones:**  
     - "Clear Selection" para reiniciar la selección de inicio y meta.
     - "Fill Grid with Grass" para rellenar la cuadrícula con terreno de hierba.

---

## Estructura del Proyecto

- **pathfinding_app.py:**  
  Código principal de la aplicación, que implementa la interfaz gráfica, la lógica de los algoritmos de búsqueda y la visualización en tiempo real.

- **README.md:**  
  Documentación y guía de uso del proyecto.

---

## Contribuciones

Las contribuciones son bienvenidas. Si deseas proponer mejoras, nuevas funcionalidades o corregir errores, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama con la nueva funcionalidad o corrección.
3. Envía un pull request describiendo los cambios realizados.

---

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo [LICENSE](https://opensource.org/licenses/MIT) para más detalles.

---

## Notas y Sugerencias

- **Optimización de la visualización:**  
  Se puede ajustar el parámetro `DELAY` para modificar la velocidad de actualización durante la búsqueda.

- **Extensiones futuras:**  
  - Implementar estadísticas de rendimiento (nodos expandidos, costo total, etc.).
  - Agregar nuevos algoritmos de búsqueda o técnicas de optimización.
  - Mejorar la interfaz gráfica para una experiencia más intuitiva.

---

_Disfruta explorando y comparando la búsqueda de caminos con **I Will Find a Way**!_
