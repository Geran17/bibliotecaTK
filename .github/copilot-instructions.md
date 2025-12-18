# Guías de Codificación AI para BibliotecaTK

## Descripción General de la Arquitectura
BibliotecaTK es una aplicación de escritorio en Python para la gestión de documentos usando Tkinter. Sigue el patrón MVC:
- **Vistas** (`src/views/`): Interfaz de usuario Tkinter con temas ttkbootstrap, organizada en frames (menú, central, inferior)
- **Controladores** (`src/models/controllers/`): Lógica de negocio, manejan eventos de UI, coordinan DAOs
- **Modelos** (`src/models/`): Capa de datos con DAOs (acceso SQLite), DTOs (transferencia de datos), Entidades (objetos de dominio)

Flujo de datos: UI → Controlador → DAO → Base de datos SQLite. Los controladores actualizan la UI directamente.

## Patrones Clave
- **DAOs Thread-Safe**: Todos los DAOs heredan de la clase base `DAO` usando context managers para conexiones. Usa el context manager `_get_connection()` para operaciones de BD.
- **Claves Foráneas Habilitadas**: Siempre `PRAGMA foreign_keys = ON` en conexiones.
- **Row Factory**: Usa `sqlite3.Row` para acceso dict-like a resultados de consultas.
- **Directorios XDG**: Config en `~/.config/bibliotecaTK`, datos en `~/.local/share/bibliotecaTK`.
- **Procesamiento PDF**: Usa `fitz` (PyMuPDF) para extracción de texto, `pdf2image` para miniaturas.

## Flujos de Trabajo
- **Ejecutar App**: `python src/main.py` (crea BD si es necesario, inicializa directorios)
- **Pruebas**: `pytest` (usa `pythonpath=src`, fixtures de BD en memoria)
- **Dependencias**: Usa Pipenv (`pipenv install`, `pipenv run python src/main.py`)

## Convenciones
- **Imports**: Imports relativos dentro de src (ej. `from models.daos.documento_dao import DocumentoDAO`)
- **Nombres**: Nombres de métodos en español (ej. `crear_tabla`, `insertar`), pero entidades en inglés
- **Manejo de Errores**: Imprimir excepciones en main, rollback en errores de BD
- **Actualizaciones UI**: Los controladores reciben widgets de UI (labels, progress bars) y los actualizan directamente
- **Iconos**: Usa emojis Unicode para indicadores de estado (⭐ para favoritos, ❗ para archivos faltantes)

## Puntos de Integración
- **ExifTool**: Via `pyexiftool` para extracción de metadatos
- **Operaciones de Archivos**: `send2trash` para eliminación segura
- **Solicitudes HTTP**: `requests` para datos externos (si es necesario)

## Ejemplos
- Agregar nuevo DAO: Extender `DAO`, implementar `crear_tabla()`, usar `_get_connection()` para consultas
- Componente UI: Crear frame en `views/frames/`, integrar en `AppTK.crear_widgets()`
- Probar DAO: Usar fixture `documento_dao_en_memoria`, afirmar estado de BD</content>
<parameter name="filePath">/home/geran/MEGA/Workspaces/proyectos/bibliotecaTK/.github/copilot-instructions.md