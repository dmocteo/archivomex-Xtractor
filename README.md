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

Y de preferencia una versión de Python igual o superior a 3.6.

Es necesario hacer la instalación de Tesseract-OCR para el correcto funcionamiento de la herramienta.

Para más información sobre la primera instalación, revisar el "Manual de Instalación Xtractor" que se encuentra dentro de la carpeta Xtractor EHM 2014.

*Se deben de actualizar las rutas al ejecutable de Tesseract o incluirlo en el mismo directorio donde se encuentre el archivo .py que se esté utilizando.

**Xtractor EHM 2014**

Esta versión de la herramienta es exclusiva para la extracción de tablas de las Estadísticas Históricas de México de 2014.

Se recomienda comenzar por este Xtractor para tener la instalación adecuada para el uso de las adicionales herramientas disponibles.

**Censo Hospitales**

Esta versión de la herramienta es exclusiva para la extracción de tablas del Censo y Planificación de hospitales de 1959.

En el siguiente enlace se encuentra el Censo y Planificación de hospitales de 1959: https://drive.google.com/file/d/15EFbzDvc8BgYMi1zHzNbatozrkC_sAYT/view?usp=sharing

**Xtractor EHM 1970**

Está versión de la herramienta es exclusiva para la extracción de tablas de las Estadísticas Históricas de México de 1970.

Para el uso de esta herramienta es necesario entrenar un modelo de clasificación de caracteres del 0-9 para la extracción de los datos numéricos de la tabla. En la carpeta CNN se encuentra el dataset utilizado para el entrenamiento de la red, así como un algoritmo de segmentación de caracteres para generar un dataset propio.

*Para obtener mejores resultados, procesar imagenes de las columnas individuales (ColumnaLista.png), segmentadas manualmente de la imagen original (Original.png). También es posible procesar toda la imagen generada.

Una vez que se genera el modelo de clasificación, es posible utilizar el *Xtracor CNN.py* para la extracción de tablas.

*Es necesario actualizar las rutas de acceso a archivos. Las rutas que se encuentran definidas quedan como ejemplo para obtener un correcto funcionamiento de la herramienta.
