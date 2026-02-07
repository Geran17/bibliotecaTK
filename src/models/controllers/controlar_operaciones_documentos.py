import time
from threading import Thread
from os.path import exists, join
from ttkbootstrap.tableview import Tableview, TableRow
from ttkbootstrap import Label, Progressbar
from models.entities.documento import Documento
from typing import List, Dict
from tkinter.messagebox import showwarning, askyesno
from utilities.auxiliar import (
    generar_ruta_documento,
    copiar_archivo,
    mover_archivo,
    eliminar_archivo,
)
from models.controllers.configuracion_controller import ConfiguracionController


class ControlarOperacionesDocumentos:
    def __init__(
        self, master, table_view: Tableview, lbl_progreso: Label, progress_bar: Progressbar
    ):
        self.master = master
        self.table_view = table_view
        self.lbl_progreso = lbl_progreso
        self.prosgress_bar = progress_bar

        # variables
        self.path_copy = None
        self.path_move = None
        self.path_biblioteca = None

        conf = ConfiguracionController()
        if isinstance(conf, ConfiguracionController):
            if conf.obtener_ubicacion_biblioteca():
                self.path_biblioteca = conf.obtener_ubicacion_biblioteca()

        # obtenemos los documentos seleccionados
        self.documentos_seleccionados: List[Documento] = []
        # mapa de documento fila
        self.map_id_fila: Dict[str, TableRow] = {}

        # cargamos los documetos seleccionados
        self._cargar_documentos_seleccionados()

    def _cargar_documentos_seleccionados(self):
        filas = self.table_view.get_rows(selected=True)
        for fila in filas:
            if fila.values:
                id_documento = int(fila.values[0])
                documento = Documento(
                    id=id_documento,
                    nombre=fila.values[3],
                    extension=fila.values[4],
                    tamano=0,
                    creado_en="",
                    actualizado_en="",
                    hash=fila.values[9],
                )
                # cargamos el mapa
                self.map_id_fila.setdefault(documento.id, fila)
                documento.instanciar()
                if isinstance(documento, Documento):
                    self.documentos_seleccionados.append(documento)

    def set_path_copy(self, path_copy: str):
        self.path_copy = path_copy

    def set_path_move(self, path_move: str):
        self.path_move = path_move

    def ejecutar_copia_seleccionados(self):
        if not self._confirmar_operacion("copiar", self.path_copy):
            return
        hijo_copia = Thread(target=self._copiar_seleccionados)
        hijo_copia.start()

    def ejecutar_mover_seleccionados(self):
        if not self._confirmar_operacion("mover", self.path_move):
            return
        hijo_mover = Thread(target=self._mover_seleccionados)
        hijo_mover.start()

    def ejecutar_eliminar_seleccionados(self):
        if not self._confirmar_operacion("eliminar"):
            return
        hijo_eliminar = Thread(target=self._eliminar_seleccionados)
        hijo_eliminar.start()

    def ejecutar_eliminar_filas_seleccionados(self):
        if not self._confirmar_operacion("eliminar filas"):
            return
        hijo_eliminar_filas = Thread(target=self._eliminar_filas_seleccionados)
        hijo_eliminar_filas.start()

    def ejecutar_eliminar_registros(self):
        if not self._confirmar_operacion("eliminar registros"):
            return
        hijo_registros = Thread(target=self._eliminar_registros)
        hijo_registros.start()

    def _confirmar_operacion(self, operacion: str, ruta_destino: str = None) -> bool:
        if not self.documentos_seleccionados:
            showwarning(
                title="Advertencia",
                message="Seleccione al menos un documento para continuar.",
                parent=self.master,
            )
            return False

        total = len(self.documentos_seleccionados)
        mensaje = [f"Operación: {operacion}", f"Documentos seleccionados: {total}"]
        if ruta_destino:
            mensaje.append(f"Destino: {ruta_destino}")
        mensaje.append("¿Desea continuar?")
        return askyesno(
            title="Confirmar operación en lote",
            message="\n".join(mensaje),
            parent=self.master,
        )

    def _copiar_seleccionados(self):
        """Copiamos los archivos seleccionados"""

        # verificamos que se hayan selecciados los documentos
        if not self.documentos_seleccionados:
            showwarning(
                title="Advertencia",
                message="Seleccione los documentos a copiar",
                parent=self.master,
            )
            return

        total_seleccinados = len(self.documentos_seleccionados)
        # configuramos el progress, con el maximo de elementos encontrados
        self.table_view.after(
            0, lambda: self.prosgress_bar.config(maximum=total_seleccinados, value=0)
        )
        for i, documento in enumerate(self.documentos_seleccionados):
            # actualizamos o mostramos el proceso en el label
            self.table_view.after(
                0,
                lambda nombre=documento.nombre: self.lbl_progreso.config(
                    text=f"Copiando >> {nombre} a >> {self.path_copy}"
                ),
            )

            # Copiamos ....
            self._copiar(documento=documento)

            # Actualizamos el progreso
            self.table_view.after(0, lambda v=i + 1: self.prosgress_bar.config(value=v))

        # finalizamos
        self._finalizar_carga_gui()

    def _eliminar_filas_seleccionados(self):
        """Eliminamos filas de los archivos seleccionados"""

        # verificamos que se hayan selecciados los documentos
        if not self.documentos_seleccionados:
            showwarning(
                title="Advertencia",
                message="Seleccione los documentos a copiar",
                parent=self.master,
            )
            return

        total_seleccinados = len(self.documentos_seleccionados)
        # configuramos el progress, con el maximo de elementos encontrados
        self.table_view.after(
            0, lambda: self.prosgress_bar.config(maximum=total_seleccinados, value=0)
        )
        for i, documento in enumerate(self.documentos_seleccionados):
            # actualizamos o mostramos el proceso en el label
            self.table_view.after(
                0,
                lambda nombre=documento.nombre: self.lbl_progreso.config(
                    text=f"Eliminando filas >> {nombre}"
                ),
            )

            # Elimnamos ....
            self._eliminar_filas(documento=documento)

            # Actualizamos el progreso
            self.table_view.after(0, lambda v=i + 1: self.prosgress_bar.config(value=v))

        # finalizamos
        self._finalizar_carga_gui()

    def _eliminar_seleccionados(self):
        """Eliminamos los archivos seleccionados"""

        # verificamos que se hayan selecciados los documentos
        if not self.documentos_seleccionados:
            showwarning(
                title="Advertencia",
                message="Seleccione los documentos a copiar",
                parent=self.master,
            )
            return

        total_seleccinados = len(self.documentos_seleccionados)
        # configuramos el progress, con el maximo de elementos encontrados
        self.table_view.after(
            0, lambda: self.prosgress_bar.config(maximum=total_seleccinados, value=0)
        )
        for i, documento in enumerate(self.documentos_seleccionados):
            # actualizamos o mostramos el proceso en el label
            self.table_view.after(
                0,
                lambda nombre=documento.nombre: self.lbl_progreso.config(
                    text=f"Eliminando >> {nombre}"
                ),
            )

            # Elimnamos ....
            self._eliminar(documento=documento)

            # Actualizamos el progreso
            self.table_view.after(0, lambda v=i + 1: self.prosgress_bar.config(value=v))

        # finalizamos
        self._finalizar_carga_gui()

    def _eliminar_registros(self):
        """Eliminamos los archivos seleccionados"""

        # verificamos que se hayan selecciados los documentos
        if not self.documentos_seleccionados:
            showwarning(
                title="Advertencia",
                message="Seleccione los documentos a copiar",
                parent=self.master,
            )
            return

        total_seleccinados = len(self.documentos_seleccionados)
        # configuramos el progress, con el maximo de elementos encontrados
        self.table_view.after(
            0, lambda: self.prosgress_bar.config(maximum=total_seleccinados, value=0)
        )
        for i, documento in enumerate(self.documentos_seleccionados):
            # actualizamos o mostramos el proceso en el label
            self.table_view.after(
                0,
                lambda nombre=documento.nombre: self.lbl_progreso.config(
                    text=f"Eliminando >> {nombre}"
                ),
            )

            # Elimnamos ....
            self._eliminar_registro(documento=documento)

            # Actualizamos el progreso
            self.table_view.after(0, lambda v=i + 1: self.prosgress_bar.config(value=v))

        # finalizamos
        self._finalizar_carga_gui()

    def _mover_seleccionados(self):
        """Movemos los archivos seleccionados"""

        # verificamos que se hayan selecciados los documentos
        if not self.documentos_seleccionados:
            showwarning(
                title="Advertencia",
                message="Seleccione los documentos a mover",
                parent=self.master,
            )
            return

        total_seleccinados = len(self.documentos_seleccionados)
        # configuramos el progress, con el maximo de elementos encontrados
        self.table_view.after(
            0, lambda: self.prosgress_bar.config(maximum=total_seleccinados, value=0)
        )
        for i, documento in enumerate(self.documentos_seleccionados):
            # actualizamos o mostramos el proceso en el label
            self.table_view.after(
                0,
                lambda nombre=documento.nombre: self.lbl_progreso.config(
                    text=f"Moviendo >> {nombre} a >> {self.path_move}"
                ),
            )

            # Copiamos ....
            self._mover(documento=documento)

            # Actualizamos el progreso
            self.table_view.after(0, lambda v=i + 1: self.prosgress_bar.config(value=v))

        # finalizamos
        self._finalizar_carga_gui()

    def _copiar(self, documento: Documento):
        time.sleep(1)

        if not exists(self.path_biblioteca):
            showwarning(
                title="Advertencia",
                message=f"No existe o no se ha configurado la ubicacion de la bibllioteca: {self.path_biblioteca}",
                parent=self.master,
            )
            return

        ruta_documento = generar_ruta_documento(
            ruta_biblioteca=self.path_biblioteca,
            id_documento=documento.id,
            nombre_documento=f"{documento.nombre}.{documento.extension}",
        )

        if not exists(ruta_documento):
            showwarning(
                title="Advertencia",
                message=f"No existe el documento en la ubicacion seleccionada: {ruta_documento}",
                parent=self.master,
            )
            return

        ruta_destino = join(self.path_copy, f"{documento.nombre}.{documento.extension}")

        copiar_archivo(ruta_origen=ruta_documento, ruta_destino=ruta_destino)

    def _mover(self, documento: Documento):
        time.sleep(1)

        if not exists(self.path_biblioteca):
            showwarning(
                title="Advertencia",
                message=f"No existe o no se ha configurado la ubicacion de la bibllioteca: {self.path_biblioteca}",
                parent=self.master,
            )
            return

        ruta_documento = generar_ruta_documento(
            ruta_biblioteca=self.path_biblioteca,
            id_documento=documento.id,
            nombre_documento=f"{documento.nombre}.{documento.extension}",
        )

        if not exists(ruta_documento):
            showwarning(
                title="Advertencia",
                message=f"No existe el documento en la ubicacion seleccionada: {ruta_documento}",
                parent=self.master,
            )
            return

        ruta_destino = join(self.path_move, f"{documento.nombre}.{documento.extension}")

        if mover_archivo(ruta_origen=ruta_documento, ruta_destino=ruta_destino):
            # si la operacion fue en exito, eliminamos el registros de la base datos
            if documento.eliminar():
                # aqui eliminamos la fila de la tabla
                self.table_view.after(
                    0, lambda doc_id=documento.id: self._eliminar_fila_tabla(doc_id)
                )

    def _eliminar(self, documento: Documento):
        time.sleep(1)

        if not exists(self.path_biblioteca):
            showwarning(
                title="Advertencia",
                message=f"No existe o no se ha configurado la ubicacion de la bibllioteca: {self.path_biblioteca}",
                parent=self.master,
            )
            return

        ruta_documento = generar_ruta_documento(
            ruta_biblioteca=self.path_biblioteca,
            id_documento=documento.id,
            nombre_documento=f"{documento.nombre}.{documento.extension}",
        )

        if eliminar_archivo(ruta_destino=ruta_documento):
            # si la operacion fue un exito, eliminamos el registro de la base de datos
            if documento.eliminar():
                # aqui eliminamos la fila de la tabla
                self.table_view.after(
                    0, lambda doc_id=documento.id: self._eliminar_fila_tabla(doc_id)
                )

    def _eliminar_registro(self, documento: Documento):
        time.sleep(1)

        if documento.eliminar():
            # aqui eliminamos la fila de la tabla
            self.table_view.after(0, lambda doc_id=documento.id: self._eliminar_fila_tabla(doc_id))

    def _eliminar_filas(self, documento: Documento):
        time.sleep(1)
        self.table_view.after(0, lambda doc_id=documento.id: self._eliminar_fila_tabla(doc_id))

    def _finalizar_carga_gui(self):
        self.table_view.autofit_columns()
        self.lbl_progreso.config(text="Proceso completado con exito!!!.")

    def _eliminar_fila_tabla(self, id_documento: int):
        fila: TableRow = self.map_id_fila.get(id_documento, None)
        if fila is not None:
            iid = fila.iid
            self.table_view.delete_row(iid=iid)
            # Limpiamos el mapeo
            del self.map_id_fila[id_documento]
