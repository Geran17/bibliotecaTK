# Lógica de la Aplicación

## Seleccion de Documentos

Mediante el diálogo nativo del sistema operativo, el usuario selecciona los archivos que serán copiados a la biblioteca local. El usuario también deberá seleccionar la ubicación (directorio raíz) de dicha biblioteca.

Durante el proceso de importación, la aplicación realizará las siguientes validaciones:

* **Detección de Duplicados:** Se calculará el hash de cada archivo (ej. `SHA-256`) para compararlo con los hashes de los archivos ya existentes en la base de datos de la biblioteca.
* **Omisión de Archivos Existentes:** Los archivos cuyo hash ya se encuentre en la base de datos no serán copiados, para evitar duplicados.

Opcionalmente, la interfaz podría ofrecer funcionalidades de gestión de archivos en una vista de "preparación" (staging area) antes de la copia definitiva, como: renombrar, mover a la papelera o eliminar de la selección.

## Sistema de copiado

En la biblioteca local se generarán sub-carpetas para organizar los archivos y evitar tener un número excesivo de ellos en un solo directorio. La estructura se basará en el `id` del archivo en la base de datos.

* **Estructura de Directorios:** Se crearán carpetas numéricas (`000`, `001`, `002`, ...). Cada carpeta contendrá un máximo de 1000 archivos. La carpeta de destino para un archivo se determinará por la operación `floor(id / 1000)`.
* *Ejemplo:* El archivo con `id=500` irá a la carpeta `000`. El archivo con `id=1250` irá a la carpeta `001`.
* **Nomenclatura de Archivos:** Los archivos se renombrarán al ser copiados para incluir su `id` único, siguiendo el formato: `{id}_{nombre_original}.{extension}`.

## Flujo de Trabajo de Importación

Para cada archivo seleccionado por el usuario, la aplicación seguirá estos pasos:

1. **Calcular Hash:** Se calcula el hash del archivo de origen.
2. **Verificar Duplicado:** Se consulta la base de datos para ver si el hash ya existe. Si es así, se ignora el archivo y se continúa con el siguiente.
3. **Insertar en BD:** Si el archivo es nuevo, se inserta su metadata (nombre original, hash, etc.) en la base de datos.
4. **Obtener ID:** Se recupera el `id` autoincremental generado por la base de datos para el nuevo registro.
5. **Determinar Ruta:** Se calcula la carpeta de destino (ej: `001`) y el nuevo nombre del archivo (ej: `1250_mi_documento.pdf`).
6. **Copiar Archivo:** Se copia el archivo de origen a su nueva ruta y con su nuevo nombre dentro de la biblioteca local.

## Implementacion de la Biblioteca Local

Una vez que los archivos están importados en la biblioteca y registrados en la base de datos, la aplicación debe ofrecer funcionalidades para su gestión y organización. Estas operaciones se dividen en dos categorías principales:

### 1. Gestión de Archivos y Metadatos

Estas operaciones modifican directamente los archivos físicos o su registro principal en la base de datos. Es crucial que estas acciones se realicen a través de la aplicación para mantener la consistencia entre el sistema de archivos y la base de datos.

* **Renombrar:**
* **Acción del Usuario:** El usuario edita el nombre de un documento en la interfaz.
* **Lógica de la App:**
        1.  Actualiza el campo `nombre` en la tabla de documentos de la base de datos.
        2.  Renombra el archivo físico en el disco, manteniendo el `id` como prefijo. (Ej: `1250_mi_documento.pdf` pasa a ser `1250_documento_actualizado.pdf`).

* **Eliminar (Mover a la Papelera):**
* **Acción del Usuario:** El usuario elimina un documento.
* **Lógica de la App (Soft Delete):**
        1.  En la base de datos, se actualiza el registro del documento para marcarlo como inactivo (`esta_activo = False`).
        2.  El archivo físico se mueve a un directorio especial dentro de la biblioteca (ej: `biblioteca/.trash/`) para permitir su futura restauración.
        3.  La aplicación debe ofrecer una vista de "Papelera" para restaurar o eliminar permanentemente estos archivos.

### 2. Organización Lógica y Enriquecimiento de Datos

Estas operaciones no alteran el archivo físico, sino que añaden capas de información y contexto en la base de datos para facilitar la búsqueda, el filtrado y la clasificación.

* **Etiquetas / Palabras Clave:** El usuario podrá asociar múltiples etiquetas a un documento (ej: "python", "desarrollo-web", "tutorial"). Esto requerirá una tabla de relación muchos a muchos (`documentos_etiquetas`).
* **Colecciones / Grupos:** Permitir al usuario agrupar documentos en colecciones lógicas (ej: "Libros de Programación", "Artículos Científicos 2023"). Similar a las etiquetas, esto se puede implementar con una tabla de relación.
* **Metadatos Bibliográficos:** El usuario podrá añadir información detallada como autor, editorial, año de publicación, resumen, etc. Estos campos se añadirían a la tabla de documentos o a una tabla relacionada.
* **Comentarios y Anotaciones:** Permitir al usuario agregar notas personales o comentarios a cada documento.
