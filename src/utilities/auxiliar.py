from PIL import Image, ImageTk
from pdf2image import convert_from_path
import exiftool
import subprocess
import fitz
import requests
from datetime import datetime as dt
from pathlib import Path
from os import rename, mkdir
from os.path import exists, isfile, isdir, join
from shutil import copy2, move
from send2trash import send2trash  # type: ignore
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


def obtener_datos_libros(isbn: str) -> Dict[str, Any]:

    # Limpiar el ISBN (opcional pero recomendado)
    isbn_limpio = isbn.replace('-', '').replace(' ', '').strip()

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_limpio}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('totalItems', 0) == 0:
            return None

        # Tomar el primer resultado
        libro = data['items'][0]['volumeInfo']

        # Extraer ISBN (preferir ISBN-13)
        isbn_final = isbn
        if 'industryIdentifiers' in libro:
            for identifier in libro['industryIdentifiers']:
                if identifier['type'] == 'ISBN_13':
                    isbn_final = identifier['identifier']
                    break

        # Extraer año de publicación
        ano = None
        if 'publishedDate' in libro:
            ano = int(libro['publishedDate'].split('-')[0])

        # Preparar datos
        datos = {
            'titulo': libro.get('title', ''),
            'autores': ', '.join(libro.get('authors', [])) if libro.get('authors') else None,
            'ano_publicacion': ano,
            'editorial': libro.get('publisher'),
            'numero_edicion': libro.get('edition'),
            'idioma': libro.get('language'),
            'numero_paginas': libro.get('pageCount'),
        }

        return datos

    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None
    return data


def eliminar_archivo(ruta_destino: str) -> bool:
    """
    Elimina un archivo del sistema de archivos.

    Verifica si la ruta de destino existe y es un archivo antes de intentar eliminarlo.

    Args:
        ruta_destino (str): La ruta completa del archivo a eliminar.

    Returns:
        bool: True si el archivo fue eliminado exitosamente, False en caso contrario."""
    if exists(ruta_destino) and isfile(ruta_destino):
        try:
            archivo = Path(ruta_destino)
            archivo.unlink()
            return True
        except Exception as e:
            print("Error al tratar de eliminar el archivo: {e}")
            return False
    else:
        print(f"La ruta de destino no existe o no es un archivo: {ruta_destino}")
        return False


def desglosar_ruta_documento(ruta_documento: str) -> Dict[str, Any]:
    if exists(ruta_documento) and isfile(ruta_documento):
        archivo = Path(ruta_documento)
        pos = archivo.name.find("_")
        return {
            'ruta_completa': str(archivo),
            'ruta_padre': str(archivo.parent),
            'id_documento': archivo.name[:pos],
            'nombre_sin_id': archivo.name[pos + 1 :],
        }


def generar_ruta_documento(ruta_biblioteca: str, nombre_documento: str, id_documento: int) -> str:
    """
    Genera una ruta del documento a la biblioteca, para que el usuario para operar sobre el archivo
    Esta función crea subdirectorios basados en el ID del documento para organizar los archivos.

    Args:
        ruta_biblioteca (str): La ruta base del directorio donde se almacenan los documentos de la biblioteca.

        nombre_documento (str): El nombre original del archivo, incluyendo su extensión (ej. "documento.pdf").

        id_documento (int): es el id del documento que genero el registro en la base de datos

    Returns:
        str: retorna la ruta del documento
    """
    if exists(ruta_biblioteca) and isdir(ruta_biblioteca):
        # Si existe la ruta a la biblioteca y es un directorio, entonces
        # concatenamos con el posible ubicacion del subdirecectorio
        ruta_subdirectorio = crear_directorio_id_documento(
            ruta_destino=ruta_biblioteca, id_documento=id_documento
        )
        if exists(ruta_subdirectorio):
            # Si existe el subdirectorio concanetamos con el nombre nombre
            nuevo_nombre = f"{id_documento}_{nombre_documento}"
            return join(ruta_subdirectorio, nuevo_nombre)
        else:
            print(f"No existe la ruta del subdirectorio: {ruta_subdirectorio}")
            return None
    else:
        print(f"No existe la ruta a la biblioteca o no es un directorio: {ruta_biblioteca}")
        return None


