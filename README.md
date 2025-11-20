# BibliotecaTK

BibliotecaTK es una aplicación en Python para la gestión de documentos electronicos. Ya sea
libros u otros tipos de documentos que se puedan guardar en la memoria. No se es una aplicacion
multi-usuario, ya que funcion principar es la de organizar y detectar documentos duplicados mediante el hash de cada archivo.
Una de sus funciones principales es la registrar los contenidos de los documentos, para que el
usuario pueda buscar contenidos especificos dentro los diferentes documentos.
Ofrece funcionalidades para agregar, ver, actualizar y eliminar documentos de la biblioteca.

## Características

- **Gestión de Documentos**: Agregar nuevos documentos, ver la lista completa,
    actualizar detalles o eliminar documentos de la biblioteca.
- **Búsqueda y Filtros**: Buscar fácilmente documentos o usuarios según
    distintos criterios.
- **Interfaz Intuitiva**: Una interfaz gráfica amigable construida con
    Tkinter, que facilita la navegación y la interacción.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal del proyecto.
- **Tkinter**: Para crear la interfaz gráfica de usuario.
- **SQLite3**: Para la gestión de la base de datos que almacena
    información de libros, usuarios y préstamos.

## Instalación

Para tener una copia local funcionando, sigue estos pasos sencillos.

### Requisitos Previos

- Tener Python 3.x instalado en tu sistema.

### Pasos

1. **Clona el repositorio:**

    ``` bash
    git clone https://github.com/your-username/BibliotecaTK.git
    cd BibliotecaTK
    ```

2. **Instala las dependencias (si las hubiera, aunque este proyecto usa
    principalmente módulos incorporados):**

    ``` bash
    # No se requieren dependencias externas para una app básica con Tkinter/SQLite3.
    # Si agregas alguna, inclúyela aquí junto con las instrucciones de instalación.
    ```

3. **Ejecuta la aplicación:**

    ``` bash
    python main.py
    ```

## Uso

Una vez que la aplicación esté en ejecución, puedes:

- Navegar por las distintas pestañas.
- Usar los botones "Agregar", "Editar" y "Eliminar" para gestionar
    registros.
- Utilizar las barras de búsqueda para encontrar elementos
    específicos.

## Estructura del Proyecto
