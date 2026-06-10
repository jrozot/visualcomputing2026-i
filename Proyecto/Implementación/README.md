# Panel de Simulación 3D de Bandadas (Boids)

Una **simulación de bandadas (Boids) en 3D en tiempo real** renderizada con OpenGL dentro de un panel de escritorio con apariencia profesional. Construida con **PyQt6**, **pyqtgraph** (`GLViewWidget` de OpenGL) y **NumPy**. Todo se ejecuta localmente.

## Características

- **Boids clásicos de Reynolds**: separación, alineación y cohesión.
- **Cubo 3D acotado** con límites periódicos (wrap-around), utilizando la convención de imagen mínima para que los boids interactúen a través de los bordes.
- **~250 boids**, completamente vectorizados con NumPy para una animación fluida.
- **Visor 3D OpenGL** con cuadrícula de suelo, indicadores de ejes XYZ y un cubo delimitador en estructura alámbrica. Los boids se dibujan como "dardos" orientados y coloreados según su velocidad (azul profundo → cian brillante), haciendo evidente la dirección del movimiento.
- **Controles de cámara**: arrastrar para rotar, rueda para acercar/alejar, arrastre con botón central o Shift+arrastre para desplazar la vista (controles estándar de `GLViewWidget`).
- **Panel de control**: Iniciar / Pausar / Reiniciar, además de deslizadores en tiempo real para velocidad de los boids, radio de percepción y fuerzas de separación, alineación y cohesión. Los cambios se aplican instantáneamente.
- **Métricas en vivo**: cantidad total de boids, velocidad promedio, distancia promedio al vecino más cercano, número estimado de grupos y tiempo de ejecución de la simulación.
- **Gráficas en tiempo real**: velocidad promedio, distancia promedio entre vecinos y número de grupos dentro de una ventana temporal deslizante.
- **Tema oscuro** en toda la aplicación.

## Estructura del proyecto

```text
.
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── README.md
└── boids/                  # Paquete principal de la aplicación
    ├── __init__.py
    ├── simulation.py       # Simulación Boids vectorizada + métricas (NumPy)
    ├── viewport.py         # Escena OpenGL 3D (GLViewWidget)
    ├── controls.py         # Botones + deslizadores de parámetros en vivo
    ├── metrics_panel.py    # Visualización de métricas en tiempo real
    ├── charts.py           # Gráficas en tiempo real con pyqtgraph
    ├── theme.py            # Hoja de estilos oscura para Qt
    └── main_window.py      # Diseño del panel + ciclo de simulación
```

## Requisitos

- Python **3.11+**
- Una GPU/controlador con soporte básico para OpenGL (cualquier portátil típico debería funcionar).

## Instalación y ejecución

```bash
# (opcional) crear un entorno virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

Presiona **Iniciar (Start)** para comenzar la simulación y luego experimenta con los deslizadores.

### Nota para Linux

PyQt6/OpenGL requiere bibliotecas GL del sistema. En Debian/Ubuntu, si la ventana no se abre debido a un error de OpenGL, instala:

```bash
sudo apt install libgl1 libglu1-mesa libxcb-cursor0
```

## Cómo funciona

Cada paso calcula una única vez la matriz de desplazamientos por pares considerando los límites periódicos y la reutiliza tanto para las fuerzas de dirección como para las métricas en vivo:

- **Separación**: aleja a cada boid de los vecinos cercanos, ponderando por el inverso del cuadrado de la distancia.
- **Alineación**: orienta al boid hacia la dirección promedio de los vecinos dentro del radio de percepción.
- **Cohesión**: dirige al boid hacia el centro de masa local de esos vecinos.

La velocidad se limita a un intervalo `[min, max]` para que los boids siempre se mantengan en movimiento sin superar la capacidad de la simulación. El **número de grupos (clusters)** se estima mediante una estructura union-find sobre el grafo formado por boids que se encuentran a una distancia menor que la mitad del radio de percepción entre sí.

## Ajuste de parámetros

Los valores predeterminados se encuentran en `boids/simulation.py` (`SimulationParams`) y `boids/main_window.py` (`N_BOIDS`, `BOUNDS`, `FPS`). Reducir `N_BOIDS` o `FPS` puede mejorar el rendimiento en equipos más lentos.
