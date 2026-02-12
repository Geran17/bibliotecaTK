import math
from os.path import exists
from tkinter.messagebox import showerror
from tkinter import Menu
from typing import Dict, Any, List

from ttkbootstrap import Button
from ttkbootstrap.tableview import Tableview

from models.controllers.configuracion_controller import ConfiguracionController
from models.controllers.controlar_menu_contextual_documento import (
    ControlarMenuContextualDocumento,
)
from models.entities.consulta import Consulta
from utilities.auxiliar import (
    abrir_documento_desde_biblioteca,
)


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

        self.menu_ops = ControlarMenuContextualDocumento(
            master=self.master,
            get_documento_data=self._get_documento_contextual,
            on_refresh=self.cargar_favoritos,
        )
        self._vincular_eventos()
        self._crear_menu_contextual()
        self.cargar_favoritos()

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a sus manejadores."""
        self.btn_refrescar.config(command=self.cargar_favoritos)
        self.table_view.view.bind("<Double-1>", self.on_doble_clic_tabla)
        self.table_view.view.bind("<Button-3>", self._mostrar_menu_contextual)

    def _crear_menu_contextual(self):
        self.menu_contextual = Menu(self.master, tearoff=0)
        self.menu_contextual.add_command(label="📖 Abrir documento", command=self.menu_ops.on_abrir_documento)
        self.menu_contextual.add_command(label="📂 Abrir carpeta", command=self.menu_ops.on_abrir_carpeta)
        self.menu_contextual.add_command(label="ℹ️ Propiedades", command=self.menu_ops.on_propiedades)
        self.menu_contextual.add_command(label="🧾 Ver metadatos", command=self.menu_ops.on_ver_metadatos)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="✏️ Renombrar documento", command=self.menu_ops.on_renombrar_documento)
        self.menu_contextual.add_command(label="🧬 Renombrar bibliográficamente", command=self.menu_ops.on_renombrar_bibliografico)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="📋 Copiar documento", command=self.menu_ops.on_copiar_documento)
        self.menu_contextual.add_command(label="✂️ Mover documento", command=self.menu_ops.on_mover_documento)
        self.menu_contextual.add_command(label="🗑️ Enviar a papelera", command=self.menu_ops.on_enviar_papelera)
        self.menu_contextual.add_command(label="🗑️ Eliminar documento", command=self.menu_ops.on_eliminar_documento)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="🔄 Cambiar estado", command=self.menu_ops.on_cambiar_estado)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="🔄 Refrescar", command=self.cargar_favoritos)

    def _mostrar_menu_contextual(self, event):
        item_id = self.table_view.view.identify_row(event.y)
        if item_id:
            self.table_view.view.selection_set(item_id)
            self.table_view.view.focus(item_id)
        self.menu_contextual.tk_popup(event.x_root, event.y_root)

    def _get_documento_contextual(self):
        selected_row = self.table_view.get_rows(selected=True)
        if not selected_row or not selected_row[0].values:
            return None
        id_documento = selected_row[0].values[0]
        return self.map_documentos.get(id_documento)

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

        ok, error = abrir_documento_desde_biblioteca(
            id_documento=id_documento,
            nombre_documento=documento_data["nombre"],
            extension_documento=documento_data["extension"],
            ruta_biblioteca=ruta_biblioteca,
        )
        if not ok:
            showerror(title="Error al abrir", message=error, parent=self.master)

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
