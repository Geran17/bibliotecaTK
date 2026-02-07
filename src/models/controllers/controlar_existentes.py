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


class ControlarExistentes:
    """Controlador para operaciones en masa sobre documentos existentes de la tabla.

    Gestiona operaciones de copia, movimiento, eliminación y envío a papelera
    para archivos existentes de una manera segura y asíncrona.
    Las operaciones se ejecutan en hilos separados para no bloquear la interfaz.
    """

    def __init__(
        self,
        label_progreso: Label,
        progress_bar: Progressbar,
        table_view: Tableview,
        ruta_destino: str,
    ) -> None:
        """Inicializa el controlador de operaciones en masa para existentes.

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
        logger.info("ControlarExistentes inicializado")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Públicas
    # └────────────────────────────────────────────────────────────┘

    def copiar_existentes(self) -> None:
        """Inicia el proceso asíncrono de copia de archivos existentes.

        Crea un hilo demonio para procesar la copia de archivos sin bloquear
        la interfaz de usuario. Actualiza la barra de progreso durante la operación.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_copiar_existentes, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de copia para existentes iniciado")

    def mover_existentes(self) -> None:
        """Inicia el proceso asíncrono de movimiento de archivos existentes.

        Crea un hilo demonio para procesar el movimiento de archivos sin bloquear
        la interfaz de usuario. Los archivos se mueven a ruta_destino.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_mover_existentes, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de movimiento para existentes iniciado")

    def eliminar_existentes(self) -> None:
        """Inicia el proceso asíncrono de eliminación de archivos existentes.

        Crea un hilo demonio para procesar la eliminación de archivos sin bloquear
        la interfaz de usuario. Los archivos se eliminarán permanentemente.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_eliminar_existentes, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de eliminación para existentes iniciado")

    def papelera_existentes(self) -> None:
        """Inicia el proceso asíncrono de envío a papelera de archivos existentes.

        Crea un hilo demonio para procesar el envío a papelera sin bloquear
        la interfaz de usuario. Los archivos se pueden recuperar desde papelera.
        """
        hilo_trabajo: threading.Thread = threading.Thread(
            target=self._procesar_y_papelera_existentes, daemon=True
        )
        hilo_trabajo.start()
        logger.debug("Hilo de papelera para existentes iniciado")

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
                logger.debug(f"Datos cargados: {len(self.dict_data)} elementos existentes")
            else:
                logger.warning("No hay elementos en la tabla de existentes")

        except Exception as e:
            logger.error(f"Error al cargar datos de tabla: {e}")
            self.label_progreso.config(text="❌ Error al cargar datos")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas - Procesamiento en Hilo
    # └────────────────────────────────────────────────────────────┘

    def _procesar_y_copiar_existentes(self) -> None:
        """Procesa la copia de archivos existentes en un hilo separado.

        Itera sobre todos los archivos existentes cargados, copia cada uno
        a la ruta de destino especificada, actualiza la UI con el progreso actual.
        Solo procesa archivos marcados como existentes.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos existentes para copiar")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando copia de {total_datos} archivos existentes")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    existente = True if fila[4] == "🔴 Ya Existe" else False
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"📋 Copiando: {r}"
                        ),
                    )

                    # Realizamos la copia si el archivo existe
                    if existente:
                        self._copiar(ruta_origen=nombre_archivo)
                        logger.debug(f"✓ Copiado existente: {nombre_archivo}")

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                except Exception as e:
                    logger.error(f"Error copiando archivo existente {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Copia de existentes completada")
            logger.info("Proceso de copia de existentes finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de copia de existentes: {e}")
            self.label_progreso.config(text="❌ Error en la copia")
            self.progress_bar.config(value=0)

    def _procesar_y_mover_existentes(self) -> None:
        """Procesa el movimiento de archivos existentes en un hilo separado.

        Itera sobre todos los archivos existentes cargados, mueve cada uno
        a la ruta de destino especificada, actualiza la UI y elimina las filas.
        Solo procesa archivos marcados como existentes.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos existentes para mover")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando movimiento de {total_datos} archivos existentes")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    existente = True if fila[4] == "🔴 Ya Existe" else False
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"➡️ Moviendo: {r}"
                        ),
                    )

                    # Realizamos el movimiento si el archivo existe
                    if existente:
                        self._mover(ruta_origen=nombre_archivo)
                        logger.debug(f"✓ Movido existente: {nombre_archivo}")

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                    # Eliminamos la fila del archivo
                    self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

                except Exception as e:
                    logger.error(f"Error moviendo archivo existente {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Movimiento de existentes completado")
            logger.info("Proceso de movimiento de existentes finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de movimiento de existentes: {e}")
            self.label_progreso.config(text="❌ Error en el movimiento")
            self.progress_bar.config(value=0)

    def _procesar_y_eliminar_existentes(self) -> None:
        """Procesa la eliminación de archivos existentes en un hilo separado.

        Itera sobre todos los archivos existentes cargados, elimina cada uno
        permanentemente, actualiza la UI y elimina las filas de la tabla.
        Solo procesa archivos marcados como existentes.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos existentes para eliminar")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando eliminación de {total_datos} archivos existentes")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    existente = True if fila[4] == "🔴 Ya Existe" else False
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"🗑️ Eliminando: {r}"
                        ),
                    )

                    # Realizamos la eliminación si el archivo existe
                    if existente:
                        self._eliminar(ruta_origen=nombre_archivo)
                        logger.debug(f"✓ Eliminado existente: {nombre_archivo}")

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                    # Eliminamos la fila del archivo
                    self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

                except Exception as e:
                    logger.error(f"Error eliminando archivo existente {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Eliminación de existentes completada")
            logger.info("Proceso de eliminación de existentes finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de eliminación de existentes: {e}")
            self.label_progreso.config(text="❌ Error en la eliminación")
            self.progress_bar.config(value=0)

    def _procesar_y_papelera_existentes(self) -> None:
        """Procesa el envío a papelera de archivos existentes en un hilo separado.

        Itera sobre todos los archivos existentes cargados, envía cada uno a papelera,
        actualiza la UI y elimina las filas de la tabla.
        Solo procesa archivos marcados como existentes.
        """
        try:
            # Cargamos los datos
            self._load_data()

            if not self.dict_data:
                logger.warning("No hay archivos existentes para enviar a papelera")
                self.label_progreso.config(text="❌ No hay archivos seleccionados")
                return

            total_datos = len(self.dict_data)
            logger.info(f"Iniciando envío a papelera de {total_datos} archivos existentes")

            # Configuramos el proceso inicial
            self.table_view.after(0, lambda: self.progress_bar.config(maximum=total_datos, value=0))

            # Recorremos los datos y procesamos cada uno
            for i, item in enumerate(self.dict_data.keys()):
                try:
                    fila = self.dict_data[item]
                    existente = True if fila[4] == "🔴 Ya Existe" else False
                    nombre_archivo = fila[6] if len(fila) > 6 else str(item)

                    self.table_view.after(
                        0,
                        lambda r=nombre_archivo: self.label_progreso.config(
                            text=f"♻️ Papelera: {r}"
                        ),
                    )

                    # Realizamos envío a papelera si el archivo existe
                    if existente:
                        self._papelera(ruta_origen=nombre_archivo)
                        logger.debug(f"✓ Enviado a papelera existente: {nombre_archivo}")

                    # Actualizamos la barra de progreso
                    self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

                    # Eliminamos la fila del archivo
                    self.table_view.after(0, lambda it=item: self.table_view.view.delete(it))

                except Exception as e:
                    logger.error(f"Error enviando a papelera {item}: {e}")
                    continue

            # Finalizamos el proceso
            self._proceso_finalizado(tipo_proceso="✅ Papelera de existentes completada")
            logger.info("Proceso de papelera de existentes finalizado")

        except Exception as e:
            logger.error(f"Error en proceso de papelera de existentes: {e}")
            self.label_progreso.config(text="❌ Error en papelera")
            self.progress_bar.config(value=0)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas - Operaciones de Archivo
    # └────────────────────────────────────────────────────────────┘

    def _papelera(self, ruta_origen: str) -> None:
        """Envía un archivo existente a la papelera del sistema.

        Args:
            ruta_origen: Ruta completa del archivo a enviar a papelera

        Raises:
            Exception: Si ocurre un error durante la operación de papelera
        """
        try:
            time.sleep(2)
            papelera_archivo(ruta_origen=ruta_origen)
            logger.debug(f"Archivo existente enviado a papelera: {ruta_origen}")
        except Exception as e:
            logger.error(f"Error al enviar a papelera {ruta_origen}: {e}")
            raise

    def _eliminar(self, ruta_origen: str) -> None:
        """Elimina un archivo existente permanentemente.

        Args:
            ruta_origen: Ruta completa del archivo a eliminar

        Raises:
            Exception: Si ocurre un error durante la eliminación
        """
        try:
            time.sleep(2)
            eliminar_archivo(ruta_destino=ruta_origen)
            logger.debug(f"Archivo existente eliminado: {ruta_origen}")
        except Exception as e:
            logger.error(f"Error al eliminar {ruta_origen}: {e}")
            raise

    def _copiar(self, ruta_origen: str) -> None:
        """Copia un archivo existente a la ruta de destino especificada.

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
            logger.debug(f"Archivo existente copiado: {ruta_origen} → {ruta_dest}")
        except Exception as e:
            logger.error(f"Error al copiar {ruta_origen}: {e}")
            raise

    def _mover(self, ruta_origen: str) -> None:
        """Mueve un archivo existente a la ruta de destino especificada.

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
            logger.debug(f"Archivo existente movido: {ruta_origen} → {ruta_dest}")
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
