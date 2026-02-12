# BibliotecaTK

BibliotecaTK es una aplicación de escritorio en **Python** para la gestión integral de documentos digitales. Permite organizar, catalogar y buscar documentos de forma eficiente mediante una interfaz gráfica intuitiva.

## 🎯 Descripción

Una aplicación moderna y funcional para la gestión de bibliotecas personales o pequeñas colecciones de documentos. Su función principal es organizar documentos, detectar duplicados mediante hash SHA-256, registrar metadatos y permitir búsquedas avanzadas de contenido dentro de los documentos.

### Características Principales

- **📚 Gestión de Documentos**: Importar, renombrar, copiar, mover y eliminar documentos
- **🔍 Búsqueda Avanzada**: Buscar contenido dentro de documentos PDF y EPUB
- **🏷️ Catalogación**: Agregar información bibliográfica, categorías, etiquetas y palabras clave
- **📊 Detección de Duplicados**: Identificar archivos duplicados mediante hash SHA-256
- **📑 Extracción de Contenido**: Registrar capítulos y secciones de documentos
- **⭐ Favoritos**: Marcar documentos como favoritos para acceso rápido
- **🎨 Interfaz Moderna**: Interfaz gráfica con tema ttkbootstrap, responsive y fácil de usar
- **🔒 Almacenamiento Seguro**: Base de datos SQLite con validación de integridad
- **⚙️ Configuración Flexible**: Configurar ubicación de biblioteca y preferencias de usuario

## 🛠️ Tecnologías Utilizadas

- **Python 3.12+**: Lenguaje de programación
- **Tkinter + ttkbootstrap**: Interfaz gráfica de usuario moderna
- **SQLite3**: Base de datos relacional
- **PyMuPDF (fitz)**: Procesamiento de archivos PDF
- **pdf2image**: Generación de miniaturas de PDF
- **send2trash**: Eliminación segura de archivos
- **exiftool**: Extracción de metadatos

## 📋 Requisitos

