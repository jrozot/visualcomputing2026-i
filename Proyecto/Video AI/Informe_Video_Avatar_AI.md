# Documento Técnico – Video con Avatar AI Proyecto Final

## Herramientas utilizadas

- Generación de guion: NotebookLM y ChatGPT.
- Generación de voz: FreeTTS.
- Creación de avatares: DreamFaceAI.
- Edición de video: Kdenlive.

## Descripción del flujo implementado

### 1. Definición del guion

El proyecto fue realizado por un único integrante. El video se dividió en dos secciones:

- Primeros 5 minutos: avatar femenino presentando el problema y su contexto.
- Siguientes 10 minutos: avatar masculino mostrando los resultados obtenidos, dos desafíos encontrados durante el desarrollo y una explicación de cómo ejecutar el programa.

### 2. Generación del contenido

- Se crearon diapositivas para acompañar la introducción.
- Se realizaron grabaciones de pantalla para mostrar la demostración del programa y partes relevantes del código.
- Se generaron las narraciones mediante herramientas de texto a voz.

### 3. Edición del video

Todo el contenido fue integrado en Kdenlive. Durante esta etapa se sincronizaron las narraciones con las diapositivas, demostraciones y demás elementos visuales.

### 4. Creación de avatares

Se utilizaron avatares generados con DreamFaceAI en formato de presentador. Los avatares se emplearon principalmente como separadores entre secciones del video, utilizando fragmentos específicos del guion.

## Dificultades encontradas

La edición en Kdenlive no presentó dificultades importantes debido a experiencia previa con la herramienta. La generación del guion y de la voz también resultó sencilla.

La principal dificultad fue la generación de avatares animados con sincronización labial. Inicialmente se intentó utilizar SadTalker, pero la instalación resultó problemática debido a la gran cantidad de dependencias requeridas, incluyendo Conda, PyTorch y versiones específicas de diferentes bibliotecas que generaban conflictos.

Por esta razón se optó por utilizar DreamFaceAI en su versión gratuita. Sin embargo, esta herramienta dispone de una cantidad limitada de créditos, por lo que los avatares aparecen únicamente en algunas partes del video.

## Archivos del proceso

- Guion generado con NotebookLM y ChatGPT.
- Audios generados con FreeTTS.
- Avatares generados con DreamFaceAI.
- Proyecto de edición realizado en Kdenlive.
- Video final exportado en formato MP4.
