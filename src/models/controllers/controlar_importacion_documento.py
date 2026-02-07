import threading
import time
import logging
from os.path import join, exists
from pathlib import Path
from ttkbootstrap import Label, Progressbar
from ttkbootstrap.tableview import Tableview
from typing import Dict, Optional
from models.entities.documento import Documento
from models.entities.metadato import Metadato
from utilities.auxiliar import (
    obtener_datos_documento,
    hash_sha256,
    generar_ruta_documento,
    copiar_archivo,
    mover_archivo,
    obtener_metadatos,
    crear_directorio_id_documento,
    pdf_miniatura,
    pdf_normal,
)
from models.controllers.configuracion_controller import ConfiguracionController

# Configurar logging
logger = logging.getLogger(__name__)


class ControlarImporetacionDocumento:
    """Controlador para gestionar la importación de documentos a la biblioteca.

    Esta clase maneja todo el proceso de importación incluyendo:
    - Validación y carga de documentos
    - Inserción en la base de datos
    - Generación de metadatos
    - Copia o movimiento de archivos
    - Generación de portadas para PDFs
    - Actualización de progreso en la GUI
    """

    def __init__(
        self,
        label_progress: Label,
        progress_bar: Progressbar,
        table_view: Tableview,
        tipo_importacion: str = "copiar",
    ) -> None:
        """Inicializa el controlador de importación.

        Args:
            label_progress: Widget Label para mostrar el progreso
            progress_bar: Widget Progressbar para la barra de progreso
            table_view: Widget Tableview que contiene los documentos a importar
            tipo_importacion: Tipo de operación ('copiar' o 'mover'). Por defecto 'copiar'
        """
        self.label_progress: Label = label_progress
        self.progress_bar: Progressbar = progress_bar
        self.table_view: Tableview = table_view
        self.dict_data: Dict[str, tuple] = {}
        self.tipo_importacion: str = tipo_importacion
        self.ruta_biblioteca: str = ""
        self.ruta_portadas: str = ""

        try:
            configuracion = ConfiguracionController()
            if exists(configuracion.obtener_ubicacion_biblioteca()):
                self.ruta_biblioteca = configuracion.obtener_ubicacion_biblioteca()
                self.ruta_portadas = configuracion.obtener_ubicacion_portadas()
                logger.info(f"Rutas configuradas - Biblioteca: {self.ruta_biblioteca}")
        except Exception as e:
            logger.error(f"Error al obtener configuración: {e}")

    def importar(self) -> None:
        """Inicia el hilo de trabajo para importar documentos de forma asíncrona."""
        try:
            hilo_trabajo = threading.Thread(target=self._procesar_importacion, daemon=True)
            hilo_trabajo.start()
            logger.info("Iniciando proceso de importación en hilo de trabajo")
        except Exception as e:
            logger.error(f"Error al iniciar importación: {e}")
            self.table_view.after(0, lambda: self.label_progress.config(text=f"Error: {e}"))

    def _load_data(self) -> None:
        """Carga los datos de la tabla en un diccionario.

        Extrae todos los items de la Tableview y los almacena en dict_data
        para procesarlos posteriormente.
        """
        try:
            items = self.table_view.view.get_children()
            if items:
                for item in items:
                    values = self.table_view.view.item(item, 'values')
                    if values:
                        self.dict_data[item] = values
            logger.info(f"Datos cargados: {len(self.dict_data)} documentos")
        except Exception as e:
            logger.error(f"Error al cargar datos de la tabla: {e}")

    def _procesar_importacion(self) -> None:
        """Procesa la importación de todos los documentos en el hilo de trabajo.

        Este método es ejecutado en un hilo separado para no bloquear la GUI.
        Realiza:
        - Validación de documentos
        - Inserción en base de datos
        - Gestión de metadatos
        - Copia/movimiento de archivos
        - Generación de portadas
        """
        # cargamos los datos
        self._load_data()

        # Configuramos el proceso inicial
        total_archivos = len(self.dict_data.keys())
        self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_archivos, value=0))

        # recorremos los datos
        if self.dict_data:

            for i, item in enumerate(self.dict_data.keys()):
                fila = self.dict_data[item]
                ruta_documento = fila[6]
                documento = self._generar_documento(ruta_documento=ruta_documento)
                # verificamos que se una instancia del documento
                if isinstance(documento, Documento):
                    # verificamos que no exista en la base de datos
                    if not documento.existe():
                        # si no existe cargamos el documento a la base de datos
                        id_documento = documento.insertar()
                        nombre_con_extension = f"{documento.nombre}.{documento.extension}"
                        # insertamos los metadatos de los documentos
                        self._inserta_metadatos(
                            id_documento=id_documento, ruta_documento=ruta_documento
                        )
                        # Copiamos o movemos los archivos de acuerdo a la opcion del usuario
                        if self.tipo_importacion == "copiar":
                            # copiamos los archivos
                            ruta_destino = generar_ruta_documento(
                                self.ruta_biblioteca,
                                nombre_documento=nombre_con_extension,
                                id_documento=id_documento,
                            )
                            # copiamos
                            self._copiar_documento(
                                ruta_origen=ruta_documento, ruta_destino=ruta_destino
                            )
                            # generamos la portad
                            self._generar_portada(
                                pdf_path=ruta_documento,
                                id_documento=id_documento,
                                extension=documento.extension,
                            )
                        elif self.tipo_importacion == "mover":
                            # movemos lo archivos
                            ruta_destino = generar_ruta_documento(
                                self.ruta_biblioteca,
                                nombre_documento=nombre_con_extension,
                                id_documento=id_documento,
                            )
                            # antes de mover generamos la portada
                            self._generar_portada(
                                pdf_path=ruta_documento,
                                id_documento=id_documento,
                                extension=documento.extension,
                            )
                            # movemos
                            self._mover_documento(
                                ruta_origen=ruta_documento, ruta_destino=ruta_destino
                            )

                        # mostramos el proceso en el label
                        self.table_view.after(
                            0,
                            lambda r=ruta_documento: self.label_progress.config(
                                text=f"Importando el archivo: {r}"
                            ),
                        )

                        # sacamos los archivos importados de la tabla, para evitar dobles importaciones
                        self.table_view.after(0, lambda it=item: self.table_view.view.delete(item))

                # 2. Actualizar el progreso (DELEGADO a la GUI)
                self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

            # mostramos la importacion de documentos
            self.table_view.view.after(0, self._finalizar_carga_gui)

    def _inserta_metadatos(self, id_documento: int, ruta_documento):
        datos = obtener_metadatos(ruta_origen=ruta_documento)
        for clave, valor in datos.items():
            meta_dato = Metadato(id_documento=id_documento, clave=clave, valor=valor)
            meta_dato.insertar()

    def _finalizar_carga_gui(self):
        """Método seguro para la GUI: ajusta la tabla y actualiza el mensaje final."""
        self.table_view.autofit_columns()
        self.label_progress.config(text="Importacion de archivos completado.")

    def _copiar_documento(self, ruta_origen, ruta_destino):
        """Copiamos los archivos importados a la biblioteca"""
        time.sleep(1)
        copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)

    def _mover_documento(self, ruta_origen, ruta_destino):
        """Copiamos los archivos importados a la biblioteca"""
        time.sleep(1)
        mover_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)

    def _generar_documento(self, ruta_documento: str) -> Documento:
        documento = None
        if exists(ruta_documento):
            datos = obtener_datos_documento(ruta_origen=ruta_documento)
            documento = Documento(
                nombre=datos['nombre_sin_extension'],
                extension=datos['extension'],
                tamano=datos['tamano_bytes'],
                hash=hash_sha256(archivo=ruta_documento),
                esta_activo=True,
            )
        return documento

    def _generar_portada(self, pdf_path: str, id_documento: int, extension: str):
        if extension.lower() == "pdf":
            if exists(self.ruta_portadas):
                dir_portada = crear_directorio_id_documento(
                    ruta_destino=self.ruta_portadas, id_documento=id_documento
                )
                output_path_normal = join(dir_portada, f"{str(id_documento)}_normal.png")
                output_path_miniatura = join(dir_portada, f"{str(id_documento)}_miniatura.png")
                pdf_miniatura(pdf_path=pdf_path, output_path=output_path_miniatura)
                pdf_normal(pdf_path=pdf_path, output_path=output_path_normal)
