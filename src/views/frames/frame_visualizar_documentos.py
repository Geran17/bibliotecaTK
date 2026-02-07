from ttkbootstrap import (
    Frame,
    PanedWindow,
    Notebook,
    Treeview,
    Label,
    Button,
    StringVar,
    LabelFrame,
    Separator,
)
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from ttkbootstrap.tooltip import ToolTip
from models.controllers.controlar_visualizacion_documentos import (
    ControlarVisualizacionDocumentos,
)
from views.components.smart_table_frame import SmartTableFrame
from views.components.context_menu_factory import ContextMenuFactory
from views.components.ui_tokens import PADDING_COMPACT, PADDING_OUTER, PADDING_PANEL


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
        self.controlador = ControlarVisualizacionDocumentos(
            master=self, map_widgets=self.map_widgets, map_vars=map_vars
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Creación de Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        paned_window = PanedWindow(self, orient=HORIZONTAL, style="Separador.TPanedwindow")
        paned_window.pack(fill=BOTH, expand=True, padx=PADDING_OUTER, pady=PADDING_OUTER)

        # --- Panel Izquierdo (Organización) ---
        frame_izquierdo = LabelFrame(paned_window, text="📚 Organización", padding=PADDING_PANEL)
        self.panel_izquierdo(frame=frame_izquierdo)
        paned_window.add(frame_izquierdo, weight=1)

        # --- Panel Derecho (Documentos) ---
        frame_derecho = LabelFrame(paned_window, text="📜 Documentos", padding=PADDING_PANEL)
        self.panel_derecho(frame=frame_derecho)
        paned_window.add(frame_derecho, weight=4)

    def panel_izquierdo(self, frame: Frame):
        """Crea el Notebook con Treeviews para la organización."""
        notebook_organizacion = Notebook(frame, style="Left.TNotebook")
        notebook_organizacion.pack(fill=BOTH, expand=True, pady=(0, PADDING_OUTER))

        # Pestañas para cada tipo de organización
        for nombre_tab, icono in self.map_iconos_tabs.items():
            self.map_treeviews[nombre_tab] = self._crear_tab_organizacion(
                notebook=notebook_organizacion, nombre_tab=nombre_tab, icono=icono
            )

        self.btn_refrescar = Button(frame, text="🔄 Refrescar", style="secondary-toolbutton")
        self.btn_refrescar.pack(side=BOTTOM, fill=X, padx=PADDING_COMPACT, pady=(PADDING_OUTER, 0))
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
        Separator(frame, orient=HORIZONTAL).pack(fill=X, pady=5)

        self.smart_table = SmartTableFrame(
            master=frame,
            coldata=self.coldata,
            search_fields=self.campos_busqueda,
            var_buscar=self.var_buscar,
            show_refresh=True,
            on_search=self.on_buscar_documentos,
            on_refresh=self.actualizar_tabla,
            paginated=True,
            searchable=False,
            autofit=True,
            bootstyle=PRIMARY,
        )
        self.smart_table.pack(fill=BOTH, expand=True)

        self.ent_buscar = self.smart_table.ent_buscar
        self.cbx_campos = self.smart_table.cbx_campos
        self.btn_buscar = self.smart_table.btn_buscar
        self.btn_refrescar_tabla = self.smart_table.btn_refrescar
        self.table_view = self.smart_table.table_view

        ToolTip(self.ent_buscar, "Escribe aquí para buscar y presiona Enter")
        ToolTip(self.cbx_campos, "Selecciona en qué campo buscar")
        ToolTip(self.btn_buscar, "Realizar la búsqueda de documentos")
        self._crear_menu_contextual_tabla()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos (a implementar)
    # └────────────────────────────────────────────────────────────┘

    def on_buscar_documentos(self):
        """Lógica para buscar documentos y poblar la tabla."""
        if hasattr(self, "controlador"):
            self.controlador.on_buscar_documentos()

    def actualizar_tabla(self):
        """
        Refrescar los datos de la tabla de documentos.

        Nota: El refrescado es manejado automáticamente por el controlador
        cuando hay cambios en la búsqueda o selección de elementos.
        """
        if hasattr(self, "controlador"):
            self.controlador.recargar_datos()

    def _crear_menu_contextual_tabla(self):
        acciones = [
            {
                "label": "📖 Abrir documento",
                "command": lambda: self.controlador.on_doble_clic_tabla_documentos(None),
            },
            {"label": "🔎 Buscar", "command": self.on_buscar_documentos},
            {"separator": True},
            {"label": "🔄 Refrescar", "command": self.actualizar_tabla},
        ]
        self.menu_contextual_tabla = ContextMenuFactory.build_for_treeview(
            master=self,
            treeview=self.table_view.view,
            actions=acciones,
        )
