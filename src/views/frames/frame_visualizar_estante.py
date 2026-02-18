from ttkbootstrap import Frame, Entry, Combobox, Button, StringVar, Label, Separator
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *

# Import the new controller
from models.controllers.controlar_visualizar_estante import ControlarVisualizarEstante
from views.components.ui_tokens import (
    PADDING_COMPACT,
    PADDING_OUTER,
    PADDING_PANEL,
    FONT_TITLE,
)


class FrameVisualizarEstante(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master,
            **kwargs,
        )

        # --- Variables ---
        self.var_buscar = StringVar()
        self.var_modo_visualizacion = StringVar(value="Cuadrícula")
        self.var_tipo_organizacion = StringVar()
        self.var_organizacion = StringVar()
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
        self.tipos_organizacion = [
            "Colecciones",
            "Grupos",
            "Categorías",
            "Etiquetas",
            "Palabras Clave",
        ]
        self.map_documentos = {}

        # --- Mapas para el controlador ---
        self.map_widgets = {}  # Initialize empty, populate after widgets are created
        self.map_vars = {
            "var_buscar": self.var_buscar,
            "var_modo_visualizacion": self.var_modo_visualizacion,
            "var_tipo_organizacion": self.var_tipo_organizacion,
            "var_organizacion": self.var_organizacion,
        }

        self._crear_widgets()  # Creates widgets and populates self.map_widgets

        # --- Instanciar Controlador ---
        self.controlador = ControlarVisualizarEstante(
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
        frame_superior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self._panel_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        # frame central
        frame_central = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self._panel_central(frame=frame_central)
        frame_central.pack(
            side=TOP,
            fill=BOTH,
            padx=PADDING_COMPACT,
            pady=PADDING_COMPACT,
            expand=TRUE,
        )

        # frame inferior
        frame_inferior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self._panel_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        # Populate map_widgets after all widgets are created
        self.map_widgets = {
            "ent_buscar": self.ent_buscar,
            "cbx_campos": self.cbx_campos,
            "cbx_modo_visualizacion": self.cbx_modo_visualizacion,
            "cbx_tipo_organizacion": self.cbx_tipo_organizacion,
            "cbx_organizacion": self.cbx_organizacion,
            "btn_buscar": self.btn_buscar,
            "btn_anterior": self.btn_anterior,
            "btn_siguiente": self.btn_siguiente,
            "lbl_pagina": self.lbl_pagina,
        }

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Superior
    # └────────────────────────────────────────────────────────────┘

    def _panel_superior(self, frame: Frame):
        frame_header = Frame(frame)
        frame_header.pack(side=TOP, fill=X, padx=PADDING_OUTER, pady=(5, 10))

        lbl_titulo = Label(frame_header, text="📚 Estante de la Biblioteca", font=FONT_TITLE)
        lbl_titulo.pack(side=LEFT, fill=X, expand=True)

        lbl_vista = Label(frame_header, text="Vista:")
        lbl_vista.pack(side=LEFT, padx=(0, PADDING_COMPACT))

        self.cbx_modo_visualizacion = Combobox(
            frame_header,
            values=["Cuadrícula", "Lista"],
            state=READONLY,
            width=12,
            textvariable=self.var_modo_visualizacion,
        )
        self.cbx_modo_visualizacion.current(0)
        self.cbx_modo_visualizacion.pack(side=LEFT)
        ToolTip(
            self.cbx_modo_visualizacion,
            "Cambia cómo se muestran los documentos en el estante",
        )

        Separator(frame, orient=HORIZONTAL).pack(
            fill=X,
            padx=PADDING_OUTER,
            pady=(0, PADDING_OUTER),
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Central
    # └────────────────────────────────────────────────────────────┘

    def _panel_central(self, frame: Frame):
        self.scroll_frame = ScrolledFrame(
            frame,
            padding=(PADDING_COMPACT, PADDING_COMPACT),
        )
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Inferior
    # └────────────────────────────────────────────────────────────┘

    def _panel_inferior(self, frame: Frame):
        frame_organizacion = Frame(frame)
        frame_organizacion.pack(fill=X, padx=PADDING_OUTER, pady=(0, PADDING_OUTER))

        lbl_tipo_org = Label(frame_organizacion, text="Organización:")
        lbl_tipo_org.pack(side=LEFT, padx=(0, PADDING_PANEL))

        self.cbx_tipo_organizacion = Combobox(
            frame_organizacion,
            values=self.tipos_organizacion,
            state=READONLY,
            width=18,
            textvariable=self.var_tipo_organizacion,
        )
        self.cbx_tipo_organizacion.pack(side=LEFT, padx=(0, PADDING_PANEL))
        ToolTip(self.cbx_tipo_organizacion, "Selecciona el tipo de organización")

        lbl_org = Label(frame_organizacion, text="Elemento:")
        lbl_org.pack(side=LEFT, padx=(0, PADDING_PANEL))

        self.cbx_organizacion = Combobox(
            frame_organizacion,
            values=[],
            state=DISABLED,
            width=28,
            textvariable=self.var_organizacion,
        )
        self.cbx_organizacion.pack(side=LEFT, fill=X, expand=True)
        ToolTip(self.cbx_organizacion, "Selecciona la organización para mostrar sus libros")

        frame_busqueda = Frame(frame)
        frame_busqueda.pack(fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER)

        self.ent_buscar = Entry(frame_busqueda, textvariable=self.var_buscar)
        self.ent_buscar.pack(side=LEFT, fill=X, expand=True, padx=(0, PADDING_PANEL))
        ToolTip(self.ent_buscar, "Escribe aquí para buscar y presiona Enter")

        self.cbx_campos = Combobox(
            frame_busqueda, values=self.campos_busqueda, state=READONLY, width=12
        )
        self.cbx_campos.current(0)
        self.cbx_campos.pack(side=LEFT, padx=PADDING_PANEL)
        ToolTip(self.cbx_campos, "Selecciona en qué campo buscar")

        self.btn_buscar = Button(frame_busqueda, text="Buscar", style="primary")
        self.btn_buscar.pack(side=LEFT)
        ToolTip(self.btn_buscar, "Realizar la búsqueda en el estante")

        # Frame para paginación
        frame_paginacion = Frame(frame)
        frame_paginacion.pack(fill=X, padx=PADDING_OUTER, pady=(0, PADDING_OUTER))

        self.btn_anterior = Button(frame_paginacion, text="◀ Anterior", style="secondary")
        self.btn_anterior.pack(side=LEFT, padx=(0, PADDING_PANEL))
        ToolTip(self.btn_anterior, "Ir a la página anterior")

        self.lbl_pagina = Label(frame_paginacion, text="Página 1 de 1", bootstyle="secondary")
        self.lbl_pagina.pack(side=LEFT, expand=True)

        self.btn_siguiente = Button(frame_paginacion, text="Siguiente ▶", style="secondary")
        self.btn_siguiente.pack(side=RIGHT, padx=(PADDING_PANEL, 0))
        ToolTip(self.btn_siguiente, "Ir a la página siguiente")

    def actualizar_tabla(self):
        """
        Refrescar los datos del estante.

        Nota: El refrescado es manejado automáticamente por el controlador
        cuando hay cambios en la búsqueda.
        """
        if hasattr(self, "controlador"):
            self.controlador.recargar_estante()