def crear_directorio(ruta_destino: str) -> bool:
    """
    Crea un directorio en la ruta especificada.

    Args:
        ruta_destino (str): La ruta completa del directorio a crear.

    Returns:
        bool: True si el directorio fue creado exitosamente, False en caso contrario.
    """
    try:
        mkdir(ruta_destino)
        return True
    except Exception as e:
        print(f"Error al crear el directorio: {e}")
        return False


def crear_directorio_id_documento(ruta_destino: str, id_documento: int) -> str:
    """
    Crea un subdirectorio basado en el ID de un documento para organizar los archivos.

    Los subdirectorios se nombran con el formato '000', '001', etc.,
    donde cada uno contiene hasta 1000 documentos. La carpeta se determina
    por `floor(id_documento / 1000)`.

    Args:
        ruta_destino (str): La ruta base donde se crearán los subdirectorios.
        id_documento (int): El ID único del documento.

    Returns:
        str: La ruta completa al subdirectorio creado o existente,
             o None si la `ruta_destino` no es un directorio válido o no existe.
    """
    # verficamos que la ruta de destino sea un directorio y exista
    # este directorio sera la ubicacion para los documentos guardados por el usuario
    if isdir(ruta_destino) and exists(ruta_destino):
        sub_directorio = str(id_documento // 1000).zfill(3)
        # hacemos una union y verificamos si existe la carpeta dentro de la ruta de destino
        if not exists(join(ruta_destino, sub_directorio)):
            crear_directorio(join(ruta_destino, sub_directorio))
            return join(ruta_destino, sub_directorio)
        else:
            return join(ruta_destino, sub_directorio)
    else:
        print(f"La ruta de destino no es un directorio: {ruta_destino}")
        return None


def renombrar_archivo(ruta_origen: str, ruta_destino: str) -> bool:
    """
    Renombra un archivo de una ruta a otra.

    Args:
        ruta_origen (str): La ruta completa del archivo original.
        ruta_destino (str): La nueva ruta completa (incluyendo el nuevo nombre) para el archivo.

    Returns:
        bool: True si el archivo fue renombrado exitosamente, False en caso contrario.
    """
    if exists(ruta_origen):
        try:
            rename(ruta_origen, ruta_destino)
            return True
        except Exception as e:
            print(f"Error al renombrar el archivo: {e}")
            return False
    else:
        print(f"No existe el archivo en ruta de origen: {ruta_origen}")
        return False


def copiar_archivo(ruta_origen: str, ruta_destino: str) -> bool:
    """
    Copia un archivo de una ruta a otra.

    Args:
        ruta_origen (str): La ruta completa del archivo a copiar.
        ruta_destino (str): La ruta completa de destino para la copia del archivo.

    Returns:
        bool: True si el archivo fue copiado exitosamente, False en caso contrario.
    """
    if exists(ruta_origen):
        try:
            copy2(ruta_origen, ruta_destino)
            return True
        except Exception as e:
            print(f"Error al copiar el archivo: {e}")
            return False
    else:
        print(f"No existe el archivo en ruta de origen: {ruta_origen}")
        return False


def mover_archivo(ruta_origen: str, ruta_destino: str) -> bool:
    """
    Mueve un archivo de una ubicación a otra.

    Args:
        ruta_origen (str): La ruta completa del archivo a mover.
        ruta_destino (str): La ruta completa de destino para el archivo.

    Returns:
        bool: True si el archivo fue movido exitosamente, False en caso contrario.
    """
    if exists(ruta_origen):
        try:
            move(ruta_origen, ruta_destino)
            return True
        except Exception as e:
            print(f"Error al tratar de mover el archivo: {e}")
            return False
    else:
        print(f"No existe el archivo en ruta de origen: {ruta_origen}")
        return False


def papelera_archivo(ruta_origen: str) -> bool:
    """
    Mueve un archivo a la papelera de reciclaje del sistema operativo.

    Args:
        ruta_origen (str): La ruta completa del archivo a enviar a la papelera.

    Returns:
        bool: True si el archivo fue enviado a la papelera exitosamente, False en caso contrario.
    """
    if exists(ruta_origen):
        try:
            send2trash(ruta_origen)
            return True
        except Exception as e:
            print(f"Error al tratar de mover el archivo a la papelera del sistema: {e}")
            return False
    else:
        print(f"No existe el archivo en ruta de origen: {ruta_origen}")
        return False


def obtener_metadatos(ruta_origen: str) -> Dict:
    """
    Obtiene los metadatos de un archivo utilizando exiftool.

    Args:
        ruta_origen (str): La ruta completa del archivo del cual se extraerán los metadatos.
                           Se espera que exiftool esté instalado y accesible en el PATH.

    Returns:
        Dict: Un diccionario con los metadatos del archivo. Retorna un diccionario vacío
              si el archivo no existe o si ocurre un error durante la extracción.
    """
    if exists(ruta_origen):
        try:
            with exiftool.ExifToolHelper() as exif:
                metadatos = exif.get_metadata(ruta_origen)
                return metadatos[0]
        except Exception as e:
            print(f"Error al obtener los metadatos del archivo: {e}")
            return {}
    else:
        print(f"No existe el archivo en la ruta de origen: {ruta_origen}")
        return {}


def editar_metadato(clave: str, valor: str, path_file: str) -> bool:
    """
    Edita un metadato específico de un archivo usando ExifTool.

    Args:
        clave (str): La clave del metadato a editar (ej: "PDF:Title").
        valor (str): El nuevo valor para el metadato.
        path_file (str): La ruta completa del archivo a modificar.

    Returns:
        bool: True si la operación fue exitosa, False en caso contrario.
    """
    if exists(path_file):
        comando = ['exiftool', f'-{clave}={valor}', '-overwrite_original', path_file]
        try:
            # Ejecutar el comando
            subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8')
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar ExifTool: {e}")
            print(f"Salida de error: {e.stderr}")
            return False
        except FileNotFoundError:
            print("Error: ExifTool no está instalado o no está en el PATH del sistema")
            # Podrías mostrar un messagebox aquí si lo deseas.
            return False
    else:
        raise FileExistsError("No existe el archivo")


def abrir_archivo(ruta_origen: str, pagina: Optional[int] = None):
    """
    Abre un archivo con la aplicación predeterminada del sistema de forma multiplataforma.

    Args:
            ruta_origen (str): La ruta completa del archivo a abrir.
    """
    if not exists(ruta_origen):
        print(f"No existe el archivo en la ruta de origen: {ruta_origen}")
        return

    try:
        import os
        import sys

        if sys.platform == "win32":
            os.startfile(ruta_origen)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", ruta_origen], check=True)
        else:  # Linux y otros Unix-like
            # Intentar con diferentes comandos en orden de preferencia
            # kioclient5 es el preferido en KDE para evitar problemas.
            for cmd in ["kioclient5 exec", "xdg-open", "gvfs-open", "gnome-open"]:
                if subprocess.run(["which", cmd], capture_output=True).returncode == 0:
                    subprocess.run([cmd, ruta_origen], check=True)
                    return
            print("No se encontró un comando para abrir archivos (xdg-open, gvfs-open, etc.).")
    except Exception as e:
        print(f"Error al tratar de abrir el archivo '{ruta_origen}': {e}")


def abrir_documento_desde_biblioteca(
    id_documento: int,
    nombre_documento: str,
    extension_documento: str,
    pagina: Optional[int] = None,
    ruta_biblioteca: Optional[str] = None,
) -> tuple[bool, str]:
    """
    Abre un documento de biblioteca copiándolo primero al directorio temporal.

    Returns:
        tuple[bool, str]: (ok, mensaje_error). Si ok=True, mensaje_error es cadena vacía.
    """
    if not ruta_biblioteca:
        from models.controllers.configuracion_controller import ConfiguracionController

        ruta_biblioteca = ConfiguracionController().obtener_ubicacion_biblioteca()

    if not ruta_biblioteca or not exists(ruta_biblioteca):
        return False, "La ubicación de la biblioteca no está configurada o no existe."

    nombre_archivo = f"{nombre_documento}.{extension_documento}"
    ruta_origen = generar_ruta_documento(
        ruta_biblioteca=ruta_biblioteca,
        id_documento=id_documento,
        nombre_documento=nombre_archivo,
    )

    if not ruta_origen or not exists(ruta_origen):
        return False, f"El archivo no se encontró en la biblioteca:\n{ruta_origen}"

    from utilities.configuracion import DIRECTORIO_TEMPORAL

    ruta_destino_temporal = join(DIRECTORIO_TEMPORAL, nombre_archivo)
    try:
        copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino_temporal)
        abrir_archivo(ruta_origen=ruta_destino_temporal) if pagina is None else abrir_archivo(
            ruta_origen=ruta_destino_temporal
        )
        return True, ""
    except Exception as ex:
        logger.exception("Error al abrir documento desde biblioteca")
        return False, f"No se pudo abrir el documento: {ex}"


