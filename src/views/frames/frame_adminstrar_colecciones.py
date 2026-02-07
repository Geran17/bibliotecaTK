from ttkbootstrap import (
    Frame,
    Label,
    Separator,
    Notebook,
    Button,
    Entry,
    Text,
    IntVar,
    StringVar,
    LabelFrame,
    Scrollbar,
)
from typing import List
from tkinter import messagebox
from ttkbootstrap.constants import *
from views.components.ui_tokens import PADDING_COMPACT, PADDING_OUTER, PADDING_PANEL
from ttkbootstrap.tableview import Tableview
from models.entities.coleccion import Coleccion
from models.entities.consulta import Consulta


class AdministrarColecciones(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # variables
        self.var_id_coleccion = IntVar()
        self.var_id_coleccion.set(0)
        self.var_nombre = StringVar()
        self.var_nombre.set("")
        # table view
        self.coldata = [
            {"text": "ID", "stretch": False, "width": 50},
            {"text": "Nombre", "stretch": True},
            {"text": "Creado", "stretch": False},
            {"text": "Actualizado", "stretch": False},
        ]
        # controlar desplazamiento
        self.desplazar = 0

        # cargamos los widgets
        self.crear_widgets()

        # cargamos las colecciones en la tabla
        self._load_table()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        # Frame superior
        self.frame_superior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_superior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.panel_superior(frame=self.frame_superior)

        # Frame central
        self.frame_central = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.panel_central(frame=self.frame_central)

        # Frame inferior
        self.frame_inferior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_inferior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.panel_inferior(frame=self.frame_inferior)

    def panel_superior(self, frame: Frame):

        estilo_fuente_titulo = ('Helvetica', 14, 'bold')

        label_titulo = Label(
            frame,
            text="📚 Administrar Colecciones",
            font=estilo_fuente_titulo,  # Aplicamos la fuente
        )
        label_titulo.pack(side=TOP, fill=X, padx=PADDING_PANEL, pady=PADDING_PANEL)

        separador = Separator(frame)
        separador.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

    def panel_central(self, frame: Frame):
        # 1. Crear el widget Notebook
        self.notebook = Notebook(frame)
        self.notebook.pack(
            fill=BOTH, expand=True, padx=PADDING_OUTER, pady=PADDING_OUTER
        )  # Lo expandimos para que ocupe el frame central

        # frame datos
        frame_datos = Frame(self.notebook, padding=(PADDING_PANEL, PADDING_PANEL))
        frame_datos.pack(side=TOP, fill=BOTH)
        self.tab_datos(frame=frame_datos)
        self.notebook.add(frame_datos, text="Datos")

        # frame explorar
        frame_explorar = Frame(self.notebook, padding=(PADDING_PANEL, PADDING_PANEL))
        frame_explorar.pack(side=TOP, fill=BOTH, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)
        self.tab_explorar(frame=frame_explorar)
        self.notebook.add(frame_explorar, text="Explorar")

    def tab_datos(self, frame):
        # --- Frame para Detalles de la Colección ---
        lf_detalles = LabelFrame(frame, text="Detalles de la Colección", padding=10)
        lf_detalles.pack(side=TOP, fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER)
        lf_detalles.columnconfigure(1, weight=1)

        # Fila 1: ID
        Label(lf_detalles, text="ID:").grid(row=0, column=0, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
        ent_id = Entry(
            lf_detalles,
            state=READONLY,
            textvariable=self.var_id_coleccion,
            width=10,
            justify="center",
        )
        ent_id.grid(row=0, column=1, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)

        # Fila 2: Nombre
        Label(lf_detalles, text="Nombre:").grid(row=1, column=0, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
        ent_coleccion = Entry(lf_detalles, textvariable=self.var_nombre)
        ent_coleccion.grid(row=1, column=1, sticky=EW, padx=PADDING_OUTER, pady=PADDING_OUTER)

        # --- Frame para Descripción ---
        lf_descripcion = LabelFrame(frame, text="Descripción", padding=10)
        lf_descripcion.pack(side=TOP, fill=BOTH, padx=PADDING_OUTER, pady=PADDING_OUTER, expand=True)

        scrollbar = Scrollbar(lf_descripcion)
        self.txt_descripcion = Text(
            lf_descripcion, wrap=WORD, height=5, yscrollcommand=scrollbar.set
        )
        scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_descripcion.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.txt_descripcion.yview)

        # --- Frame para Botones de Acción ---
        frame_buttons = Frame(frame, padding=(PADDING_COMPACT, PADDING_COMPACT))
        frame_buttons.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        frame_buttons.columnconfigure((0, 1, 2), weight=1)

        Button(frame_buttons, text="Aplicar", command=self.on_aplicar, style="primary.TButton").pack(
            side=LEFT, fill=X, expand=TRUE, padx=PADDING_PANEL, pady=PADDING_PANEL
        )
        Button(frame_buttons, text="Eliminar", command=self.on_eliminar, style="danger.Outline.TButton").pack(
            side=LEFT, fill=X, expand=TRUE, padx=PADDING_PANEL, pady=PADDING_PANEL
        )
        Button(frame_buttons, text="Nuevo", command=self.on_nuevo, style="success.Outline.TButton").pack(
            side=LEFT, fill=X, expand=TRUE, padx=PADDING_PANEL, pady=PADDING_PANEL
        )

        # Botones de navegación
        Button(frame_buttons, text="|<", command=self.on_primer_elemento, style="secondary.Outline.TButton").pack(side=LEFT)
        Button(frame_buttons, text="<", command=self.on_anterior_elemento, style="secondary.Outline.TButton").pack(side=LEFT)
        Button(frame_buttons, text=">", command=self.on_siguiente_elemento, style="secondary.Outline.TButton").pack(side=LEFT)
        Button(frame_buttons, text=">|", command=self.on_ultimo_elemento, style="secondary.Outline.TButton").pack(side=LEFT)

    def tab_explorar(self, frame):
        self.table_view = Tableview(frame, searchable=True, coldata=self.coldata, bootstyle=PRIMARY)
        self.table_view.pack(side=TOP, fill=BOTH, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        # vinculamos el evento de doble click
        self.table_view.view.bind("<Double-1>", self.on_seleccionar_fila)

    def panel_inferior(self, frame: Frame):
        pass

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones privadas
    # └────────────────────────────────────────────────────────────┘

    def _generar_lista(self) -> List[Coleccion]:
        consulta = Consulta()
        return consulta.get_colecciones()

    def _get_descripcion(self) -> str:
        return self.txt_descripcion.get("1.0", "end-1c")

    def _set_descripcion(self, descripcion):
        self.txt_descripcion.insert("1.0", descripcion)

    def _clear_descripcion(self):
        self.txt_descripcion.delete("1.0", "end")

    def _get_coleccion(self) -> Coleccion:
        id_coleccion = self.var_id_coleccion.get()
        nombre = self.var_nombre.get()
        descipcion = self._get_descripcion()
        coleccion = None
        if id_coleccion == 0:
            coleccion = Coleccion(nombre=nombre, descripcion=descipcion)
        else:
            coleccion = Coleccion(nombre=nombre, descripcion=descipcion, id=id_coleccion)
        return coleccion

    def _set_coleccion(self, coleccion: Coleccion):
        if isinstance(coleccion, Coleccion):
            self.var_id_coleccion.set(coleccion.id)
            self.var_nombre.set(coleccion.nombre)
            self._set_descripcion(coleccion.descripcion)

    def _load_table(self):
        colecciones = self._generar_lista()
        if colecciones:
            row_data = [self._get_row(coleccion) for coleccion in colecciones]
            self.table_view.build_table_data(self.coldata, row_data)
            self.table_view.autofit_columns()

    def _get_row(self, coleccion: Coleccion) -> List:
        fila = []
        if isinstance(coleccion, Coleccion):
            fila.append(coleccion.id)
            fila.append(coleccion.nombre)
            fila.append(coleccion.creado_en)
            fila.append(coleccion.actualizado_en)
        return fila

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_seleccionar_fila(self, event):
        """
        Maneja el evento de doble clic en una fila de la tabla.
        Carga los datos de la colección seleccionada en el formulario de la pestaña 'Datos'.
        """
        # Obtener el item seleccionado
        item_seleccionado = self.table_view.view.selection()
        if not item_seleccionado:
            return

        # Obtener los datos de la fila
        datos_fila = self.table_view.view.item(item_seleccionado[0], "values")
        if not datos_fila:
            return

        id_coleccion = int(datos_fila[0])

        # Buscar el objeto Coleccion correspondiente y actualizar el formulario
        lista_colecciones = self._generar_lista()
        for i, coleccion in enumerate(lista_colecciones):
            if coleccion.id == id_coleccion:
                self.desplazar = i
                self._set_coleccion(coleccion)
                self.notebook.select(0)  # Cambiar a la pestaña "Datos"
                break

    def on_siguiente_elemento(self):
        lista = self._generar_lista()
        if not lista:
            return
        total_elementos = len(lista)
        if self.desplazar < (total_elementos - 1):
            self.desplazar += 1
            self.on_nuevo()
            coleccion = lista[self.desplazar]
            self._set_coleccion(coleccion=coleccion)

    def on_anterior_elemento(self):
        lista = self._generar_lista()
        if not lista:
            return
        if self.desplazar > 0:
            self.desplazar -= 1
            self.on_nuevo()
            coleccion = lista[self.desplazar]
            self._set_coleccion(coleccion=coleccion)

    def on_primer_elemento(self):
        colecciones = self._generar_lista()
        if colecciones:
            self.desplazar = 0
            self.on_nuevo()
            coleccion = colecciones[0]
            self._set_coleccion(coleccion=coleccion)

    def on_ultimo_elemento(self):
        colecciones = self._generar_lista()
        if colecciones:
            self.desplazar = len(colecciones) - 1
            self.on_nuevo()
            coleccion = colecciones[self.desplazar]
            self._set_coleccion(coleccion=coleccion)

    def on_aplicar(self):
        id_coleccion = self.var_id_coleccion.get()
        if id_coleccion == 0:
            # insertamos los datos de la coleccion
            coleccion = self._get_coleccion()
            if not coleccion.nombre:
                return
            new_id = coleccion.insertar()
            self.var_id_coleccion.set(new_id)
            # refrscamos la tabla
            self._load_table()
        elif id_coleccion != 0:
            # actualizamos los datos de la coleccion
            coleccion = self._get_coleccion()
            if not coleccion.nombre:
                return
            coleccion.actualizar()
            # refrscamos la tabla
            self._load_table()

    def on_nuevo(self):
        # limpiamos los datos, para un nuevo registro
        self.var_id_coleccion.set(0)
        self.var_nombre.set("")
        self._clear_descripcion()

    def on_eliminar(self):
        resp = messagebox.askokcancel(
            parent=self,
            title="Advertencia",
            message="Se eliminara el registro de la base de datos. ¿Esta seguro?",
        )
        if resp:
            coleccion = self._get_coleccion()
            if coleccion.id != 0:
                coleccion.eliminar()
                self.on_nuevo()
                self._load_table()
