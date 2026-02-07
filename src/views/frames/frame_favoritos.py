from ttkbootstrap import Frame, LabelFrame, Button
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from models.controllers.controlar_favoritos import ControlarFavoritos


class FrameFavoritos(Frame):
    """
    Frame que muestra los documentos marcados como favoritos.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.coldata = [
            {"text": "Id", "stretch": False, "width": 50},
            {"text": "Tipo", "stretch": False, "width": 40},
            {"text": "Nombre", "stretch": True},
            {"text": "Ext", "stretch": False, "width": 50},
            {"text": "Tamaño", "stretch": False, "width": 80},
            {"text": "Creado", "stretch": False},
            {"text": "Actualizado", "stretch": False},
        ]

        # --- Creación de Widgets ---
        self.crear_widgets()

        # --- Instanciar Controlador ---
        ControlarFavoritos(
            table_view=self.table_view,
            btn_refrescar=self.btn_refrescar,
            master=self,
        )

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        frame_principal = LabelFrame(self, text="Documentos Favoritos", padding=5)
        frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # --- Botón de Refrescar ---
        self.btn_refrescar = Button(
            frame_principal, text="🔄 Refrescar Favoritos", style="secondary-toolbutton"
        )
        self.btn_refrescar.pack(side=TOP, fill=X, padx=2, pady=(0, 5))
        ToolTip(self.btn_refrescar, "Vuelve a cargar la lista de documentos favoritos")

        # --- Tabla de Documentos ---
        self.table_view = Tableview(
            master=frame_principal,
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
        Refrescar los datos de la tabla de favoritos.
        Invoca el botón de refrescar para recargar los datos.
        """
        try:
            if hasattr(self, 'btn_refrescar') and self.btn_refrescar.winfo_exists():
                try:
                    self.btn_refrescar.invoke()
                except Exception:
                    pass
        except Exception:
            pass