def obtener_datos_documento(ruta_origen: str) -> Dict[str, Any]:
    """
    Obtiene información básica de un archivo a partir de su ruta.

    Utiliza `pathlib.Path` para extraer detalles como el nombre, la extensión,
    el tamaño y la ruta del directorio padre.

    Args:
        ruta_origen (str): La ruta completa del archivo.

    Returns:
        Dict[str, Any]: Un diccionario con los datos del archivo si este existe
                        y es un archivo válido. Las claves incluyen:
                        'ruta_completa', 'nombre_con_extension',
                        'nombre_sin_extension', 'extension', 'tamano_bytes',
                        'ruta_padre'. Retorna un diccionario vacío si la ruta
                        no es un archivo válido.
    """
    if exists(ruta_origen) and isfile(ruta_origen):
        archivo = Path(ruta_origen)
        return {
            'ruta_completa': str(archivo),
            'nombre_con_extension': archivo.name,
            'nombre_sin_extension': archivo.stem,
            'extension': archivo.suffix[1:],
            'tamano_bytes': archivo.stat().st_size,
            'ruta_padre': str(archivo.parent),
        }

    else:
        print(f"La ruta de origen de existe o no es un archivo: {ruta_origen}")
        return {}


def hash_sha256(archivo: str) -> Optional[str]:
    """
    Calcula el hash SHA-256 de un archivo utilizando el comando `sha256sum`.

    Esta función depende de que el comando `sha256sum` esté disponible en el
    entorno del sistema (común en sistemas tipo Unix/Linux).

    Args:
        archivo (str): La ruta completa del archivo para calcular el hash.

    Returns:
        Optional[str]: El hash SHA-256 como una cadena de texto si tiene éxito,
                       o None si ocurre un error.
    """
    try:
        resultado = subprocess.run(
            ['sha256sum', archivo], capture_output=True, text=True, check=True
        )
        # Extraer solo el hash (sin el nombre del archivo)
        hash_resultado = resultado.stdout.split()[0]
        return hash_resultado
    except subprocess.CalledProcessError as e:
        print(f"Error al calcular hash: {e}")
        return None


