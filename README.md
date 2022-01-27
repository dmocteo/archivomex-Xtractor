# archivomex-Xtractor
Proyecto de Archivomex Estadísticas históricas de México. CIDE-INEGI-CentroGEO


La versión más actualizada (v1.1.1) de nuestra herramienta open-source de extracción para exportar información númerica de los tomos en PDF de las Estadísticas Históricas de México a tablas en xls. Esta versión solo corre en maquinas Windows10, una futura versión para macOS está en desarrollo. Con este enlace puedes descargar directamente la herramienta ejecutable en formato zip.

https://drive.google.com/file/d/1IRNFwpq8jTKwjv4e9d0BNQ-TGOygRF7v/view?usp=sharing

**Uso directamente desde Python**

Para poder utilizar la versión de Python es necesario tener los siguientes paquetes con sus respectivas versiones:

Openpyxl 3.0.3 <br />
TK-tools 0.12.0 <br />
PyMuPDF 1.17.3 <br />
opencv-python 4.3.0.36 <br />
pytesseract 0.3.4 <br />
Pillow 7.2.0 <br />

Se puede utilizar el archivo librerias.py ubicado en cualquiera de las subcarpetas para instalar los paquetes.

Es necesario instalar una versión de Python igual o superior a 3.6.

Es necesario hacer la instalación de Tesseract-OCR para el correcto funcionamiento de la herramienta. La ubicación de Tesseract-OCR debe de ser la misma en la que se encuentra el archivo .py del Xtractor que se esté utilizando o se deben de actualizar las rutas con la referencia correcta.

Para más información sobre la primera instalación, revisar el "Manual de Instalación Xtractor" que se encuentra dentro de la carpeta Xtractor EHM 2014.


**Xtractor EHM 2014**

Esta versión de la herramienta es exclusiva para la extracción de tablas de las Estadísticas Históricas de México de 2014.

Se recomienda comenzar por este Xtractor para tener la instalación adecuada para el uso de las adicionales herramientas disponibles. Revisar el "Manual de Instalación Xtractor" que se encuentra dentro de la carpeta Xtractor EHM 2014.

Para verificar si la instalación fue satisfactoria y conocer el funcionamiento de la herramienta, se deben de realizar los siguientes pasos:

1. Correr el script de Python *ArchivoMex_Extractor.py*, la siguiente ventana deberá de aparecer en la pantalla:

![image](https://user-images.githubusercontent.com/42630580/151274875-551f7dd3-523f-4687-9468-0cf66c9cba99.png)

2. Seleccionar de la carpeta EHM2014 el anuario estadístico de su interés y la página donde se encuentra la tabla que desea extraer. Indicar el índice de la tabla dentro de la página seleccionada, se debe de contar de arriba para abajo comenzando con el índice 1. En caso de que la extracción sea errónea y presente texto o números que no corresponden a los de la tabla, incremente el valor del zoom en 1 y ajuste los demás parámetros de acuerdo a la fórmula. Para este ejemplo se seleccionó el anuario estadístico número 18 (Precios), con la página 130 y la tabla número 2.

![image](https://user-images.githubusercontent.com/42630580/151275603-2d110560-d2d6-4175-9fb9-a0aefa1531bf.png)

3. Una vez se llenan los campos, se da click en el botón de procesar. Una vez que el procesamiento termine deberá de aparecer un mensaje indicando el fin del proceso. El archivo de Excel se encontrará en la misma ubicación del script de Python.

![image](https://user-images.githubusercontent.com/42630580/151275836-92c0b81c-c29c-459c-bf0b-a4646cbd3f1d.png)

**Resultado**

![image](https://user-images.githubusercontent.com/42630580/151276009-df82d3e4-93fd-4fe4-8b70-fb4dc273f985.png)

*Es importante destacar que el Xtractor está limitado a extraer únicamente el contenido de la tabla, el título y los encabezados se ignoran.

**Censo Hospitales**

Esta versión de la herramienta es exclusiva para la extracción de tablas del Censo y Planificación de hospitales de 1959.

En el siguiente enlace se encuentra el Censo y Planificación de hospitales de 1959: https://drive.google.com/file/d/15EFbzDvc8BgYMi1zHzNbatozrkC_sAYT/view?usp=sharing

Los prerrequisitos para el uso de esta herramienta son los mismos que se utilizan en el Xtractor EHM 2014.

Para verificar si la instalación fue satisfactoria y conocer el funcionamiento de la herramienta, se deben de realizar los siguientes pasos:

1. Correr el script de Python *CensoHospitalesExtrator_GUI.py*, la siguiente ventana deberá de aparecer en la pantalla:

![image](https://user-images.githubusercontent.com/42630580/151276748-b0db9485-78cd-489f-be4c-4b4fbeb5140a.png)

2. Seleccionar el PDF del censo y planificación de hospitales, el número de página del PDF y el número de página del censo (1 o 2). Dejar el campo de rotar en "0" y dar click en Procesar. Para este ejemplo se seleccionó la página 16 del PDF y la página 2 del Censo.

![image](https://user-images.githubusercontent.com/42630580/151277377-455614ff-7c4d-4a0a-9f17-060e62e1c372.png)

3. Se van a generar imagenes de cada tabla segmentada y puede que en algunos casos una imagen de *ruido*. Deberá de aparecer el mensaje de completado.

![image](https://user-images.githubusercontent.com/42630580/151277297-804a27e1-d611-4500-881c-4f6ac483ae0a.png)


**Xtractor EHM 1970**

Está versión de la herramienta es exclusiva para la extracción de tablas de las Estadísticas Históricas de México de 1970.

Para el uso de esta herramienta es necesario entrenar un modelo de clasificación de caracteres del 0-9 para la extracción de los datos numéricos de la tabla. En la carpeta CNN se encuentra el dataset utilizado para el entrenamiento de la red, así como un algoritmo de segmentación de caracteres para generar un dataset propio.

*Para obtener mejores resultados, procesar imagenes de las columnas individuales (ColumnaLista.png), segmentadas manualmente de la imagen original (Original.png). También es posible procesar toda la imagen generada.

Una vez que se genera el modelo de clasificación, es posible utilizar el *Xtracor CNN.py* para la extracción de tablas.

*Es necesario actualizar las rutas de acceso a archivos. Las rutas que se encuentran definidas quedan como ejemplo para obtener un correcto funcionamiento de la herramienta.
