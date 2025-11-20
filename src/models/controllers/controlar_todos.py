import threading
import time
from os.path import join
from ttkbootstrap import Label, Progressbar
from ttkbootstrap.tableview import Tableview
from typing import Dict
from utilities.auxiliar import copiar_archivo, mover_archivo, eliminar_archivo, papelera_archivo
from pathlib import Path


class ControlarTodos:
    """Esta clase controlara todas las operaciones referente a la tabla"""

    def __init__(
        self,
        label_progreso: Label,
        progress_bar: Progressbar,
        table_view: Tableview,
        ruta_destino: str,
    ):
        # creamos las variables para administrar el proceso
        self.label_progreso = label_progreso
        self.progress_bar = progress_bar
        self.table_view = table_view
        # creamos la variable que
        self.dict_data: Dict[str, tuple] = {}
        # la ruta de destino para operar con los archicos
        self.ruta_destino = ruta_destino

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas
    # └────────────────────────────────────────────────────────────┘

    def _load_data(self):
        items = self.table_view.view.get_children()
        if items:
            for item in items:
                values = self.table_view.view.item(item, 'values')
                if values:
                    self.dict_data[item] = values

    def copiar_todos(self):
        """Iniciamos el hilo de trabajo"""
        hilo_trabajo = threading.Thread(target=self._procesar_y_copiar_todos)
        hilo_trabajo.start()

    def mover_todos(self):
        """Iniciamos el hilo de trabajo"""
        hilo_trabajo = threading.Thread(target=self._procesar_y_mover_todos)
        hilo_trabajo.start()

    def eliminar_todos(self):
        """Iniciamos el hilo de trabajo"""
        hilo_trabajo = threading.Thread(target=self._procesar_y_eliminar_todos)
        hilo_trabajo.start()

    def papelara_todos(self):
        """Iniciamos el hilo de trabajo"""
        hilo_trabajo = threading.Thread(target=self._procesar_y_papelera_todos)
        hilo_trabajo.start()

    def _procesar_y_copiar_todos(self):

        # cargamos los datos
        self._load_data()

        if self.dict_data:
            # obtenemos el total de los datos
            total_datos = len(self.dict_data.keys())

            # configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # recorremos los datos y obtebemos la ruta
            for i, item in enumerate(self.dict_data.keys()):
                fila = self.dict_data[item]
                self.table_view.after(
                    0, lambda r=fila[6]: self.label_progreso.config(text=f"Copiando: {r}")
                )
                # copiamos
                self._copiar(ruta_origen=fila[6])

                # Actualizamos la bara de progreso
                self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

            # Finalizamos el proceso y mostramos un mensaje
            self._proceso_finalizado(tipo_proceso="Proceso de copiado finalizado")

    def _procesar_y_mover_todos(self):

        # cargamos los datos
        self._load_data()

        if self.dict_data:
            # obtenemos el total de los datos
            total_datos = len(self.dict_data.keys())

            # configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # recorremos los datos y obtebemos la ruta
            for i, item in enumerate(self.dict_data.keys()):
                fila = self.dict_data[item]
                self.table_view.after(
                    0, lambda r=fila[6]: self.label_progreso.config(text=f"Moviendo: {r}")
                )
                # copiamos
                self._mover(ruta_origen=fila[6])

                # Actualizamos la bara de progreso
                self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                # eliminamos la fila del archivo
                self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

            # Finalizamos el proceso y mostramos un mensaje
            self._proceso_finalizado(tipo_proceso="Proceso de translado finalizado")

    def _procesar_y_eliminar_todos(self):

        # cargamos los datos
        self._load_data()

        if self.dict_data:
            # obtenemos el total de los datos
            total_datos = len(self.dict_data.keys())

            # configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # recorremos los datos y obtebemos la ruta
            for i, item in enumerate(self.dict_data.keys()):
                fila = self.dict_data[item]
                self.table_view.after(
                    0, lambda r=fila[6]: self.label_progreso.config(text=f"Eliminado: {r}")
                )
                # copiamos
                self._eliminar(ruta_origen=fila[6])

                # Actualizamos la bara de progreso
                self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                # eliminamos la fila del archivo
                self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

            # Finalizamos el proceso y mostramos un mensaje
            self._proceso_finalizado(tipo_proceso="Proceso de eliminacion finalizado")

    def _procesar_y_papelera_todos(self):

        # cargamos los datos
        self._load_data()

        if self.dict_data:
            # obtenemos el total de los datos
            total_datos = len(self.dict_data.keys())

            # configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # recorremos los datos y obtebemos la ruta
            for i, item in enumerate(self.dict_data.keys()):
                fila = self.dict_data[item]
                self.table_view.after(
                    0, lambda r=fila[6]: self.label_progreso.config(text=f"Papelara: {r}")
                )
                # copiamos
                self._papelera(ruta_origen=fila[6])

                # Actualizamos la bara de progreso
                self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                # eliminamos la fila del archivo
                self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

            # Finalizamos el proceso y mostramos un mensaje
            self._proceso_finalizado(tipo_proceso="Proceso de translado a la papelera finalizado")

    def _papelera(self, ruta_origen):
        """Hacemos la operacion de enviar los archivos a la papelera"""
        time.sleep(2)
        papelera_archivo(ruta_origen=ruta_origen)

    def _eliminar(self, ruta_origen):
        """Hacemos la operacion de eliminar los archivos"""
        time.sleep(2)
        eliminar_archivo(ruta_destino=ruta_origen)

    def _copiar(self, ruta_origen: str):
        """Hacemos la operacion de copiar"""
        time.sleep(2)
        nombre_archivo = Path(ruta_origen).name
        ruta_dest = join(self.ruta_destino, nombre_archivo)
        copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_dest)

    def _mover(self, ruta_origen: str):
        """Hacemos la operacion de copiar"""
        time.sleep(2)
        nombre_archivo = Path(ruta_origen).name
        ruta_dest = join(self.ruta_destino, nombre_archivo)
        mover_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_dest)

    def _proceso_finalizado(self, tipo_proceso: str):
        """Método seguro para la GUI: ajusta la tabla y actualiza el mensaje final."""
        self.table_view.autofit_columns()
        self.label_progreso.config(text=tipo_proceso)