def pdf_primera_pagina_a_png(pdf_path, output_path, dpi=72, thumbnail_size=(150, 200)):
    """
    Extrae la primera página de un PDF y la guarda como PNG miniatura.

    Args:
        pdf_path (str): Ruta al archivo PDF
        output_path (str): Ruta donde guardar el PNG
        dpi (int): Resolución (72 para miniaturas, 150 para calidad)
        thumbnail_size (tuple): (ancho, alto) para miniatura

    Returns:
        bool: True si fue exitoso, False en caso contrario
    """
    try:
        doc = fitz.open(pdf_path)
        pagina = doc[0]

        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = pagina.get_pixmap(matrix=mat)

        # Guardar temporalmente
        pix.save(output_path)

        # Redimensionar para miniatura
        img = Image.open(output_path)
        img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        img.save(output_path, optimize=True, quality=85)

        doc.close()
        return True

    except Exception as e:
        print(f"Error al extraer portada: {e}")
        return False


def pdf_miniatura(pdf_path, output_path=None, size=(150, 200), dpi=72):
    """
    Extrae la primera página del PDF o carga una imagen como miniatura optimizada.
    Ideal para TableView, listas, previews pequeñas.

    Args:
        pdf_path (str): Ruta al archivo (PDF o imagen)
        output_path (str, optional): Ruta donde guardar. Si es None, retorna PhotoImage
        size (tuple): (ancho, alto) de la miniatura. Default: (150, 200)
        dpi (int): Resolución baja para rapidez (solo PDF). Default: 72

    Returns:
        ImageTk.PhotoImage si output_path es None, bool si se guarda archivo
    """
    try:
        img = None
        # Verificar si es PDF
        if str(pdf_path).lower().endswith('.pdf'):
            # Convertir solo primera página con baja resolución
            imagenes = convert_from_path(pdf_path, dpi=dpi, first_page=1, last_page=1)
            if imagenes:
                img = imagenes[0]
        elif str(pdf_path).lower().endswith('.epub'):
            try:
                with fitz.open(pdf_path) as doc:
                    page = doc[0]
                    zoom = dpi / 72
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mat)
                    mode = "RGBA" if pix.alpha else "RGB"
                    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            except RuntimeError as e:
                print(f"Error al abrir EPUB (posible DRM o archivo corrupto): {e}")
            except Exception as e:
                print(f"Error inesperado procesando EPUB: {e}")
        else:
            # Intentar abrir como imagen
            img = Image.open(pdf_path)

        if img is None:
            return None if output_path is None else False

        # Redimensionar a miniatura manteniendo proporción
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # Si se especifica ruta, guardar archivo
        if output_path:
            img.save(output_path, 'PNG', optimize=True, quality=85)
            return True

        # Si no, retornar PhotoImage para uso directo en tkinter
        return ImageTk.PhotoImage(img)

    except Exception as e:
        return None if output_path is None else False