- Python 3.12 o superior
- Pipenv (gestor de dependencias)
- SQLite3 (incluido en Python)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/bibliotecaTK.git
cd bibliotecaTK
```

### 2. Instalar Pipenv (si no lo tienes)

```bash
pip install pipenv
```

### 3. Instalar dependencias

```bash
pipenv install
```

### 4. Ejecutar la aplicación

Modo Tkinter:

```bash
pipenv run python src/main.py
```

Tambien puedes definirlo con variable de entorno:

```bash
BIBLIOTECA_UI=tkinter pipenv run python src/main.py
```

## 📁 Estructura del Proyecto

```
bibliotecaTK/
├── src/
│   ├── main.py                    # Punto de entrada
│   ├── models/
│   │   ├── controllers/           # Lógica de negocio
│   │   │   ├── controlar_documento_seleccionado.py
│   │   │   ├── controlar_importacion_documento.py
│   │   │   ├── controlar_seleccion_documentos.py
│   │   │   ├── controlar_todos.py
│   │   │   ├── controlar_existentes.py
│   │   │   └── ... (más controladores)
│   │   ├── daos/                  # Acceso a datos
│   │   │   ├── dao.py
│   │   │   ├── documento_dao.py
│   │   │   ├── categoria_dao.py
│   │   │   └── ... (más DAOs)
│   │   ├── dtos/                  # Objetos de transferencia
│   │   └── entities/              # Entidades de dominio
│   │       ├── documento.py
│   │       ├── categoria.py
│   │       └── ... (más entidades)
│   ├── views/
│   │   ├── tk/                   # Backend Tkinter
│   │   ├── apps/factory.py       # Selección de backend visual
│   │   ├── frames/               # Componentes de UI
│   │   │   ├── frame_importar_documento.py
│   │   │   ├── frame_administrar_documentos.py
│   │   │   └── ... (más frames)
│   │   └── dialogs/              # Diálogos modales
│   └── utilities/                # Funciones auxiliares
│       ├── configuracion.py
│       ├── auxiliar.py
│       └── fileINI.py
├── tests/                        # Pruebas unitarias
├── Pipfile                       # Dependencias del proyecto
├── pytest.ini                    # Configuración de pytest
└── README.md
```

## 🎮 Uso

### Importar Documentos

1. Ir a **Importar → Seleccionar archivos**
2. Elegir documentos PDF, EPUB o MOBI
3. Opción de copiar o mover a la biblioteca
4. Los documentos se registran en la BD automáticamente

### Administrar Documentos

1. Ir a **Administración**
2. Seleccionar un documento haciendo doble clic
3. Usar los botones para:
   - **Abrir**: Abrir en aplicación asociada
   - **Renombrar**: Cambiar nombre del documento
   - **Copiar**: Copiar a ubicación externa
   - **Mover**: Mover fuera de la biblioteca
   - **Papelera**: Enviar a papelera
   - **Eliminar**: Eliminar permanentemente

### Buscar Contenido

1. Ir a **Búsqueda**
2. Escribir término de búsqueda
3. Los resultados muestran documentos y páginas donde aparece

### Ver Favoritos

1. Ir a **Favoritos**
2. Ver documentos marcados como favoritos
3. Hacer clic para abrir

## 🔧 Configuración

Los datos de configuración se almacenan en:

- **Linux/Mac**: `~/.config/bibliotecaTK/`
- **Windows**: `%APPDATA%/bibliotecaTK/`

La base de datos se almacena en:

- **Linux/Mac**: `~/.local/share/bibliotecaTK/`
- **Windows**: `%LOCALAPPDATA%/bibliotecaTK/`

## 🏗️ Arquitectura

BibliotecaTK sigue el patrón **MVC** (Modelo-Vista-Controlador):

- **Vistas** (`src/views/`): Interfaz gráfica en Tkinter
- **Controladores** (`src/models/controllers/`): Lógica de negocio y manejo de eventos
- **Modelos** (`src/models/`): DAOs, DTOs y Entidades para acceso a datos
- **Base de Datos**: SQLite con validación de integridad referencial

### Flujo de Datos

```
UI Event → Controller → DAO → SQLite Database
    ↓
   UI Update
```

## 📊 Mejoras Recientes

### Calidad del Código

✅ Logging completo en todos los controladores
✅ Type hints para mejor análisis estático
✅ Docstrings exhaustivos en métodos
✅ Error handling robusto con try-except
✅ Métodos privados bien organizados

### Interfaz de Usuario

✅ Emojis Unicode para feedback visual
✅ Colores temáticos (info, danger, warning, success)
✅ Interfaz responsiva con ttkbootstrap
✅ Tabs (Notebook) para mejor organización
✅ Barra de progreso para operaciones largas

### Funcionalidades

✅ Sincronización correcta de datos después de renombrar
✅ Operaciones en masa (copiar, mover, eliminar, papelera)
✅ Detección de archivos existentes en biblioteca
✅ Generación automática de portadas y miniaturas
✅ Búsqueda avanzada de contenido

## 🧪 Pruebas

Ejecutar pruebas unitarias:

```bash
pipenv run pytest
```

Pruebas disponibles:

- Tests de DAOs (documento, categoría, colección, etc.)
- Tests de DTOs (validación de datos)
- Tests de Entidades (lógica de negocio)
- Tests de conexión SQLite

## 🐛 Problemas Conocidos

Ninguno en la versión actual.

## 📝 Convenciones de Código

- **Nombres en español**: Métodos y variables en español
- **Nombres en inglés**: Entidades y clases en inglés
- **Type hints**: Todos los métodos públicos con type hints
- **Docstrings**: Formato Google Style
- **Logging**: Usar `logger.info()`, `logger.debug()`, `logger.error()`

## 🤝 Contribuir

Se aceptan pull requests para mejoras y corrección de bugs.

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para detalles.

## 👤 Autor

**Geran** - Desarrollo y mantenimiento

## 🙏 Agradecimientos

- ttkbootstrap por el tema moderno
- PyMuPDF por procesamiento de PDFs
- La comunidad de Python por las herramientas
