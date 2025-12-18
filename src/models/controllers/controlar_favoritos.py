import math
from os.path import join, exists
from tkinter.messagebox import showerror
from typing import Dict, Any, List

from ttkbootstrap import Button
from ttkbootstrap.tableview import Tableview

from models.controllers.configuracion_controller import ConfiguracionController
from models.entities.consulta import Consulta
from utilities.auxiliar import (
    generar_ruta_documento,
    copiar_archivo,
    abrir_archivo,
)
from utilities.configuracion import DIRECTORIO_TEMPORAL


class ControlarFavoritos:
    """
    Controlador para la lógica de la vista de documentos favoritos.
    """

    def __init__(self, table_view: Tableview, btn_refrescar: Button, master):
        self.table_view = table_view
        self.btn_refrescar = btn_refrescar
        self.master = master

        self.map_documentos: Dict[int, Dict[str, Any]] = {}
        self.icon_libro = "📕"

        self._vincular_eventos()
        self.cargar_favoritos()

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a sus manejadores."""
        self.btn_refrescar.config(command=self.cargar_favoritos)
        self.table_view.view.bind("<Double-1>", self.on_doble_clic_tabla)

    def cargar_favoritos(self):
        """Obtiene los documentos favoritos de la BD y los puebla en la tabla."""
        favoritos = Consulta().get_documentos_favoritos()
        self.map_documentos = {doc["id"]: doc for doc in favoritos}
        self._poblar_tabla(favoritos)

    def _poblar_tabla(self, lista_documentos: List[Dict[str, Any]]):
        """Limpia y puebla la tabla con una lista de documentos."""
        self.table_view.delete_rows()
        if not lista_documentos:
            return

        coldata = self.master.coldata
        row_data = [self._formatear_fila_documento(doc) for doc in lista_documentos]

        self.table_view.build_table_data(coldata, row_data)
        self.table_view.autofit_columns()

    def on_doble_clic_tabla(self, event=None):
        """Abre el archivo correspondiente al hacer doble clic en la tabla."""
        selected_row = self.table_view.get_rows(selected=True)
        if not selected_row:
            return

        id_documento = selected_row[0].values[0]
        documento_data = self.map_documentos.get(id_documento)

        if not documento_data:
            showerror(
                title="Error",
                message="No se encontró la información del documento.",
                parent=self.master,
            )
            return

        config = ConfiguracionController()
        ruta_biblioteca = config.obtener_ubicacion_biblioteca()
        if not ruta_biblioteca or not exists(ruta_biblioteca):
            showerror(
                title="Error",
                message="La ubicación de la biblioteca no está configurada o no existe.",
            )
            return

        nombre_archivo = f"{documento_data['nombre']}.{documento_data['extension']}"
        ruta_origen = generar_ruta_documento(
            ruta_biblioteca=ruta_biblioteca,
            id_documento=id_documento,
            nombre_documento=nombre_archivo,
        )

        if not exists(ruta_origen):
            showerror(
                title="Archivo no encontrado",
                message=f"El archivo no se encontró en la biblioteca:\n{ruta_origen}",
            )
            return

        ruta_destino_temporal = join(DIRECTORIO_TEMPORAL, nombre_archivo)
        try:
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino_temporal)
            abrir_archivo(ruta_origen=ruta_destino_temporal)
        except Exception as e:
            showerror(title="Error al abrir", message=f"No se pudo abrir el documento: {e}")

    def _formatear_fila_documento(self, doc: Dict[str, Any]) -> list:
        """Formatea un diccionario de documento a una lista para la tabla."""
        return [
            doc.get("id", "-"),
            self.icon_libro,
            doc.get("nombre", "N/A"),
            doc.get("extension", ""),
            self._formatear_tamano(doc.get("tamano", 0)),
            doc.get("creado_en", "-"),
            doc.get("actualizado_en", "-"),
        ]

    def _formatear_tamano(self, bytes_size: int) -> str:
        """Formatea el tamaño de un archivo de bytes a una unidad legible."""
        if not isinstance(bytes_size, (int, float)) or bytes_size <= 0:
            return "0 B"
        unidades = ["B", "KB", "MB", "GB", "TB"]
        indice = int(math.log(bytes_size, 1024))
        valor = bytes_size / (1024**indice)
        return f"{valor:.2f} {unidades[indice]}"