def pdf_normal(pdf_path, output_path=None, max_size=(800, 1100), dpi=150):
    """
    Extrae la primera página del PDF o carga una imagen en tamaño normal con buena calidad.
    Ideal para visualización completa, impresión, vista detallada.

    Args:
        pdf_path (str): Ruta al archivo (PDF o imagen)
        output_path (str, optional): Ruta donde guardar. Si es None, retorna PhotoImage
        max_size (tuple): Tamaño máximo (ancho, alto). Default: (800, 1100)
        dpi (int): Resolución media-alta para calidad (solo PDF). Default: 150

    Returns:
        ImageTk.PhotoImage si output_path es None, bool si se guarda archivo
    """
    try:
        img = None
        # Verificar si es PDF
        if str(pdf_path).lower().endswith('.pdf'):
            # Convertir primera página con buena resolución
            imagenes = convert_from_path(pdf_path, dpi=dpi, first_page=1, last_page=1)
            if imagenes:
                img = imagenes[0]
        elif str(pdf_path).lower().endswith('.epub'):
            try:
                with fitz.open(pdf_path) as doc:
                    page = doc[0]
                    zoom = dpi / 72
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mat)
                    mode = "RGBA" if pix.alpha else "RGB"
                    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            except RuntimeError as e:
                print(f"Error al abrir EPUB (posible DRM o archivo corrupto): {e}")
            except Exception as e:
                print(f"Error inesperado procesando EPUB: {e}")
        else:
            # Intentar abrir como imagen
            img = Image.open(pdf_path)

        if img is None:
            return None if output_path is None else False

        # Redimensionar si excede el tamaño máximo
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Si se especifica ruta, guardar archivo
        if output_path:
            img.save(output_path, 'PNG', optimize=True, quality=95)
            return True

        # Si no, retornar PhotoImage para uso directo en tkinter
        return ImageTk.PhotoImage(img)

    except Exception as e:
        return None if output_path is None else False
