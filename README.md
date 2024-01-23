# Introducción
Este repositorio corresponde a la biblioteca digital de Indesca. Este fue un proyecto interno realizado para el Centro de Información Técnica (CIT) de Indesca para la carga de informes creados en las investigaciones desarrolladas. Se desarrolló con Python y Django junto con HTMX. El motor de base de datos utilizado fue MySQL.

## :ledger: Índice

- [Información](#beginner-información)
- [Utilización](#zap-utilización)
  - [Instalación](#electric_plug-instalación)
- [Desarrollo](#wrench-desarrollo)
  - [Pre-Requisitos](#notebook-pre-requisitos)
  - [Ambiente de Desarrollo](#nut_and_bolt-ambiente-de-desarrollo)
  - [Estructura de Archivos](#file_folder-estructura-de-archivos)
  - [Datos de Deployment](#rocket-datos-de-deployment)  
- [Comunidad](#cherry_blossom-comunidad)
  - [Colaboración](#fire-colaboración)
  - [Branches](#cactus-branches)
- [FAQ](#question-faq)
- [Recursos](#page_facing_up-recursos)
- [Reconocimientos](#star2-reconocimientos)

##  :beginner: Información
Este proyecto corresponde a la biblioteca digital de Indesca. Fue realizado inicialmente en el mes de enero del año 2024 para la carga y consulta de informes técnicos generados en la investigación y libros contenidos en el CIT, junto con datos que facilitan la búsqueda de los mismos en el CIT.

Este proyecto fue hecho con apoyo del personal del CIT con data contenida en un software anterior realizado en páginas .asp y una base de datos en MS Access. La data fue migrada a una base de datos en MySQL donde se encuentra actualmente (23/01/2024) y está siendo cargada por el personal de CIT.

Hay dos módulos principales: Libros e Informes. Para acceder a los informes se requiere inicio de sesión, mientras que los libros puedes ser cualquiera. Solo superusuarios (personal de informática y CIT) pueden crear usuarios, crear, editar y eliminar libros e informes.

###  :electric_plug: Instalación
- Crear un ambiente virtual con `python -m venv ./env` y entrar al mismo.
- Instalar las dependencias con `pip install -r requirements.txt` en el ambiente virtual.
- Correr el comando `python manage.py migrate` de ser necesario.
- Correr el comando `python manage.py runserver` para iniciar el servidor de prueba.

###  :package: Comandos
Para ejecutar en ambiente de desarrollo:

```
$ python -m venv ./env
v pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

##  :wrench: Desarrollo

### :notebook: Pre-Requisitos
- Instalar **Python 3.9** o superior.
- Clonar el repositorio mediante la consola de git.
- Todas las dependencias contenidas en el archivo ``requirements.txt``

###  :nut_and_bolt: Ambiente de Desarrollo
El ambiente de desarrollo puede ser montado con lo mostrado en la sección de comandos. Se recomienda un mínimo de Windows 8 ya que Microsoft Windows Server 2012 es el ambiente de producción del mismo.

###  :file_folder: Estructura de Archivos
Aquí se encuentran los detalles de la estructura de archivos del proyecto.

| No | Carpeta / Archivo | Detalles 
|----|------------|-------|
| 1  | biblioteca_diital/ | Directorio principal del proyecto
| 2  | core/ | Aplicación central donde se encuentran tanto los modelos, vistas, migraciones, formularios y plantillas de la aplicación. Aquí se encuentran las vistas de CRUD de los informes y libros
| 3  | media/ | Directorio de los archivos (libros e informes) guardados por el usuario
| 4  | static/ | Archivos estáticos
| 5  | templates/ | Plantillas generales
| 6  | usuarios/ | Directorio del sistema de usuarios

Los archivos en formato .csv, .txt, .xlsx, .xls, .mdb pueden ser ignorados. Es data que se utilizó en su momento para migrarla a la base de datos.

### :rocket: Datos de Deployment
- Cambiar

## :cherry_blossom: Comunidad
Código cerrado y confidencial. Guiarse bajo los lineamientos aquí indicados.

 ###  :fire: Colaboración
Los únicos colaboradores del proyecto es el personal autorizado de Indesca. Por ahora, personal de Informática únicamente con apoyo de personal del CIT.

 ### :cactus: Branches

1. **`develop`** es la branch de desarrollo. Hacer todos los desarrollos partiendo de esta.

2. **`master`** es la branch principal. Solo código estable y testeado debe estar acá.

3. Toda branch adicional deberá de ser eliminada una vez sus cambios lleguen de develop a master.

**Pasos para crear nuevas branches**

1. Crear la branch localmente y actualizar la misma mediante push a esa branch al hacer cambios.
2. Una vez estén listos, hacer una pull request a **`develop`**.

## :question: FAQ
Colocar FAQs al finalizar proyecto.

## :star2: Reconocimientos
- **Fausto Rosales**: Ingeniero de Informática en Indesca
- **Biaggi Zambrano**: Ingeniero en Informática en Indesca
- **Diego Faria**: Ingeniero en Informática de Indesca (Programación)
- **Rosario Villalobos**: Directora del CIT
