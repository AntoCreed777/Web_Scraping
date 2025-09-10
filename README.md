# Web Scraping y Análisis de Series de TV

Implementación de un sistema de scraping y análisis de datos sobre series de televisión de la pagina wed SensaCine, utilizando Python y pandas. El proyecto permite extraer información de la web, limpiar y fusionar datos, y realizar análisis exploratorio y visualizaciones.

## 👤 Autor

| Nombre | GitHub | Matrícula |
|--------|--------|-----------|
| Antonio Jesus Benavides Puentes | [@AntoCreed777](https://github.com/AntoCreed777) | 2023455954 |

## 📋 Tabla de Contenidos
- [Web Scraping y Análisis de Series de TV](#web-scraping-y-análisis-de-series-de-tv)
  - [👤 Autor](#-autor)
  - [📋 Tabla de Contenidos](#-tabla-de-contenidos)
  - [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
    - [Lenguaje de programación](#lenguaje-de-programación)
    - [Herramientas de desarrollo y control de versiones](#herramientas-de-desarrollo-y-control-de-versiones)
    - [Testing, Linting y Tipado](#testing-linting-y-tipado)
    - [Integración continua](#integración-continua)
  - [📋 Requisitos Previos](#-requisitos-previos)
  - [🚀 Cómo ejecutar y probar el proyecto](#-cómo-ejecutar-y-probar-el-proyecto)
    - [1. Instalar pdm (si no lo tienes)](#1-instalar-pdm-si-no-lo-tienes)
    - [2. Instalar dependencias](#2-instalar-dependencias)
    - [3. Ejecutar el scraping](#3-ejecutar-el-scraping)
    - [4. Ejecutar el análisis](#4-ejecutar-el-análisis)
    - [5. Linting y tipado](#5-linting-y-tipado)
    - [6. Fusionar archivos descargados](#6-fusionar-archivos-descargados)
  - [🗂️ Estructura del Proyecto](#️-estructura-del-proyecto)
  - [📚 Documentación del Código](#-documentación-del-código)
  - [📓 Jupyter Notebook](#-jupyter-notebook)
  - [📥 Descarga por rangos de páginas y fusión de datos](#-descarga-por-rangos-de-páginas-y-fusión-de-datos)
  - [📝 Convenciones y Herramientas de Formato](#-convenciones-y-herramientas-de-formato)

## 🛠️ Tecnologías Utilizadas

<div align="center">

### Lenguaje de programación
<img src="https://skillicons.dev/icons?i=python&perline=8" />

### Herramientas de desarrollo y control de versiones
<img src="https://skillicons.dev/icons?i=git,github,vscode&perline=5" />

### Testing, Linting y Tipado
<img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
<img src="https://img.shields.io/badge/flake8-4B8BBE?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/mypy-2A6DB2?style=for-the-badge&logo=python&logoColor=white" />

### Integración continua
<img src="https://skillicons.dev/icons?i=githubactions&perline=8" />

</div>

## ⚠️ Aviso Legal

Este repositorio fue creado con fines educativos como parte de una tarea universitaria.  
El código de scraping incluido está diseñado únicamente para propósitos de aprendizaje y no debe utilizarse para recopilar datos de forma masiva o sin consentimiento.

Por favor, asegúrate de respetar los Términos de Servicio del sitio web que se scrapea y revisa su archivo `robots.txt` antes de ejecutar este script.

El autor no se hace responsable del mal uso de este código.

## 📋 Requisitos Previos

- **Sistema operativo:** Linux, macOS, o Windows con WSL
- **Python 3.8+**
- **pdm** para gestión de dependencias y entornos

## 🚀 Cómo ejecutar y probar el proyecto

### 1. Instalar pdm (si no lo tienes)

```bash
pip install pdm
```

### 2. Instalar dependencias

```bash
git clone https://github.com/AntoCreed777/Web_Scraping
cd Web_Scraping
pdm install
```

### 3. Ejecutar el scraping

```bash
pdm run python src/scraping/main.py
```

### 4. Ejecutar el análisis

```bash
pdm run python src/analisis/main.py
```

### 5. Linting y tipado

Para revisar el estilo de código:

```bash
pdm run flake8 src/
```

Para revisar el tipado:

```bash
pdm run mypy src/
```

### 6. Fusionar archivos descargados

Para fusionar los archivos de series descargados por rangos de páginas y obtener un único archivo consolidado, ejecuta:

```bash
pdm run python src/scraping/fusion_pkl.py
```

> [!NOTE]
> La fusión de archivos descargados permite consolidar todos los datos obtenidos en diferentes rangos de páginas en un solo archivo. Esto es especialmente útil cuando la web bloquea descargas masivas, ya que puedes descargar por partes y luego unir todo para el análisis final. Consulta la sección [Descarga por rangos de páginas y fusión de datos](#-descarga-por-rangos-de-páginas-y-fusión-de-datos) para más detalles sobre cómo funciona este proceso.

## 🗂️ Estructura del Proyecto

```
Web_Scraping/
├── 2025_Tarea01_AD.ipynb
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   ├── scraping/
│   │   ├── main.py
│   │   ├── extraer_datos.py
│   │   ├── datos_serie.py
│   │   ├── fusion_pkl.py
│   │   └── ...
│   └── analisis/
│       ├── main.py
│       └── utilities.py
└── ...
```

## 📚 Documentación del Código

La documentación se encuentra en los docstrings de las funciones y clases principales. Para explorar la lógica y el flujo de datos, revisa los archivos en `src/scraping/` y `src/analisis/`.

## 📓 Jupyter Notebook

El proyecto incluye un Jupyter Notebook que sirve como documento de entrega y facilita la exploración, análisis y visualización de los datos obtenidos mediante scraping. En el notebook se explican los pasos principales del proceso, se muestran ejemplos de análisis y se interpretan los resultados. Es ideal para presentar el trabajo de forma ordenada y reproducible.

## 📥 Descarga por rangos de páginas y fusión de datos

Para evitar bloqueos al descargar grandes volúmenes de datos desde la web, el sistema permite realizar descargas parciales de rangos de páginas. Cada rango se guarda en un archivo independiente en formato `.pkl` (pickle de pandas), siguiendo el nombre `series_tv_<desde>_<hasta>.pkl`, donde `<desde>` y `<hasta>` corresponden al rango de páginas descargado.

Posteriormente, el proyecto incluye código para fusionar todos los archivos descargados en un único DataFrame, que se guarda en el archivo consolidado `series_tv.pkl`. Esta funcionalidad es útil para manejar grandes datasets y asegurar que no se pierda información por interrupciones en la conexión.

## 📝 Convenciones y Herramientas de Formato

- El código sigue el estándar PEP8 para estilo y buenas prácticas en Python.
- Se utiliza **black** para el formateo automático del código.
- Se utiliza **isort** para ordenar los imports de manera consistente.
- Se utiliza **pydocstyle** para verificar la calidad y formato de los docstrings.
- Se incluyen comentarios claros y docstrings en las funciones y clases principales para facilitar la comprensión y el mantenimiento.

---

<div align="center">

**Desarrollado con pasión por el análisis de datos y el scraping web**

📚 **Universidad:** Universidad de Concepción

🎓 **Curso:** Análisis de Datos

📋 **Código curso:** 501350-1

📅 **Semestre:** 2025-2

</div>
