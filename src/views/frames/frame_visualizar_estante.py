from ttkbootstrap import Frame, Entry, Combobox, Button, StringVar, Label, Separator
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *

# Import the new controller
from models.controllers.controlar_visualizar_estante import ControlarVisualizarEstante


class FrameVisualizarEstante(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master,
            **kwargs,
        )

        # --- Variables ---
        self.var_buscar = StringVar()
        self.campos_busqueda = [
            "Todo",
            "Nombre",
            "Título",
            "Autores",
            "Editorial",
            "ISBN",
            "Colección",
            "Grupo",
        ]
        self.map_documentos = {}

        # --- Mapas para el controlador ---
        self.map_widgets = {}  # Initialize empty, populate after widgets are created
        self.map_vars = {
            "var_buscar": self.var_buscar,
        }

        self._crear_widgets()  # Creates widgets and populates self.map_widgets

        # --- Instanciar Controlador ---
        ControlarVisualizarEstante(
            master=self,
            map_widgets=self.map_widgets,
            map_vars=self.map_vars,
            map_documentos=self.map_documentos,
            scroll_frame=self.scroll_frame,
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def _crear_widgets(self):
        # frame superior
        frame_superior = Frame(self, padding=(1, 1))
        self._panel_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)

        # frame central
        frame_central = Frame(self, padding=(1, 1))
        self._panel_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)

        # frame inferior
        frame_inferior = Frame(self, padding=(1, 1))
        self._panel_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)

        # Populate map_widgets after all widgets are created
        self.map_widgets = {
            "ent_buscar": self.ent_buscar,
            "cbx_campos": self.cbx_campos,
            "btn_buscar": self.btn_buscar,
        }

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Superior
    # └────────────────────────────────────────────────────────────┘

    def _panel_superior(self, frame: Frame):
        lbl_titulo = Label(
            frame, text="📚 Estante de la Biblioteca", font=("Helvetica", 14, "bold")
        )
        lbl_titulo.pack(side=TOP, fill=X, padx=10, pady=(5, 10))

        Separator(frame, orient=HORIZONTAL).pack(fill=X, padx=5, pady=(0, 5))

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Central
    # └────────────────────────────────────────────────────────────┘

    def _panel_central(self, frame: Frame):
        self.scroll_frame = ScrolledFrame(frame, padding=(1, 1), bootstyle="dark")
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Inferior
    # └────────────────────────────────────────────────────────────┘

    def _panel_inferior(self, frame: Frame):
        frame_busqueda = Frame(frame)
        frame_busqueda.pack(fill=X, padx=5, pady=5)

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
        ToolTip(self.btn_buscar, "Realizar la búsqueda en el estante")
