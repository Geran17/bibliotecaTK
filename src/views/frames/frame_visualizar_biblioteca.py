from ttkbootstrap import (
    Frame,
    LabelFrame,
    Entry,
    Combobox,
    Button,
    StringVar,
    Separator,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from models.controllers.controlar_visualizar_biblioteca import (
    ControlarVisualizarBiblioteca,
)


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
        ControlarVisualizarBiblioteca(
            table_view=self.table_view,
            ent_buscar=self.ent_buscar,
            cbx_campos=self.cbx_campos,
            btn_buscar=self.btn_buscar,
            master=self,
        )

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        frame_principal = LabelFrame(self, text="Búsqueda Bibliográfica", padding=5)
        frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # --- Frame para la búsqueda ---
        frame_busqueda = Frame(frame_principal)
        frame_busqueda.pack(fill=X, pady=(0, 5))

        self.ent_buscar = Entry(frame_busqueda, textvariable=self.var_buscar)
        self.ent_buscar.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        ToolTip(self.ent_buscar, "Escribe aquí para buscar y presiona Enter")

        self.cbx_campos = Combobox(
            frame_busqueda, values=self.campos_busqueda, state=READONLY, width=12
        )
        self.cbx_campos.current(0)
        self.cbx_campos.pack(side=LEFT, padx=5)
        ToolTip(self.cbx_campos, "Selecciona en qué campo buscar")

        self.btn_buscar = Button(frame_busqueda, text="Buscar", style="primary")
        self.btn_buscar.pack(side=LEFT)
        ToolTip(self.btn_buscar, "Realizar la búsqueda bibliográfica")

        Separator(frame_principal, orient=HORIZONTAL).pack(fill=X, pady=5)

        # --- Tabla de Resultados ---
        self.table_view = Tableview(
            master=frame_principal,
            coldata=self.coldata,
            paginated=True,
            searchable=False,
            autofit=True,
            bootstyle=PRIMARY,
        )
        self.table_view.pack(fill=BOTH, expand=True)
        ToolTip(self.table_view.view, "Doble clic en un resultado para abrir el documento.")
