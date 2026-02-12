from ttkbootstrap import (
    Frame,
    LabelFrame,
    StringVar,
    Separator,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from models.controllers.controlar_visualizar_biblioteca import (
    ControlarVisualizarBiblioteca,
)
from views.components.smart_table_frame import SmartTableFrame
from views.components.ui_tokens import PADDING_OUTER, PADDING_PANEL


class FrameVisualizarBiblioteca(Frame):
    """
    Frame que permite buscar y visualizar datos bibliográficos de los documentos.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # --- Variables ---
        self.var_buscar = StringVar()
        self.campos_busqueda = ["Título", "Autores", "Editorial", "ISBN"]
        self.coldata = [
            {"text": "ID Doc", "stretch": False, "width": 40},
            {"text": "Tipo", "stretch": False, "width": 40},
            {"text": "Título", "stretch": False},
            {"text": "Autores", "stretch": False},
            {"text": "Año", "stretch": False, "width": 60},
            {"text": "Editorial", "stretch": False},
            {"text": "ISBN", "stretch": False},
            # Columnas ocultas para datos extra
            {"text": "nombre_doc", "stretch": False, "width": 0},
            {"text": "extension_doc", "stretch": False, "width": 0},
        ]

        # --- Creación de Widgets ---
        self.crear_widgets()

        # --- Instanciar Controlador ---
        self.controlador = ControlarVisualizarBiblioteca(
            table_view=self.table_view,
            ent_buscar=self.ent_buscar,
            cbx_campos=self.cbx_campos,
            btn_buscar=self.btn_buscar,
            master=self,
        )

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        frame_principal = LabelFrame(self, text="Búsqueda Bibliográfica", padding=PADDING_PANEL)
        frame_principal.pack(fill=BOTH, expand=True, padx=PADDING_OUTER, pady=PADDING_OUTER)

        Separator(frame_principal, orient=HORIZONTAL).pack(fill=X, pady=PADDING_PANEL)

        self.smart_table = SmartTableFrame(
            master=frame_principal,
            coldata=self.coldata,
            search_fields=self.campos_busqueda,
            var_buscar=self.var_buscar,
            on_search=self.on_buscar,
            on_refresh=self.actualizar_tabla,
            show_refresh=True,
            paginated=True,
            searchable=False,
            autofit=True,
            bootstyle=PRIMARY,
        )
        self.smart_table.pack(fill=BOTH, expand=True)

        self.ent_buscar = self.smart_table.ent_buscar
        self.cbx_campos = self.smart_table.cbx_campos
        self.btn_buscar = self.smart_table.btn_buscar
        self.btn_refrescar = self.smart_table.btn_refrescar
        self.table_view = self.smart_table.table_view

        ToolTip(self.ent_buscar, "Escribe aquí para buscar y presiona Enter")
        ToolTip(self.cbx_campos, "Selecciona en qué campo buscar")
        ToolTip(self.btn_buscar, "Realizar la búsqueda bibliográfica")
        ToolTip(self.table_view.view, "Doble clic en un resultado para abrir el documento.")

    def actualizar_tabla(self):
        """
        Refrescar los datos de la tabla bibliográfica.

        Nota: El refrescado es manejado automáticamente por el controlador
        cuando hay cambios en la búsqueda.
        """
        if hasattr(self, "controlador"):
            self.controlador.recargar_resultados()

    def on_buscar(self):
        if hasattr(self, "controlador"):
            self.controlador.on_buscar()

    def _crear_menu_contextual_tabla(self):
        pass
