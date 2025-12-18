from ttkbootstrap import (
    Frame,
    Label,
    PanedWindow,
    Separator,
    Treeview,
    LabelFrame,
    Entry,
    Button,
    Combobox,
    Radiobutton,
    IntVar,
    StringVar,
    Scrollbar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from typing import List, Dict, Any
from models.entities.documento import Documento
from models.controllers.controlar_administrar_contenido import ControlarAdministrarContenido


class FrameAdministrarContenido(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Vars
        self.var_radio_documento = IntVar()
        self.var_id_seccion_padre = IntVar()

        # Vars para Capitulo
        self.var_id_capitulo = IntVar(value=0)
        self.var_numero_capitulo = StringVar()
        self.var_pagina_capitulo = StringVar()
        self.var_titulo_capitulo = StringVar()

        # Vars para Seccion
        self.var_id_seccion = IntVar(value=0)
        self.var_nivel_seccion = StringVar()
        self.var_pagina_seccion = StringVar()
        self.var_titulo_seccion = StringVar()

        # Variables Globales
        self.documentos_seleccionados: List[Documento] = {}

        # cargamos los widgets
        self.crear_widgets()

        # map_buttons
        self.map_widgets: Dict[str, Any] = {
            'agregar_capitulo': self.btn_agregar_capitulo,
            'editar_capitulo': self.btn_editar_capitulo,
            'eliminar_capitulo': self.btn_eliminar_capitulo,
            'nuevo_capitulo': self.btn_nuevo_capitulo,
            'agregar_seccion': self.btn_agregar_seccion,
            'editar_seccion': self.btn_editar_seccion,
            'eliminar_seccion': self.btn_eliminar_seccion,
            'nuevo_seccion': self.btn_nuevo_seccion,
            'tree_view': self.tree_view,
            'seccion_padre': self.cbx_seccion_padre,
            'abrir_documento': self.btn_abrir_documento,
        }

        # map_vars
        self.map_vars: Dict[str, Any] = {
            'radio_documento': self.var_radio_documento,
            'id_seccion_padre': self.var_id_seccion_padre,
            'id_capitulo': self.var_id_capitulo,
            'numero_capitulo': self.var_numero_capitulo,
            'pagina_capitulo': self.var_pagina_capitulo,
            'titulo_capitulo': self.var_titulo_capitulo,
            'id_seccion': self.var_id_seccion,
            'nivel_seccion': self.var_nivel_seccion,
            'pagina_seccion': self.var_pagina_seccion,
            'titulo_seccion': self.var_titulo_seccion,
        }

        # Cargamos el controlador
        controlador = ControlarAdministrarContenido(
            map_vars=self.map_vars, map_widgets=self.map_widgets, master=self
        )

    def crear_widgets(self):

        # frame superior
        frame_superior = Frame(self, padding=(1, 1))
        self.panel_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)

        # frame central
        frame_central = Frame(self, padding=(1, 1))
        self.panel_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)

        # frame inferior
        frame_inferior = Frame(self, padding=(1, 1))
        self.panel_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Superior
    # └────────────────────────────────────────────────────────────┘

    def panel_superior(self, frame: Frame):
        lbl_titulo = Label(frame, text="📑 Administrar Contenidos", font=('Helvetica', 14, 'bold'))
        lbl_titulo.pack(side=TOP, fill=X, padx=1, pady=1)

        Separator(frame, orient='horizontal').pack(side=TOP, fill=X, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Central
    # └────────────────────────────────────────────────────────────┘

    def panel_central(self, frame: Frame):
        # Corregido: orientación horizontal para izquierda-derecha
        paned_window = PanedWindow(frame, orient="horizontal")
        paned_window.pack(side=TOP, fill=BOTH, expand=TRUE)  # ¡Agregado!

        frame_izquierdo = Frame(paned_window, padding=(1, 1))
        self.panel_documentos(frame=frame_izquierdo)
        paned_window.add(frame_izquierdo, weight=0)

        frame_derecho = Frame(paned_window, padding=(1, 1))
        self.panel_contenido(frame=frame_derecho)
        paned_window.add(frame_derecho, weight=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Documentos
    # └────────────────────────────────────────────────────────────┘

    def panel_documentos(self, frame: Frame):
        # Título de la sección
        Label(frame, text="Documentos", font=('Helvetica', 10, 'bold')).pack(
            side=TOP, fill=X, padx=5, pady=5
        )

        Separator(frame).pack(side=TOP, fill=X, padx=5, pady=5)

        self.scroll_frame = ScrolledFrame(frame, autohide=TRUE)
        self.scroll_frame.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=TRUE)

        self.btn_abrir_documento = Button(frame, text="Abrir documento")
        self.btn_abrir_documento.pack(side=TOP, fill=X, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Contenido
    # └────────────────────────────────────────────────────────────┘
    def panel_contenido(self, frame: Frame):

        Label(frame, text="Contenido", font=('Helvetica', 10, 'bold')).pack(
            side=TOP, fill=X, padx=5, pady=5
        )

        Separator(frame).pack(side=TOP, fill=X, padx=5, pady=5)

        # Configuración completa del Treeview
        self.tree_view = Treeview(
            frame,
            columns=("Pagina"),
            show='tree headings',  # Mostrar árbol y encabezados
            selectmode='browse',
        )

        # Configuerar encabezados
        self.tree_view.heading("#0", text="Contenido", anchor=W)
        self.tree_view.heading("Pagina", text="Pagina", anchor=W)

        # Configuramos ancho de columnas
        self.tree_view.column("#0", width=200)
        self.tree_view.column("Pagina", width=50, anchor=E)

        scrollbar = Scrollbar(frame, orient=VERTICAL, command=self.tree_view.yview)

        self.tree_view.pack(side=LEFT, fill=BOTH, padx=1, pady=1, expand=TRUE)

        scrollbar.pack(side=RIGHT, fill=Y)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Inferior
    # └────────────────────────────────────────────────────────────┘

    def panel_inferior(self, frame: Frame):
        label_frame_izq = LabelFrame(frame, text="Capitulo")
        self.panel_capitulo(frame=label_frame_izq)
        label_frame_izq.pack(side=LEFT, fill=Y, padx=1, pady=1, expand=TRUE)

        label_frame_der = LabelFrame(frame, text="Seccion")
        self.panel_seccion(frame=label_frame_der)
        label_frame_der.pack(side=LEFT, fill=Y, padx=1, pady=1, expand=TRUE)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Capitulo
    # └────────────────────────────────────────────────────────────┘

    def panel_capitulo(self, frame: LabelFrame):
        frame_capitulo = Frame(frame, padding=(1, 1))
        frame_capitulo.pack(side=TOP, fill=X, padx=1, pady=1, expand=True)

        lbl_id_capitulo = Label(frame_capitulo, text="ID: ")
        lbl_id_capitulo.grid(column=0, row=0, sticky=EW, padx=1, pady=1)

        ent_id_capitulo = Entry(
            frame_capitulo, state=READONLY, justify=CENTER, textvariable=self.var_id_capitulo
        )
        ent_id_capitulo.grid(column=0, row=1, padx=1, pady=1, sticky=EW)

        lbl_numero_capitulo = Label(frame_capitulo, text="Numero Capitulo: ")
        lbl_numero_capitulo.grid(column=1, row=0, padx=1, pady=1, sticky=EW)

        ent_numero_capitulo = Entry(
            frame_capitulo, justify=CENTER, textvariable=self.var_numero_capitulo
        )
        ent_numero_capitulo.grid(column=1, row=1, padx=1, pady=1, sticky=EW)

        lbl_pagina_capitulo = Label(frame_capitulo, text="Numero Pagina: ")
        lbl_pagina_capitulo.grid(column=3, row=0, padx=1, pady=1, sticky=EW)

        ent_pagina_capitulo = Entry(
            frame_capitulo, justify=RIGHT, textvariable=self.var_pagina_capitulo
        )
        ent_pagina_capitulo.grid(column=3, row=1, padx=1, pady=1, sticky=EW)

        lbl_titulo_capitulo = Label(frame_capitulo, text="Titulo: ")
        lbl_titulo_capitulo.grid(column=0, row=2, padx=1, pady=1, sticky=EW)

        ent_titulo_capitulo = Entry(frame_capitulo, textvariable=self.var_titulo_capitulo)
        ent_titulo_capitulo.grid(column=0, row=3, padx=1, pady=1, sticky=EW, columnspan=4)

        frame_buttons = Frame(frame, padding=(1, 1))
        frame_buttons.pack(side=TOP, fill=X, padx=1, pady=1)

        self.btn_agregar_capitulo = Button(frame_buttons, text="Agregar")
        self.btn_agregar_capitulo.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        self.btn_editar_capitulo = Button(frame_buttons, text="Editar", state=DISABLED)
        self.btn_editar_capitulo.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        self.btn_nuevo_capitulo = Button(frame_buttons, text="Nuevo")
        self.btn_nuevo_capitulo.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        self.btn_eliminar_capitulo = Button(frame_buttons, text="Eliminar")
        self.btn_eliminar_capitulo.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

    def panel_seccion(self, frame: LabelFrame):
        frame_seccion = Frame(frame, padding=(1, 1))
        frame_seccion.pack(side=TOP, fill=X, padx=1, pady=1, expand=True)

        lbl_id_seccion = Label(frame_seccion, text="ID: ")
        lbl_id_seccion.grid(column=0, row=0, padx=1, pady=1, sticky=EW)

        ent_id_seccion = Entry(
            frame_seccion, justify=CENTER, state=READONLY, textvariable=self.var_id_seccion
        )
        ent_id_seccion.grid(column=0, row=1, padx=1, pady=1, sticky=EW)

        lbl_nivel_seccion = Label(frame_seccion, text="Nivel: ")
        lbl_nivel_seccion.grid(column=1, row=0, padx=1, pady=1, sticky=EW)

        ent_nivel_seccion = Entry(
            frame_seccion, justify=CENTER, textvariable=self.var_nivel_seccion
        )
        ent_nivel_seccion.grid(column=1, row=1, padx=1, pady=1, sticky=EW)

        lbl_pagina_seccion = Label(frame_seccion, text="Pagina: ")
        lbl_pagina_seccion.grid(column=2, row=0, padx=1, pady=1, sticky=EW)

        ent_pagina_seccion = Entry(
            frame_seccion, justify=RIGHT, textvariable=self.var_pagina_seccion
        )
        ent_pagina_seccion.grid(column=2, row=1, padx=1, pady=1, sticky=EW)

        lbl_seccion_padre = Label(frame_seccion, text="Seccion Padre: ")
        lbl_seccion_padre.grid(column=0, row=2, padx=1, pady=1, sticky=EW)

        self.cbx_seccion_padre = Combobox(
            frame_seccion,
            state=READONLY,
            values=[
                "Sin padre",
            ],
        )
        self.cbx_seccion_padre.current(0)
        self.cbx_seccion_padre.grid(column=0, row=3, padx=1, pady=1, columnspan=3, sticky=EW)

        lbl_titulo_seccion = Label(frame_seccion, text="Titulo: ")
        lbl_titulo_seccion.grid(column=0, row=4, padx=1, pady=1, sticky=EW)

        ent_titulo_seccion = Entry(frame_seccion, textvariable=self.var_titulo_seccion)
        ent_titulo_seccion.grid(column=0, row=5, padx=1, pady=1, columnspan=3, sticky=EW)

        frame_buttons = Frame(frame, padding=(1, 1))
        frame_buttons.pack(side=TOP, fill=X, padx=1, pady=1)

        self.btn_agregar_seccion = Button(frame_buttons, text="Agregar")
        self.btn_agregar_seccion.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        self.btn_editar_seccion = Button(frame_buttons, text="Editar", state=DISABLED)
        self.btn_editar_seccion.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        self.btn_nuevo_seccion = Button(frame_buttons, text="Nuevo")
        self.btn_nuevo_seccion.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        self.btn_eliminar_seccion = Button(frame_buttons, text="Eliminar")
        self.btn_eliminar_seccion.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Publicos
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
