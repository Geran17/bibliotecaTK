import threading
import time
import logging
from os.path import join
from ttkbootstrap import Label, Progressbar
from ttkbootstrap.tableview import Tableview
from typing import Dict
from utilities.auxiliar import copiar_archivo, mover_archivo, eliminar_archivo, papelera_archivo
from pathlib import Path

# Configurar logging
logger = logging.getLogger(__name__)


class ControlarTodos:
    """Controlador para operaciones en masa sobre todos los documentos de la tabla.

    Gestiona operaciones de copia, movimiento, eliminación y envío a papelera
    para todos los archivos cargados en la tabla de una manera segura y asíncrona.
    Las operaciones se ejecutan en hilos separados para no bloquear la interfaz.
    """

    def __init__(
        self,
        label_progreso: Label,
        progress_bar: Progressbar,
        table_view: Tableview,
        ruta_destino: str,
    ) -> None:
        """Inicializa el controlador de operaciones en masa.

        Args:
            label_progreso: Widget Label para mostrar el progreso y estado actual
            progress_bar: Widget Progressbar para la visualización del progreso
            table_view: Widget Tableview que contiene los documentos
            ruta_destino: Ruta de destino para operaciones de copia/movimiento
        """
        self.label_progreso: Label = label_progreso
        self.progress_bar: Progressbar = progress_bar
        self.table_view: Tableview = table_view
        self.dict_data: Dict[str, tuple] = {}
        self.ruta_destino: str = ruta_destino
        logger.info("ControlarTodos inicializado")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Públicas
    # └────────────────────────────────────────────────────────────┘

    def copiar_todos(self) -> None:
        """Inicia el proceso asíncrono de copia de todos los archivos.

        Crea un hilo demonio para procesar la copia de archivos sin bloquear
        la interfaz de usuario. Actualiza la barra de progreso durante la operación.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_copiar_todos, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de copia iniciado")

    def mover_todos(self) -> None:
        """Inicia el proceso asíncrono de movimiento de todos los archivos.

        Crea un hilo demonio para procesar el movimiento de archivos sin bloquear
        la interfaz de usuario. Los archivos se mueven a ruta_destino.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_mover_todos, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de movimiento iniciado")

    def eliminar_todos(self) -> None:
        """Inicia el proceso asíncrono de eliminación de todos los archivos.

        Crea un hilo demonio para procesar la eliminación de archivos sin bloquear
        la interfaz de usuario. Los archivos se eliminarán permanentemente.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_eliminar_todos, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de eliminación iniciado")

    def papelera_todos(self) -> None:
        """Inicia el proceso asíncrono de envío a papelera de todos los archivos.

        Crea un hilo demonio para procesar el envío a papelera sin bloquear
        la interfaz de usuario. Los archivos se pueden recuperar desde papelera.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_papelera_todos, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de papelera iniciado")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas - Carga de Datos
    # └────────────────────────────────────────────────────────────┘

    def _load_data(self) -> None:
        """Carga los datos de la tabla en el diccionario interno.

        Itera sobre todos los elementos visibles en la tabla y almacena
        sus valores en dict_data para procesamiento posterior.
        """
        try:
            items = self.table_view.view.get_children()
            self.dict_data.clear()

            if items:
                for item in items:
                    values = self.table_view.view.item(item, 'values')
                    if values:
                        self.dict_data[item] = values
                logger.debug(f"Datos cargados: {len(self.dict_data)} elementos")
            else:
                logger.warning("No hay elementos en la tabla")

        except Exception as e:
            logger.error(f"Error al cargar datos de tabla: {e}")
            self.label_progreso.config(text="❌ Error al cargar datos")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas - Procesamiento en Hilo
    # └────────────────────────────────────────────────────────────┘

    def _procesar_y_copiar_todos(self) -> None:
        """Procesa la copia de todos los archivos en un hilo separado.

        Itera sobre todos los archivos cargados, copia cada uno a la ruta
        de destino especificada, actualiza la UI con el progreso actual.
        Maneja errores de forma robusta continuando con el siguiente archivo.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos para copiar")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando copia de {total_datos} archivos")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"📋 Copiando: {r}"
                        ),
                    )

                    # Realizamos la copia
                    self._copiar(ruta_origen=nombre_archivo)

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                    logger.debug(f"✓ Copiado: {nombre_archivo}")

                except Exception as e:
                    logger.error(f"Error copiando archivo {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Copia completada exitosamente")
            logger.info("Proceso de copia finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de copia masiva: {e}")
            self.label_progreso.config(text="❌ Error en la copia")
            self.progress_bar.config(value=0)

    def _procesar_y_mover_todos(self) -> None:
        """Procesa el movimiento de todos los archivos en un hilo separado.

        Itera sobre todos los archivos cargados, mueve cada uno a la ruta
        de destino especificada, actualiza la UI y elimina las filas de la tabla.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos para mover")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando movimiento de {total_datos} archivos")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"➡️ Moviendo: {r}"
                        ),
                    )

                    # Realizamos el movimiento
                    self._mover(ruta_origen=nombre_archivo)

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                    # Eliminamos la fila del archivo
                    self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

                    logger.debug(f"✓ Movido: {nombre_archivo}")

                except Exception as e:
                    logger.error(f"Error moviendo archivo {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Movimiento completado exitosamente")
            logger.info("Proceso de movimiento finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de movimiento masivo: {e}")
            self.label_progreso.config(text="❌ Error en el movimiento")
            self.progress_bar.config(value=0)

    def _procesar_y_eliminar_todos(self) -> None:
        """Procesa la eliminación de todos los archivos en un hilo separado.

        Itera sobre todos los archivos cargados, elimina cada uno permanentemente,
        actualiza la UI y elimina las filas de la tabla.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos para eliminar")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando eliminación de {total_datos} archivos")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"🗑️ Eliminando: {r}"
                        ),
                    )

                    # Realizamos la eliminación
                    self._eliminar(ruta_origen=nombre_archivo)

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                    # Eliminamos la fila del archivo
                    self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

                    logger.debug(f"✓ Eliminado: {nombre_archivo}")

                except Exception as e:
                    logger.error(f"Error eliminando archivo {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Eliminación completada")
            logger.info("Proceso de eliminación finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de eliminación masiva: {e}")
            self.label_progreso.config(text="❌ Error en la eliminación")
            self.progress_bar.config(value=0)

    def _procesar_y_papelera_todos(self) -> None:
        """Procesa el envío a papelera de todos los archivos en un hilo separado.

        Itera sobre todos los archivos cargados, envía cada uno a papelera,
        actualiza la UI y elimina las filas de la tabla.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos para enviar a papelera")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando envío a papelera de {total_datos} archivos")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"♻️ Papelera: {r}"
                        ),
                    )

                    # Realizamos envío a papelera
                    self._papelera(ruta_origen=nombre_archivo)

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                    # Eliminamos la fila del archivo
                    self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

                    logger.debug(f"✓ Enviado a papelera: {nombre_archivo}")

                except Exception as e:
                    logger.error(f"Error enviando a papelera {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Envío a papelera completado")
            logger.info("Proceso de papelera finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de papelera masiva: {e}")
            self.label_progreso.config(text="❌ Error en papelera")
            self.progress_bar.config(value=0)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas - Operaciones de Archivo
    # └────────────────────────────────────────────────────────────┘

    def _papelera(self, ruta_origen: str) -> None:
        """Envía un archivo a la papelera del sistema.

        Args:
            ruta_origen: Ruta completa del archivo a enviar a papelera

        Raises:
            Exception: Si ocurre un error durante la operación de papelera
        """
        try:
            time.sleep(2)
            papelera_archivo(ruta_origen=ruta_origen)
            logger.debug(f"Archivo enviado a papelera: {ruta_origen}")
        except Exception as e:
            logger.error(f"Error al enviar a papelera {ruta_origen}: {e}")
            raise

    def _eliminar(self, ruta_origen: str) -> None:
        """Elimina un archivo permanentemente.

        Args:
            ruta_origen: Ruta completa del archivo a eliminar

        Raises:
            Exception: Si ocurre un error durante la eliminación
        """
        try:
            time.sleep(2)
            eliminar_archivo(ruta_destino=ruta_origen)
            logger.debug(f"Archivo eliminado: {ruta_origen}")
        except Exception as e:
            logger.error(f"Error al eliminar {ruta_origen}: {e}")
            raise

    def _copiar(self, ruta_origen: str) -> None:
        """Copia un archivo a la ruta de destino especificada.

        Args:
            ruta_origen: Ruta completa del archivo a copiar

        Raises:
            Exception: Si ocurre un error durante la copia
        """
        try:
            time.sleep(2)
            nombre_archivo = Path(ruta_origen).name
            ruta_dest = join(self.ruta_destino, nombre_archivo)
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_dest)
            logger.debug(f"Archivo copiado: {ruta_origen} → {ruta_dest}")
        except Exception as e:
            logger.error(f"Error al copiar {ruta_origen}: {e}")
            raise

    def _mover(self, ruta_origen: str) -> None:
        """Mueve un archivo a la ruta de destino especificada.

        Args:
            ruta_origen: Ruta completa del archivo a mover

        Raises:
            Exception: Si ocurre un error durante el movimiento
        """
        try:
            time.sleep(2)
            nombre_archivo = Path(ruta_origen).name
            ruta_dest = join(self.ruta_destino, nombre_archivo)
            mover_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_dest)
            logger.debug(f"Archivo movido: {ruta_origen} → {ruta_dest}")
        except Exception as e:
            logger.error(f"Error al mover {ruta_origen}: {e}")
            raise

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas - Finalización
    # └────────────────────────────────────────────────────────────┘

    def _proceso_finalizado(self, tipo_proceso: str) -> None:
        """Finaliza el proceso actualizando la UI de forma segura.

        Args:
            tipo_proceso: Mensaje descriptivo del proceso finalizado
        """
        try:
            self.table_view.autofit_columns()
            self.label_progreso.config(text=tipo_proceso)
            logger.info(tipo_proceso)
        except Exception as e:
            logger.error(f"Error al finalizar proceso: {e}")
