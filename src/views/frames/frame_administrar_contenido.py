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
from views.components.ui_tokens import PADDING_COMPACT, PADDING_OUTER, PADDING_PANEL
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog, messagebox
from typing import List, Dict, Any
from models.entities.documento import Documento
from models.controllers.controlar_administrar_contenido import ControlarAdministrarContenido
from models.controllers.controlar_importacion_csv import ControlarImportacionCSV


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
            'importar_capitulos': self.btn_importar_capitulos,
            'importar_secciones': self.btn_importar_secciones,
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
        frame_superior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        # frame central
        frame_central = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=TRUE)

        # frame inferior
        frame_inferior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Superior
    # └────────────────────────────────────────────────────────────┘

    def panel_superior(self, frame: Frame):
        lbl_titulo = Label(frame, text="📑 Administrar Contenidos", font=('Helvetica', 14, 'bold'))
        lbl_titulo.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        Separator(frame, orient='horizontal').pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Central
    # └────────────────────────────────────────────────────────────┘

    def panel_central(self, frame: Frame):
        # Corregido: orientación horizontal para izquierda-derecha
        paned_window = PanedWindow(frame, orient="horizontal")
        paned_window.pack(side=TOP, fill=BOTH, expand=TRUE)  # ¡Agregado!

        frame_izquierdo = Frame(paned_window, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_documentos(frame=frame_izquierdo)
        paned_window.add(frame_izquierdo, weight=0)

        frame_derecho = Frame(paned_window, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_contenido(frame=frame_derecho)
        paned_window.add(frame_derecho, weight=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Documentos
    # └────────────────────────────────────────────────────────────┘

    def panel_documentos(self, frame: Frame):
        # Título de la sección
        Label(frame, text="Documentos", font=('Helvetica', 10, 'bold')).pack(
            side=TOP, fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER
        )

        Separator(frame).pack(side=TOP, fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER)

        self.scroll_frame = ScrolledFrame(frame, autohide=TRUE)
        self.scroll_frame.pack(side=TOP, fill=BOTH, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=TRUE)

        self.btn_abrir_documento = Button(frame, text="Abrir documento")
        self.btn_abrir_documento.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Contenido
    # └────────────────────────────────────────────────────────────┘
    def panel_contenido(self, frame: Frame):

        Label(frame, text="Contenido", font=('Helvetica', 10, 'bold')).pack(
            side=TOP, fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER
        )

        Separator(frame).pack(side=TOP, fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER)

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

        self.tree_view.pack(side=LEFT, fill=BOTH, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=TRUE)

        scrollbar.pack(side=RIGHT, fill=Y)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Inferior
    # └────────────────────────────────────────────────────────────┘

    def panel_inferior(self, frame: Frame):
        label_frame_izq = LabelFrame(frame, text="Capitulo")
        self.panel_capitulo(frame=label_frame_izq)
        label_frame_izq.pack(side=LEFT, fill=Y, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=TRUE)

        label_frame_der = LabelFrame(frame, text="Seccion")
        self.panel_seccion(frame=label_frame_der)
        label_frame_der.pack(side=LEFT, fill=Y, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=TRUE)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Capitulo
    # └────────────────────────────────────────────────────────────┘

    def panel_capitulo(self, frame: LabelFrame):
        frame_capitulo = Frame(frame, padding=(PADDING_COMPACT, PADDING_COMPACT))
        frame_capitulo.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        lbl_id_capitulo = Label(frame_capitulo, text="ID: ")
        lbl_id_capitulo.grid(column=0, row=0, sticky=EW, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        ent_id_capitulo = Entry(
            frame_capitulo, state=READONLY, justify=CENTER, textvariable=self.var_id_capitulo
        )
        ent_id_capitulo.grid(column=0, row=1, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        lbl_numero_capitulo = Label(frame_capitulo, text="Numero Capitulo: ")
        lbl_numero_capitulo.grid(column=1, row=0, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        ent_numero_capitulo = Entry(
            frame_capitulo, justify=CENTER, textvariable=self.var_numero_capitulo
        )
        ent_numero_capitulo.grid(column=1, row=1, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        lbl_pagina_capitulo = Label(frame_capitulo, text="Numero Pagina: ")
        lbl_pagina_capitulo.grid(column=3, row=0, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        ent_pagina_capitulo = Entry(
            frame_capitulo, justify=RIGHT, textvariable=self.var_pagina_capitulo
        )
        ent_pagina_capitulo.grid(column=3, row=1, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        lbl_titulo_capitulo = Label(frame_capitulo, text="Titulo: ")
        lbl_titulo_capitulo.grid(column=0, row=2, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        ent_titulo_capitulo = Entry(frame_capitulo, textvariable=self.var_titulo_capitulo)
        ent_titulo_capitulo.grid(column=0, row=3, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW, columnspan=4)

        frame_buttons = Frame(frame, padding=(PADDING_COMPACT, PADDING_COMPACT))
        frame_buttons.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        self.btn_agregar_capitulo = Button(frame_buttons, text="Agregar", style="primary.TButton")
        self.btn_agregar_capitulo.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        self.btn_editar_capitulo = Button(
            frame_buttons, text="Editar", state=DISABLED, style="info.Outline.TButton"
        )
        self.btn_editar_capitulo.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        self.btn_nuevo_capitulo = Button(
            frame_buttons, text="Nuevo", style="success.Outline.TButton"
        )
        self.btn_nuevo_capitulo.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        self.btn_eliminar_capitulo = Button(
            frame_buttons, text="Eliminar", style="danger.Outline.TButton"
        )
        self.btn_eliminar_capitulo.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        frame_buttons_import = Frame(frame, padding=(PADDING_COMPACT, PADDING_COMPACT))
        frame_buttons_import.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        self.btn_importar_capitulos = Button(
            frame_buttons_import,
            text="📥 Importar CSV",
            style="secondary.Outline.TButton",
        )
        self.btn_importar_capitulos.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

    def panel_seccion(self, frame: LabelFrame):
        frame_seccion = Frame(frame, padding=(PADDING_COMPACT, PADDING_COMPACT))
        frame_seccion.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        lbl_id_seccion = Label(frame_seccion, text="ID: ")
        lbl_id_seccion.grid(column=0, row=0, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        ent_id_seccion = Entry(
            frame_seccion, justify=CENTER, state=READONLY, textvariable=self.var_id_seccion
        )
        ent_id_seccion.grid(column=0, row=1, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        lbl_nivel_seccion = Label(frame_seccion, text="Nivel: ")
        lbl_nivel_seccion.grid(column=1, row=0, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        ent_nivel_seccion = Entry(
            frame_seccion, justify=CENTER, textvariable=self.var_nivel_seccion
        )
        ent_nivel_seccion.grid(column=1, row=1, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        lbl_pagina_seccion = Label(frame_seccion, text="Pagina: ")
        lbl_pagina_seccion.grid(column=2, row=0, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        ent_pagina_seccion = Entry(
            frame_seccion, justify=RIGHT, textvariable=self.var_pagina_seccion
        )
        ent_pagina_seccion.grid(column=2, row=1, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        lbl_seccion_padre = Label(frame_seccion, text="Seccion Padre: ")
        lbl_seccion_padre.grid(column=0, row=2, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        self.cbx_seccion_padre = Combobox(
            frame_seccion,
            state=READONLY,
            values=[
                "Sin padre",
            ],
        )
        self.cbx_seccion_padre.current(0)
        self.cbx_seccion_padre.grid(column=0, row=3, padx=PADDING_COMPACT, pady=PADDING_COMPACT, columnspan=3, sticky=EW)

        lbl_titulo_seccion = Label(frame_seccion, text="Titulo: ")
        lbl_titulo_seccion.grid(column=0, row=4, padx=PADDING_COMPACT, pady=PADDING_COMPACT, sticky=EW)

        ent_titulo_seccion = Entry(frame_seccion, textvariable=self.var_titulo_seccion)
        ent_titulo_seccion.grid(column=0, row=5, padx=PADDING_COMPACT, pady=PADDING_COMPACT, columnspan=3, sticky=EW)

        frame_buttons = Frame(frame, padding=(PADDING_COMPACT, PADDING_COMPACT))
        frame_buttons.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        self.btn_agregar_seccion = Button(frame_buttons, text="Agregar", style="primary.TButton")
        self.btn_agregar_seccion.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        self.btn_editar_seccion = Button(
            frame_buttons, text="Editar", state=DISABLED, style="info.Outline.TButton"
        )
        self.btn_editar_seccion.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        self.btn_nuevo_seccion = Button(
            frame_buttons, text="Nuevo", style="success.Outline.TButton"
        )
        self.btn_nuevo_seccion.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        self.btn_eliminar_seccion = Button(
            frame_buttons, text="Eliminar", style="danger.Outline.TButton"
        )
        self.btn_eliminar_seccion.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

        frame_buttons_import = Frame(frame, padding=(PADDING_COMPACT, PADDING_COMPACT))
        frame_buttons_import.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        self.btn_importar_secciones = Button(
            frame_buttons_import,
            text="📥 Importar CSV",
            style="secondary.Outline.TButton",
        )
        self.btn_importar_secciones.pack(side=LEFT, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Publicos
    # └────────────────────────────────────────────────────────────┘

    def obtener_documentos_seleccionados(self, documentos_seleccionados: List[Documento]):
        if documentos_seleccionados:
            self.documentos_seleccionados = documentos_seleccionados
            # Aqui es donde cargamos los documentos seleccionados
            self._cargar_documentos_seleccionados()

    def importar_capitulos(self) -> None:
        """Abre diálogo para seleccionar archivo CSV e importa capítulos."""
        id_documento = self.var_radio_documento.get()

        if not id_documento:
            messagebox.showwarning(
                title="Advertencia",
                message="Debe seleccionar un documento antes de importar capítulos.",
                parent=self,
            )
            return

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de capítulos",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            parent=self,
        )

        if not ruta_archivo:
            return

        try:
            controlador = ControlarImportacionCSV()
            registros_importados, errores = controlador.importar_capitulos_csv(
                ruta_archivo, id_documento
            )

            mensaje = f"✅ Se importaron {registros_importados} capítulos exitosamente.\n"

            if errores:
                mensaje += f"\n⚠️ Se encontraron {len(errores)} errores:\n"
                mensaje += "\n".join(errores[:10])  # Mostrar primeros 10 errores
                if len(errores) > 10:
                    mensaje += f"\n... y {len(errores) - 10} errores más"

                messagebox.showwarning(
                    title="Importación con errores",
                    message=mensaje,
                    parent=self,
                )
            else:
                messagebox.showinfo(
                    title="Importación exitosa",
                    message=mensaje,
                    parent=self,
                )

        except Exception as e:
            messagebox.showerror(
                title="Error en importación",
                message=f"Ocurrió un error durante la importación:\n{str(e)}",
                parent=self,
            )

    def importar_secciones(self) -> None:
        """Abre diálogo para seleccionar archivo CSV e importa secciones."""
        # Obtener ID del capítulo seleccionado del treeview
        seleccion = self.tree_view.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Debe seleccionar un capítulo antes de importar secciones."
            )
            return

        # El ID del capítulo se obtendría del árbol seleccionado
        # Para este caso, usaremos el var_id_capitulo
        id_capitulo = self.var_id_capitulo.get()

        if not id_capitulo:
            messagebox.showwarning(
                title="Advertencia",
                message="No se pudo obtener el ID del capítulo seleccionado.",
                parent=self,
            )
            return

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de secciones",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            parent=self,
        )

        if not ruta_archivo:
            return

        try:
            controlador = ControlarImportacionCSV()
            registros_importados, errores = controlador.importar_secciones_csv(
                ruta_archivo, id_capitulo
            )

            mensaje = f"✅ Se importaron {registros_importados} secciones exitosamente.\n"

            if errores:
                mensaje += f"\n⚠️ Se encontraron {len(errores)} errores:\n"
                mensaje += "\n".join(errores[:10])  # Mostrar primeros 10 errores
                if len(errores) > 10:
                    mensaje += f"\n... y {len(errores) - 10} errores más"

                messagebox.showwarning(
                    title="Importación con errores",
                    message=mensaje,
                    parent=self,
                )
            else:
                messagebox.showinfo(title="Importación exitosa", message=mensaje, parent=self)

        except Exception as e:
            messagebox.showerror(
                title="Error en importación",
                message=f"Ocurrió un error durante la importación:\n{str(e)}",
                parent=self,
            )

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
                radio.pack(anchor=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
