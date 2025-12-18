from ttkbootstrap import (
    Frame,
    LabelFrame,
    Entry,
    Button,
    StringVar,
    Separator,
    Treeview,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from models.controllers.controlar_visualizar_contenido import (
    ControlarVisualizarContenido,
)


class FrameVisualizarContenido(Frame):
    """
    Frame que permite buscar en el contenido (capítulos y secciones) de los documentos.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # --- Variables ---
        self.var_buscar = StringVar()

        # --- Creación de Widgets ---
        self.crear_widgets()

        # --- Instanciar Controlador ---
        ControlarVisualizarContenido(
            tree_view=self.tree_view,
            ent_buscar=self.ent_buscar,
            btn_buscar=self.btn_buscar,
            master=self,
        )

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        frame_principal = LabelFrame(self, text="Búsqueda en Contenido", padding=5)
        frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # --- Frame para la búsqueda ---
        frame_busqueda = Frame(frame_principal)
        frame_busqueda.pack(fill=X, pady=(0, 5))

        self.ent_buscar = Entry(frame_busqueda, textvariable=self.var_buscar)
        self.ent_buscar.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        ToolTip(
            self.ent_buscar,
            "Busca en títulos de capítulos y secciones. Presiona Enter para buscar.",
        )

        self.btn_buscar = Button(frame_busqueda, text="Buscar", style="primary")
        self.btn_buscar.pack(side=LEFT)
        ToolTip(self.btn_buscar, "Realizar la búsqueda en el contenido")

        Separator(frame_principal, orient=HORIZONTAL).pack(fill=X, pady=5)

        # --- Treeview para Resultados ---
        self.tree_view = Treeview(
            master=frame_principal,
            columns=("tipo", "titulo", "pagina"),
            show="tree headings",
            bootstyle=PRIMARY,
        )
        self.tree_view.pack(fill=BOTH, expand=True)

        # Configuración de encabezados y columnas
        self.tree_view.heading("#0", text="Documento / Contenido", anchor=W)
        self.tree_view.heading("tipo", text="Tipo", anchor=W)
        self.tree_view.heading("titulo", text="Título", anchor=W)
        self.tree_view.heading("pagina", text="Página", anchor=E)

        self.tree_view.column("#0", stretch=True, width=300)
        self.tree_view.column("tipo", stretch=False, width=80)
        self.tree_view.column("titulo", stretch=True, width=300)
        self.tree_view.column("pagina", stretch=False, width=60, anchor=E)

        ToolTip(self.tree_view, "Doble clic en un resultado para abrir el documento.")
