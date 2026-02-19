# Taller Construyendo Mundo 3D
**Estudiante:** Juan Mateo Rozo Torres

**Fecha:** 21-02-2026

**objetivo:** Comprender las estructuras gráficas básicas que forman los modelos 3D (mallas poligonales) y visualizar su estructura en distintas plataformas

## Implementaciones:
### Three.js
Esta implementación crea una escena 3D utilizando React Three Fiber (wrapper de Three.js para React) y carga un modelo en formato GLTF.

El componente Model utiliza useGLTF para importar el modelo y luego recorre la jerarquía de la escena (scene.traverse) para modificar cada malla (mesh) encontrada.

Para cada malla se realizan tres acciones principales:

- **Aplicar un material sólido**
Se asigna un MeshStandardMaterial color naranja para visualizar el volumen del objeto con iluminación.

- **Agregar un wireframe**
Se genera una WireframeGeometry y se dibuja como LineSegments, lo que permite visualizar la estructura triangular interna del modelo (topología).

- **Mostrar los vértices como puntos**
Se crea un objeto Points utilizando la misma geometría del mesh, renderizando cada vértice como un punto rojo visible.

### Python:
Esta implementación utiliza trimesh para cargar un modelo 3D en formato .OBJ, .STL o .GLTF y extraer su información geométrica básica.
Se visualiza la malla en 3D con matplotlib, diferenciando caras (superficie), aristas (líneas) y vértices (puntos) mediante colores distintos.
Además, se muestra información estructural del modelo como el número de vértices, aristas y caras, permitiendo analizar su composición geométrica.

## Resultados visuales:
### Three.js:
![visualización modelo simple](./media/model_1.gif)

![visualización modelo con aristas y vérctices](./media/model_mesh.gif)

### Python:
![imagen de ejecucion en colab](./media/model_py.png)

## Código relevante:

## Prompts utilizados:
```
debo hacer esto pero no tengo idea de que significa: Crear un proyecto con Vite y React Three Fiber. Cargar un modelo 3D en formato .OBJ, .STL o .GLTF usando @react-three/drei. Visualizar el modelo con OrbitControls. Resaltar vértices, aristas o caras usando efectos visuales como líneas (Edges, Wireframe) o puntos (Points).
```
```
that's it, here is a new task: Python (Colab o Jupyter Notebook) Herramientas: trimesh, vedo, numpy, matplotlib Cargar modelos .OBJ, .STL o .GLTF usando trimesh o vedo. Visualizar malla 3D con colores distintos para vértices, aristas y caras. Mostrar información estructural del modelo: número de vértices, aristas y caras.
```

## Aprendizajes:

## Dificultades:
Nunca he utilizado javascript ni react antes.
