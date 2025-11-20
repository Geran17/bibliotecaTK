# Interfaz del Usuario

La interfaz de usuario se diseñará para ser clara, funcional y eficiente, permitiendo al usuario gestionar su biblioteca con facilidad. Se propone un diseño de tres paneles principales, inspirado en gestores de correo y otras aplicaciones de organización.

## 1. Ventana Principal

La ventana principal estará dividida en las siguientes secciones:

### a. Barra de Herramientas Superior

Contendrá las acciones globales más importantes:

* **Botón "Importar Archivos"**: Abre el diálogo nativo para seleccionar uno o más archivos.
* **Botón "Importar Carpeta"**: Abre el diálogo para seleccionar una carpeta completa para su importación.
* **Barra de Búsqueda Global**: Un campo de texto para buscar en toda la biblioteca (nombres de archivo, metadatos, etiquetas, etc.).

### b. Panel Izquierdo (Navegación y Filtros)

Este panel es el centro de la organización y el filtrado.

* **Mi Biblioteca**: Un elemento principal que, al ser seleccionado, muestra todos los documentos activos en el panel central.
* **Colecciones**: Una vista de árbol o lista expandible que muestra todas las colecciones creadas por el usuario. Al seleccionar una colección, el panel central se filtra para mostrar solo los documentos de esa colección.
* **Etiquetas**: Una lista o "nube de etiquetas" con todas las etiquetas usadas. Al hacer clic en una etiqueta, se filtran los documentos que la contienen.
* **Papelera**: Muestra los documentos que han sido eliminados (soft delete). Desde aquí, el usuario podrá restaurarlos o eliminarlos permanentemente.

### c. Panel Central (Lista de Documentos)

Muestra la lista de documentos según el filtro seleccionado en el panel izquierdo.
* **Vista de Tabla**: Los documentos se listarán en una tabla con columnas personalizables como:
    *   `Nombre del Documento`
    *   `Autor(es)`
    *   `Año de Publicación`
    *   `Fecha de Adición`
*   **Selección Múltiple**: El usuario podrá seleccionar uno o varios documentos para realizar acciones en lote (ej. eliminar, añadir a una colección).
*   **Menú Contextual (Clic Derecho)**: Al hacer clic derecho sobre un documento, aparecerá un menú con acciones rápidas:
    *   `Abrir archivo`
    *   `Renombrar`
    *   `Eliminar (Mover a la papelera)`
    *   `Añadir a colección...`
    *   `Gestionar etiquetas...`

### d. Panel Derecho (Detalles y Metadatos)
Este panel es contextual y muestra la información del documento seleccionado en el panel central. Estará organizado en pestañas para mantener la claridad.
*   **Pestaña "Información"**: Muestra y permite editar los metadatos principales (nombre, autor, editorial, año, resumen, etc.).
*   **Pestaña "Etiquetas"**: Muestra las etiquetas asociadas al documento. Permite añadir nuevas etiquetas desde una lista de existentes o crear una nueva, y eliminar las asociaciones actuales.
*   **Pestaña "Notas"**: Un área de texto simple donde el usuario puede escribir y guardar anotaciones personales sobre el documento.

## 2. Flujo de Importación (Staging Area)

Para dar más control al usuario, el proceso de importación no será inmediato. Tras seleccionar los archivos, se abrirá una ventana modal de "Preparación".

*   **Lista de Archivos a Importar**: Una tabla mostrará los archivos seleccionados.
*   **Columnas**:
    *   `Nombre Original`
    *   `Estado` (ej. "Nuevo", "Duplicado - se omitirá").
    *   `Nombre en Biblioteca` (campo editable para que el usuario pueda renombrar antes de importar).
*   **Acciones**:
    *   Casillas de verificación para incluir/excluir archivos de la importación.
    *   Un botón **"Importar Seleccionados"** para iniciar el proceso de copia y registro en la BD.
    *   Un botón **"Cancelar"**.

Este diseño modular y centrado en el flujo de trabajo del usuario asegura que todas las funcionalidades lógicas descritas en `logica_app.md` tengan un lugar coherente y accesible en la interfaz.
