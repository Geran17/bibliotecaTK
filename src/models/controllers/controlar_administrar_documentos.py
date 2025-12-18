import time
from threading import Thread
import math
from os.path import exists
from ttkbootstrap import Label, Progressbar
from ttkbootstrap.tableview import Tableview
from models.entities.consulta import Consulta
from models.entities.documento import Documento
from models.entities.favorito import Favorito
from models.controllers.configuracion_controller import ConfiguracionController
from utilities.auxiliar import generar_ruta_documento
from typing import List, Dict, Any


class ControlarAdministrarDocumentos:
    def __init__(self, lbl_progreso: Label, progress_bar: Progressbar, table_view: Tableview):
        self.lbl_progreso = lbl_progreso
        self.progress_bar = progress_bar
        self.table_view = table_view
        self.encontrados: List[Dict[str, Any]] = []
        self.documentos_seleccionados: List[Documento] = []
        # icons
        # favorito
        self.icon_favorito = "⭐"
        # organizacion
        self.icon_grupo = "🗂️"
        self.icon_coleccion = "📚"
        self.icon_categoria = "🗃️"
        self.icon_etiqueta = "🏷️"
        self.icon_palabra_clave = "🔑"
        # libro
        self.icon_libro = "📕"
        self.icon_metadato = "🧮"
        self.icon_bibliografia = "🧬"
        self.icon_capitulo = "📑"
        # existencia
        self.icon_exclamacion = "❗"  # indica que el archivo no existe en la biblioteca
        self.icon_existe = "✳️"  # indica que el archivo existe en la biblioteca

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Principales
    # └────────────────────────────────────────────────────────────┘

    def ejecutar_encontrados(self):
        hilo_encontrados = Thread(target=self._procesar_encontrados)
        hilo_encontrados.start()

    def buscar_datos(self, campo: str, buscar: str):

        if not campo:
            print("El parametro campo no puede estar vacio")
            return

        if not buscar:
            print("El parametro buscar no puede estar vacio")
            return

        consulta = Consulta()
        if isinstance(consulta, Consulta):
            self.encontrados = consulta.buscar_documentos(campo=campo, buscar=buscar)

    def get_documentos_seleccionados(self) -> List[Documento]:
        lista: List[Documento] = []
        seleccionados = self.table_view.get_rows(selected=True)
        for fila in seleccionados:
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
                documento.instanciar()
                if isinstance(documento, Documento):
                    lista.append(documento)
        return lista

    def controlar_favoritos(self):
        documentos_seleccionados = self.get_documentos_seleccionados()
        if documentos_seleccionados:
            for documento in documentos_seleccionados:
                # creamos el objeto favorito
                favorito = Favorito(id_documento=documento.id)
                if not favorito.existe():
                    favorito.marcar()
                else:
                    favorito.desmarcar()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘

    def _clear_table(self):
        self.table_view.delete_rows()

    def _procesar_encontrados(self):
        # limpiamos la tabla
        self._clear_table()
        # obtenemos el total de encontrados
        total_encontrados = len(self.encontrados)
        self.table_view.after(
            0, lambda: self.progress_bar.config(maximum=total_encontrados, value=0)
        )

        for i, dato in enumerate(self.encontrados):
            # Actualizamos el label
            self.table_view.after(
                0,
                lambda nombre=dato['nombre']: self.lbl_progreso.config(
                    text=f"Procesando: {nombre}"
                ),
            )

            # Fila
            fila = self._generar_fila(dato=dato)
            if fila:
                # Insertamos
                self._insertar_fila(values=fila)

            # Actualizamos el proceso
            self.table_view.after(0, lambda v=i + 1: self.progress_bar.config(value=v))

        # finalizamos
        self._finalizar_carga_gui()

    def _generar_fila(self, dato: Dict) -> List:
        """Esta funcion genera una fila, para insertar en la tabla"""
        if isinstance(dato, Dict):
            activo = "✅" if dato['esta_activo'] else "❎"
            return [
                dato['id'],
                self._get_info(
                    dato=dato
                ),  # info, tenemos que generar una funcion, para esta columna
                self.icon_libro,
                dato['nombre'],
                dato['extension'],
                self._formatear_tamano(dato['tamano']),
                activo,
                dato['creado_en'],
                dato['actualizado_en'],
                dato['hash'],
            ]
        return []

    def _insertar_fila(self, values: list):
        time.sleep(1)
        self.table_view.after(0, self._insert_en_gui, values)

    def _insert_en_gui(self, values: list):
        self.table_view.insert_row(values=values)

    def _get_info(self, dato: Dict) -> str:
        info_parts = []
        if isinstance(dato, Dict):
            # existencia
            if self._existe_documento(dato=dato):
                info_parts.append(self.icon_existe)
            else:
                info_parts.append(self.icon_exclamacion)

            icon_map = {
                'tiene_metadato': self.icon_metadato,
                'es_favorito': self.icon_favorito,
                'tiene_capitulos': self.icon_capitulo,
                'tiene_categoria': self.icon_categoria,
                'tiene_coleccion': self.icon_coleccion,
                'tiene_dato_bibliografico': self.icon_bibliografia,
                'tiene_etiqueta': self.icon_etiqueta,
                'tiene_grupo': self.icon_grupo,
                'tiene_palabra_clave': self.icon_palabra_clave,
            }

            for key, icon in icon_map.items():
                if int(dato.get(key, 0)) == 1:
                    info_parts.append(icon)

        return " ".join(info_parts)

    def _existe_documento(self, dato) -> bool:
        conf = ConfiguracionController()
        ruta_biblioteca = conf.obtener_ubicacion_biblioteca()
        if exists(ruta_biblioteca):
            if isinstance(dato, Dict):
                ruta_documento = generar_ruta_documento(
                    ruta_biblioteca=ruta_biblioteca,
                    nombre_documento=f"{dato['nombre']}.{dato['extension']}",
                    id_documento=dato['id'],
                )
                if exists(ruta_documento):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

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
        indice = min(int(math.log(bytes, 1024)), len(unidades) - 1)

        # Calcular el valor en la unidad correspondiente
        valor = bytes / (1024**indice)

        # Formatear según la unidad
        if indice == 0:  # Bytes
            return f"{int(valor)} B"
        else:
            return f"{valor:.2f} {unidades[indice]}"

    def _finalizar_carga_gui(self):
        self.table_view.autofit_columns()
        self.lbl_progreso.config(text="Carga de encontrados completada.")
