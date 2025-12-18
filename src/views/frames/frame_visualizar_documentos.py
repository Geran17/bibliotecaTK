from ttkbootstrap import (
    Frame,
    PanedWindow,
    Notebook,
    Treeview,
    Label,
    Entry,
    Button,
    Combobox,
    StringVar,
    LabelFrame,
    Separator,
)
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from models.controllers.controlar_visualizacion_documentos import (
    ControlarVisualizacionDocumentos,
)


class FrameVisualizarDocumentos(Frame):
    """
    Frame principal para la visualización y organización de documentos.

    Contiene un panel izquierdo con un Notebook para organizar por categorías
    (colecciones, grupos, etc.) y un panel derecho para buscar y mostrar
    los documentos en una tabla.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # --- Estilos ---
        self.estilo = Style()
        # El nombre del estilo base para un PanedWindow es 'TPanedwindow'
        self.estilo.configure("Separador.TPanedwindow", sashwidth=10)
        # Estilo para poner las pestañas del Notebook a la izquierda
        self.estilo.configure(
            "Left.TNotebook", tabposition="sn"
        )  # 'ws' es west-south (izquierda, texto vertical)

        # --- Mapas para el controlador ---
        self.map_treeviews = {}
        self.map_widgets = {}

        # --- Iconos para las pestañas ---
        self.map_iconos_tabs = {
            "Colecciones": "📚",
            "Grupos": "🗂️",
            "Categorías": "🗃️",
            "Etiquetas": "🏷️",
            "Palabras Clave": "🔑",
        }
        # --- Variables ---
        self.var_buscar = StringVar()
        self.campos_busqueda = ["Todo", "Nombre"]
        self.coldata = [
            {"text": "Id", "stretch": False, "width": 50},
            {"text": "Tipo", "stretch": False, "width": 40},
            {"text": "Nombre", "stretch": False},
            {"text": "Ext", "stretch": False, "width": 50},
            {"text": "Tamaño", "stretch": False, "width": 80},
            {"text": "Creado", "stretch": False},
            {"text": "Actualizado", "stretch": False},
        ]

        # --- Creación de Widgets ---
        self.crear_widgets()

        # --- Preparar mapas para el controlador ---
        self.map_widgets = {
            "treeviews": self.map_treeviews,
            "table_view": self.table_view,
            "ent_buscar": self.ent_buscar,
            "cbx_campos": self.cbx_campos,
            "btn_buscar": self.btn_buscar,
            "btn_refrescar": self.btn_refrescar,
        }
        map_vars = {"var_buscar": self.var_buscar}

        # --- Instanciar Controlador ---
        ControlarVisualizacionDocumentos(
            master=self, map_widgets=self.map_widgets, map_vars=map_vars
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Creación de Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        paned_window = PanedWindow(self, orient=HORIZONTAL, style="Separador.TPanedwindow")
        paned_window.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # --- Panel Izquierdo (Organización) ---
        frame_izquierdo = LabelFrame(paned_window, text="📚 Organización", padding=5)
        self.panel_izquierdo(frame=frame_izquierdo)
        paned_window.add(frame_izquierdo, weight=1)

        # --- Panel Derecho (Documentos) ---
        frame_derecho = LabelFrame(paned_window, text="📜 Documentos", padding=5)
        self.panel_derecho(frame=frame_derecho)
        paned_window.add(frame_derecho, weight=4)

    def panel_izquierdo(self, frame: Frame):
        """Crea el Notebook con Treeviews para la organización."""
        notebook_organizacion = Notebook(frame, style="Left.TNotebook")
        notebook_organizacion.pack(fill=BOTH, expand=True, pady=(0, 5))

        # Pestañas para cada tipo de organización
        for nombre_tab, icono in self.map_iconos_tabs.items():
            self.map_treeviews[nombre_tab] = self._crear_tab_organizacion(
                notebook=notebook_organizacion, nombre_tab=nombre_tab, icono=icono
            )

        self.btn_refrescar = Button(frame, text="🔄 Refrescar", style="secondary-toolbutton")
        self.btn_refrescar.pack(side=BOTTOM, fill=X, padx=2, pady=(5, 0))
        ToolTip(self.btn_refrescar, "Recargar los datos de la organización")

    def _crear_tab_organizacion(
        self, notebook: Notebook, nombre_tab: str, icono: str = ""
    ) -> Treeview:
        """Crea una pestaña con un Treeview dentro del Notebook."""
        tab = Frame(notebook, padding=2)
        texto_tab = f"{icono} {nombre_tab}" if icono else nombre_tab
        notebook.add(tab, text=texto_tab)

        tree = Treeview(tab, columns=("nombre"), show="tree")
        tree.heading("#0", text=nombre_tab)
        tree.pack(fill=BOTH, expand=True)
        return tree

    def panel_derecho(self, frame: Frame):
        """Crea el panel de búsqueda y la tabla de documentos."""
        # --- Frame para la búsqueda ---
        frame_busqueda = Frame(frame)
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
        ToolTip(self.btn_buscar, "Realizar la búsqueda de documentos")

        # --- Separador ---
        Separator(frame, orient=HORIZONTAL).pack(fill=X, pady=5)

        # --- Tabla de Documentos ---
        self.table_view = Tableview(
            master=frame,
            coldata=self.coldata,
            paginated=True,
            searchable=False,  # La búsqueda se maneja con los widgets de arriba
            autofit=True,
            bootstyle=PRIMARY,
        )
        self.table_view.pack(fill=BOTH, expand=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos (a implementar)
    # └────────────────────────────────────────────────────────────┘

    def on_buscar_documentos(self):
        """Lógica para buscar documentos y poblar la tabla."""
        pass
