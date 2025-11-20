import threading
import time
from os.path import join, exists
from pathlib import Path
from ttkbootstrap import Label, Progressbar
from ttkbootstrap.tableview import Tableview
from typing import Dict
from models.entities.documento import Documento
from models.entities.metadato import Metadato
from utilities.auxiliar import (
    obtener_datos_documento,
    hash_sha256,
    generar_ruta_documento,
    copiar_archivo,
    mover_archivo,
    obtener_metadatos,
)
from models.controllers.configuracion_controller import ConfiguracionController


class ControlarImporetacionDocumento:
    def __init__(
        self,
        label_progress: Label,
        progress_bar: Progressbar,
        table_view: Tableview,
        tipo_importacion: str = "copiar",
    ):
        # creamos las variables para administrar el proceso
        self.label_progress = label_progress
        self.progress_bar = progress_bar
        self.table_view = table_view
        # creamos la variable que
        self.dict_data: Dict[str, tuple] = {}
        # variable para el tipo de importacion
        self.tipo_importacion = tipo_importacion
        # Ruta biblioteca
        self.ruta_biblioteca = ""
        configuracion = ConfiguracionController()
        if exists(configuracion.obtener_ubicacion_biblioteca()):
            self.ruta_biblioteca = configuracion.obtener_ubicacion_biblioteca()

    def importar(self):
        """Generamos el hilo de importacion"""
        hilo_trabajo = threading.Thread(target=self._procesar_importacion)
        hilo_trabajo.start()

    def _load_data(self):
        items = self.table_view.view.get_children()
        if items:
            for item in items:
                values = self.table_view.view.item(item, 'values')
                if values:
                    self.dict_data[item] = values

    def _procesar_importacion(self):
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
                            self._copiar_documento(
                                ruta_origen=ruta_documento, ruta_destino=ruta_destino
                            )
                        elif self.tipo_importacion == "mover":
                            # movemos lo archivos
                            ruta_destino = generar_ruta_documento(
                                self.ruta_biblioteca,
                                nombre_documento=nombre_con_extension,
                                id_documento=id_documento,
                            )
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
        time.sleep(2)
        copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)

    def _mover_documento(self, ruta_origen, ruta_destino):
        """Copiamos los archivos importados a la biblioteca"""
        time.sleep(2)
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
