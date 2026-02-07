import threading
import time
import datetime
import logging
from pathlib import Path
from os.path import isfile
from typing import List
from utilities.auxiliar import hash_sha256, obtener_datos_documento
from models.entities.documento import Documento
from ttkbootstrap import Label, Progressbar
from ttkbootstrap.tableview import Tableview

# Configurar logging
logger = logging.getLogger(__name__)


class ControlarSeleccionDocumentos:
    """Controlador para gestionar la selección y carga de documentos en la tabla.

    Esta clase procesa archivos seleccionados y los carga en la interfaz,
    generando metadatos como hash, tamaño, fechas, etc.
    """

    def __init__(
        self,
        label_progreso: Label,
        progress_bar: Progressbar,
        table_view: Tableview,
        lista_archivos: List[str],
    ) -> None:
        """Inicializa el controlador de selección.

        Args:
            label_progreso: Widget Label para mostrar el progreso
            progress_bar: Widget Progressbar para la barra de progreso
            table_view: Widget Tableview donde se mostrarán los archivos
            lista_archivos: Lista de rutas de archivos a procesar
        """
        self.label_progreso: Label = label_progreso
        self.progress_bar: Progressbar = progress_bar
        self.table_view: Tableview = table_view
        self.lista_archivos: List[str] = lista_archivos
        self.formato: str = "%Y-%m-%d %H:%M:%S"

    def cargar_archivos_seleccionados(self) -> None:
        """Inicia un hilo de trabajo para cargar los archivos seleccionados.

        Procesa todos los archivos de forma asíncrona sin bloquear la GUI.
        """
        if self.lista_archivos:
            try:
                logger.info(f"Iniciando carga de {len(self.lista_archivos)} archivos")
                hilo_trabajo = threading.Thread(
                    target=self._procesar_y_cargar_archivos, daemon=True
                )
                hilo_trabajo.start()
            except Exception as e:
                logger.error(f"Error al iniciar carga de archivos: {e}")
                self.table_view.after(0, lambda: self.label_progreso.config(text=f"Error: {e}"))

    def _procesar_y_cargar_archivos(self) -> None:
        """Procesa y carga todos los archivos en el hilo de trabajo.

        Genera filas con metadatos para cada archivo y las inserta
        en la tabla de forma segura para la GUI.
        """

        # 1. Configurar el progreso inicial
        total_archivos = len(self.lista_archivos)
        self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_archivos, value=0))

        for i, ruta_archivo in enumerate(self.lista_archivos):
            try:
                # Actualizar la etiqueta (DELEGADO a la GUI)
                self.table_view.after(
                    0, lambda r=ruta_archivo: self.label_progreso.config(text=f"Procesando: {r}")
                )

                fila = self._generar_fila(ruta_archivo=ruta_archivo)

                if fila:
                    # Insertar la fila en el hilo de trabajo
                    self.insertar_fila(values=fila)

                # Actualizar el progreso (DELEGADO a la GUI)
                self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))
            except Exception as e:
                logger.error(f"Error procesando archivo {ruta_archivo}: {e}")

        # Finalizar (DELEGADO a la GUI)
        self.table_view.after(0, self._finalizar_carga_gui)

    def insertar_fila(self, values: List) -> None:
        """Inserta una fila en la tabla de forma segura para la GUI.

        Args:
            values: Lista de valores para la fila
        """
        try:
            time.sleep(1.5)  # Simular operación I/O
            # Usamos 'after' para ejecutar en el hilo principal de Tkinter
            self.table_view.after(0, self._insertar_en_gui, values)
        except Exception as e:
            logger.error(f"Error al insertar fila: {e}")

    def _insertar_en_gui(self, values: list):
        """Método seguro para la GUI: inserta la fila en la Tableview."""
        self.table_view.insert_row(values=values)

    def _finalizar_carga_gui(self):
        """Método seguro para la GUI: ajusta la tabla y actualiza el mensaje final."""
        self.table_view.autofit_columns()
        self.label_progreso.config(text="Carga de archivos completada.")

    def _generar_fila(self, ruta_archivo: str) -> list:
        """
        Genera una lista de valores para una fila de la tabla a partir de una ruta de archivo.

        Args:
            ruta_archivo (str): La ruta completa al archivo a procesar.

        Returns:
            list: Una lista con los datos del archivo para ser insertada en la tabla,
                  o una lista vacía si el archivo no es válido o no se puede procesar.
        """
        if not isfile(ruta_archivo):
            return []

        # 1. Obtener datos básicos y hash del archivo.
        hash_archivo = hash_sha256(archivo=ruta_archivo)
        datos_documento = obtener_datos_documento(ruta_origen=ruta_archivo)

        if not hash_archivo or not datos_documento:
            return []

        # 2. Verificar si el documento ya existe en la base de datos.
        documento = Documento(
            nombre=datos_documento['nombre_sin_extension'],
            extension=datos_documento['extension'],
            hash=hash_archivo,
            tamano=datos_documento['tamano_bytes'],
        )
        estado_existencia = "🔴 Ya Existe" if documento.existe() else "🟢 No Existe"

        # 3. Obtener metadatos de fecha y construir la fila.
        info_archivo = Path(ruta_archivo).stat()
        fecha_creacion = datetime.datetime.fromtimestamp(info_archivo.st_ctime).strftime(
            self.formato
        )
        fecha_modificacion = datetime.datetime.fromtimestamp(info_archivo.st_mtime).strftime(
            self.formato
        )

        return [
            f"📗 {datos_documento['nombre_con_extension']}",
            self._formatear_tamano(int(datos_documento['tamano_bytes'])),
            fecha_creacion,
            fecha_modificacion,
            estado_existencia,
            hash_archivo,
            ruta_archivo,
        ]

    def _formatear_tamano(self, bytes: int) -> str:
        """
        Formatea el tamaño de un archivo de bytes a una unidad legible

        Args:
            bytes: Tamaño en bytes

        Returns:
            String formateado (ej: "1.50 MB", "234 KB", "3.2 GB")
        """
        if bytes < 0:
            return "0 B"

        # Unidades de medida
        unidades = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

        # Caso especial para 0 bytes
        if bytes == 0:
            return "0 B"

        # Calcular el índice de la unidad apropiada
        import math

        indice = min(int(math.log(bytes, 1024)), len(unidades) - 1)

        # Calcular el valor en la unidad correspondiente
        valor = bytes / (1024**indice)

        # Formatear según la unidad
        if indice == 0:  # Bytes
            return f"{int(valor)} B"
        else:
            return f"{valor:.2f} {unidades[indice]}"
