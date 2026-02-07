from ttkbootstrap import Frame, LabelFrame, PanedWindow, PRIMARY, Style
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from tkinter.ttk import Treeview, Scrollbar

from models.controllers.controlar_visor_metadatos import ControlarVisorMetadatos


class FrameVisorMetadatos(Frame):
    """
    Frame que permite explorar los metadatos de los documentos y ver
    qué archivos están asociados a cada clave de metadato.
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

        # --- Definición de columnas para la tabla de documentos ---
        self.coldata = [
            {"text": "ID", "stretch": False, "width": 40},
            {"text": "Tipo", "stretch": False, "width": 40},
            {"text": "Nombre", "stretch": True},
            {"text": "Extensión", "stretch": False, "width": 80},
            {"text": "Tamaño (bytes)", "stretch": False, "width": 120},
        ]

        # --- Creación de Widgets ---
        self.crear_widgets()

        # --- Instanciar Controlador ---
        ControlarVisorMetadatos(
            tree_view=self.tree_metadatos,
            table_view=self.table_view,
            master=self,
        )

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        pane = PanedWindow(self, orient=HORIZONTAL, style="Separador.TPanedwindow")
        pane.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # --- Panel Izquierdo: Treeview de Metadatos ---
        frame_izquierdo = LabelFrame(pane, text="Claves de Metadatos")
        pane.add(frame_izquierdo, weight=1)

        self.tree_metadatos = Treeview(
            frame_izquierdo, columns=("clave_completa", "valor"), displaycolumns=()
        )
        self.tree_metadatos.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar_y = Scrollbar(
            frame_izquierdo, orient="vertical", command=self.tree_metadatos.yview
        )
        scrollbar_y.pack(side=RIGHT, fill="y")
        self.tree_metadatos.configure(yscrollcommand=scrollbar_y.set)

        ToolTip(self.tree_metadatos, "Selecciona una clave para ver los documentos asociados.")

        # --- Panel Derecho: Tabla de Documentos ---
        frame_derecho = LabelFrame(pane, text="Documentos Asociados")
        pane.add(frame_derecho, weight=3)

        self.table_view = Tableview(
            master=frame_derecho,
            coldata=self.coldata,
            paginated=True,
            searchable=True,
            autofit=True,
            bootstyle=PRIMARY,
        )
        self.table_view.pack(fill=BOTH, expand=True)
        ToolTip(self.table_view.view, "Doble clic en un documento para abrirlo.")

    def actualizar_tabla(self):
        """
        Refrescar los datos del visor de metadatos.

        Nota: El refrescado es manejado por el controlador cuando se selecciona
        un elemento en el árbol. No requiere intervención manual.
        """
        # No hacer nada - el controlador maneja la actualización automáticamente
        pass
