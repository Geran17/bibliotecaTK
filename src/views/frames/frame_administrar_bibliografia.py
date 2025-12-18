from typing import List, Dict, Any
from ttkbootstrap import (
    Frame,
    StringVar,
    Radiobutton,
    Label,
    Entry,
    PanedWindow,
    Notebook,
    IntVar,
    Button,
    LabelFrame,
)
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from models.entities.documento import Documento
from models.controllers.controlar_administrar_bibliografia import ControlarAdministrarBiblioteca


class FrameAdministrarBibliografia(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Variables
        # Búsqueda y selección
        self.var_buscar_documentos = StringVar()
        self.var_radio_documento = IntVar(value=0)
        self.documentos_seleccionados: List[Documento] = []

        # Formulario - Datos principales
        self.var_id_bibliografia = IntVar(value=0)
        self.var_titulo = StringVar()
        self.var_autores = StringVar()
        self.var_lugar_publicacion = StringVar()
        self.var_editorial = StringVar()
        self.var_ano_publicacion = StringVar()

        # Formulario - Datos complementarios
        self.var_numero_edicion = StringVar()
        self.var_idioma = StringVar()
        self.var_volumen_tomo = StringVar()
        self.var_numero_paginas = StringVar()
        self.var_isbn = StringVar()

        # cargamos los widgets
        self.cargar_widgets()

        # map_vars, para pasar como un solo argumento al controladorç
        self.map_vars: Dict[str, Any] = {
            'id_bibliografia': self.var_id_bibliografia,
            'titulo': self.var_titulo,
            'autores': self.var_autores,
            'lugar_publicacion': self.var_lugar_publicacion,
            'editorial': self.var_editorial,
            'ano_publicacion': self.var_ano_publicacion,
            'numero_edicion': self.var_numero_edicion,
            'idioma': self.var_idioma,
            'volumne_tomo': self.var_volumen_tomo,
            'numero_paginas': self.var_numero_paginas,
            'isbn': self.var_isbn,
            'radio_documento': self.var_radio_documento,
        }

        # map_buttons, para pasar en un solo argumento al controlador
        self.map_buttons: Dict[str, Button] = {
            'abrir': self.btn_abrir,
            'guardar': self.btn_guardar,
            'eliminar': self.btn_eliminar,
            'limpiar': self.btn_limpiar,
            'datos_online': self.btn_datos_online,
            'importar': self.btn_importar,
            'exportar': self.btn_exportar,
        }

        # instanciomos el controlador
        controlador = ControlarAdministrarBiblioteca(
            master=self, map_vars=self.map_vars, map_buttons=self.map_buttons
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def cargar_widgets(self):
        frame_superior = Frame(self, padding=(1, 1))
        self.panel_superior(frame=frame_superior)
        frame_superior.pack(fill=X, padx=1, pady=1)

        frame_central = Frame(self, padding=(1, 1))
        self.panel_central(frame=frame_central)
        frame_central.pack(fill=BOTH, expand=True, padx=1, pady=1)

        frame_inferior = Frame(self, padding=(1, 1))
        self.panel_inferior(frame=frame_inferior)
        frame_inferior.pack(fill=X, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Superior
    # └────────────────────────────────────────────────────────────┘

    def panel_superior(self, frame: Frame):
        lbl_titulo = Label(
            frame, text="📚 Administrar Bibliografía", font=("Helvetica", 14, "bold")
        )
        lbl_titulo.pack(side=TOP, fill=X, padx=10, pady=(5, 10))

        lbl_buscar = Label(frame, text="Buscar Documento:")
        lbl_buscar.pack(side=LEFT, padx=(10, 5), pady=5)
        ent_buscar_documentos = Entry(frame, textvariable=self.var_buscar_documentos)
        ent_buscar_documentos.pack(side=LEFT, padx=1, pady=1, fill=X, expand=True)
        ToolTip(ent_buscar_documentos, "Buscar documentos por título, autor o contenido")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Central
    # └────────────────────────────────────────────────────────────┘

    def panel_central(self, frame: Frame):
        paned_window = PanedWindow(frame, orient="vertical")
        paned_window.pack(fill=BOTH, padx=1, pady=1, expand=True)

        # --- Panel Superior: Lista de Documentos ---
        frame_top = LabelFrame(paned_window, text="Documentos Seleccionados", padding=5)

        self.scroll_frame = ScrolledFrame(frame_top)
        self.scroll_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)

        paned_window.add(frame_top)

        # --- Panel Inferior: Formularios ---
        frame_buttom = LabelFrame(paned_window, text="Información Bibliográfica", padding=5)

        self.note_book = Notebook(frame_buttom)
        self.note_book.pack(fill=BOTH, expand=True, padx=1, pady=1)
        self.panel_bibliografico(frame_tab=self.note_book)

        paned_window.add(frame_buttom)

    def panel_bibliografico(self, frame_tab: Notebook):
        frame_datos = Frame(frame_tab, padding=(1, 1))
        frame_datos.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)
        self.formulario_datos(frame=frame_datos)
        frame_tab.add(frame_datos, text="Datos Principales")

        frame_complementarios = Frame(frame_tab, padding=(1, 1))
        frame_complementarios.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)
        self.formulario_complementario(frame=frame_complementarios)
        frame_tab.add(frame_complementarios, text="Datos Complementarios")

    def formulario_datos(self, frame: Frame):
        """
        Crea el formulario para los datos bibliográficos principales.

        Args:
            frame (Frame): El frame contenedor para los widgets del formulario.
        """

        frame.columnconfigure(1, weight=1)

        # --- Fila 1: ID y Título ---
        lbl_id_dato = Label(frame, text="ID:")
        lbl_id_dato.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        ent_id_dato_bibliografico = Entry(
            frame, textvariable=self.var_id_bibliografia, justify=CENTER, state=READONLY, width=10
        )
        ent_id_dato_bibliografico.grid(column=1, row=0, padx=5, pady=5, sticky=W)
        ToolTip(ent_id_dato_bibliografico, "ID del dato bibliográfico (no editable)")

        lbl_titulo = Label(frame, text="Título:")
        lbl_titulo.grid(column=2, row=0, sticky=W, padx=5, pady=5)

        ent_titulo = Entry(frame, textvariable=self.var_titulo)
        ent_titulo.grid(column=3, row=0, padx=5, pady=5, sticky=EW, columnspan=3)
        ToolTip(ent_titulo, "Título del documento")
        frame.columnconfigure(3, weight=1)

        # --- Fila 2: Autores ---
        lbl_autores = Label(frame, text="Autores:")
        lbl_autores.grid(column=0, row=1, padx=5, pady=5, sticky=W)

        ent_autores = Entry(frame, textvariable=self.var_autores)
        ent_autores.grid(column=1, row=1, padx=5, pady=5, sticky=EW, columnspan=5)
        ToolTip(ent_autores, "Autores del documento, separados por coma (,) si son varios")

        # --- Fila 3: Editorial, Lugar y Año ---
        lbl_editorial = Label(frame, text="Editorial:")
        lbl_editorial.grid(column=0, row=2, padx=5, pady=5, sticky=W)

        ent_editorial = Entry(frame, textvariable=self.var_editorial)
        ent_editorial.grid(column=1, row=2, padx=5, pady=5, sticky=EW)
        ToolTip(ent_editorial, "Editorial que publicó el documento")

        lbl_lugar_publicacion = Label(frame, text="Lugar:")
        lbl_lugar_publicacion.grid(column=2, row=2, padx=5, pady=5, sticky=W)

        ent_lugar_publicacion = Entry(frame, textvariable=self.var_lugar_publicacion)
        ent_lugar_publicacion.grid(column=3, row=2, padx=5, pady=5, sticky=EW)
        ToolTip(ent_lugar_publicacion, "Ciudad o país donde se publicó el documento")

        lbl_ano = Label(frame, text="Año:")
        lbl_ano.grid(column=4, row=2, padx=5, pady=5, sticky=W)

        ent_ano = Entry(frame, textvariable=self.var_ano_publicacion, width=10)
        ent_ano.grid(column=5, row=2, padx=5, pady=5, sticky=W)
        ToolTip(ent_ano, "Año de publicación del documento")

    def formulario_complementario(self, frame: Frame):
        """
        Crea el formulario para los datos bibliográficos complementarios.

        Args:
            frame (Frame): El frame contenedor para los widgets del formulario.
        """
        frame.columnconfigure((1, 3), weight=1)

        lbl_edicion = Label(frame, text="Edición N°:")
        lbl_edicion.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ent_edicion = Entry(frame, textvariable=self.var_numero_edicion)
        ent_edicion.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        ToolTip(ent_edicion, "Número de la edición del documento")

        lbl_idioma = Label(frame, text="Idioma:")
        lbl_idioma.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        ent_idioma = Entry(frame, textvariable=self.var_idioma)
        ent_idioma.grid(row=0, column=3, padx=5, pady=5, sticky=EW)
        ToolTip(ent_idioma, "Idioma original del documento")

        lbl_volumen = Label(frame, text="Volumen/Tomo:")
        lbl_volumen.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ent_volumen = Entry(frame, textvariable=self.var_volumen_tomo)
        ent_volumen.grid(row=1, column=1, padx=5, pady=5, sticky=EW, columnspan=1)
        ToolTip(ent_volumen, "Volumen o tomo, si aplica")

        lbl_paginas = Label(frame, text="Paginas:")
        lbl_paginas.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        ent_paginas = Entry(frame, textvariable=self.var_numero_paginas)
        ent_paginas.grid(row=1, column=3, padx=5, pady=5, sticky=EW, columnspan=2)
        ToolTip(ent_paginas, "Numero de paginas del documento. Ej.: 1042")

        lbl_isbn = Label(frame, text="ISBN:")
        lbl_isbn.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ent_isbn = Entry(frame, textvariable=self.var_isbn)
        ent_isbn.grid(row=2, column=1, padx=5, pady=5, sticky=EW, columnspan=3)
        ToolTip(ent_isbn, "Código ISBN del documento")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Inferior
    # └────────────────────────────────────────────────────────────┘

    def panel_inferior(self, frame: Frame):
        frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.btn_abrir = Button(frame, text="Abrir")
        self.btn_abrir.grid(row=0, column=0, padx=2, pady=5, sticky=EW)
        ToolTip(self.btn_abrir, "Abrir el documento seleccionado")

        self.btn_datos_online = Button(frame, text="Datos Online")
        self.btn_datos_online.grid(row=0, column=1, padx=2, pady=5, sticky=EW)
        ToolTip(
            self.btn_datos_online,
            "Cargar los datos del documento seleccionado en los formularios",
        )

        self.btn_guardar = Button(frame, text="Guardar")
        self.btn_guardar.grid(row=0, column=2, padx=2, pady=5, sticky=EW)
        ToolTip(self.btn_guardar, "Guardar los cambios de los datos bibliográficos")

        self.btn_limpiar = Button(frame, text="Limpiar")
        self.btn_limpiar.grid(row=0, column=3, padx=2, pady=5, sticky=EW)
        ToolTip(self.btn_limpiar, "Limpiar todos los campos del formulario")

        self.btn_eliminar = Button(frame, text="Eliminar")
        self.btn_eliminar.grid(row=0, column=4, padx=2, pady=5, sticky=EW)
        ToolTip(
            self.btn_eliminar,
            "Eliminar los datos bibliográficos del documento seleccionado",
        )

        self.btn_importar = Button(frame, text="Importar")
        self.btn_importar.grid(row=0, column=5, padx=2, pady=5, sticky=EW)
        ToolTip(
            self.btn_importar,
            "Importa los datos bibliográficos del documento seleccionado",
        )

        self.btn_exportar = Button(frame, text="Exportar")
        self.btn_exportar.grid(row=0, column=6, padx=2, pady=5, sticky=EW)
        ToolTip(
            self.btn_exportar,
            "Exporta los datos bibliográficos del documento seleccionado",
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos
    # └────────────────────────────────────────────────────────────┘

    def obtener_documentos_seleccionados(self, documentos_seleccionados: List[Documento]):
        if documentos_seleccionados:
            self.documentos_seleccionados = documentos_seleccionados
            # Aqui es donde cargamos los documentos seleccionados
            self._cargar_documentos_seleccionados()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos privados
    # └────────────────────────────────────────────────────────────┘

    def _cargar_documentos_seleccionados(self):
        # obtenemos los hijos que tiene el frame scroll y lo destruimos
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if self.documentos_seleccionados:
            for documento in self.documentos_seleccionados:
                radio = Radiobutton(
                    self.scroll_frame,
                    text=documento.nombre,
                    variable=self.var_radio_documento,
                    value=documento.id,
                )
                radio.pack(anchor=W, padx=5, pady=5)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘
