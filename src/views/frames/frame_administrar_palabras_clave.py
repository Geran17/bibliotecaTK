from ttkbootstrap import (
    Frame,
    Label,
    Separator,
    Notebook,
    Button,
    Entry,
    Text,
    IntVar,
    LabelFrame,
    StringVar,
    Scrollbar,
)
from typing import List
from tkinter import messagebox
from ttkbootstrap.constants import *
from views.components.ui_tokens import (
    BUTTON_STYLE_OUTLINE_DANGER,
    BUTTON_STYLE_OUTLINE_SECONDARY,
    BUTTON_STYLE_OUTLINE_SUCCESS,
    BUTTON_STYLE_PRIMARY,
    FONT_TITLE,
    PADDING_COMPACT,
    PADDING_OUTER,
    PADDING_PANEL,
)
from ttkbootstrap.tableview import Tableview
from models.entities.palabra_clave import PalabraClave
from models.entities.consulta import Consulta


class AdministrarPalabrasClave(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # variables
        self.var_id_palabra_clave = IntVar()
        self.var_id_palabra_clave.set(0)
        self.var_palabra = StringVar()
        self.var_palabra.set("")
        # table view
        self.coldata = [
            {"text": "ID", "stretch": False, "width": 50},
            {"text": "Palabra", "stretch": True},
            {"text": "Creado", "stretch": False},
            {"text": "Actualizado", "stretch": False},
        ]
        # controlar desplazamiento
        self.desplazar = 0

        # cargamos los widgets
        self.crear_widgets()

        # cargamos las palabras clave en la tabla
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

        label_titulo = Label(
            frame,
            text="🔑 Administrar Palabras Clave",
            font=FONT_TITLE,
        )
        label_titulo.pack(side=TOP, fill=X, padx=PADDING_PANEL, pady=PADDING_PANEL)

        separador = Separator(frame)
        separador.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

    def panel_central(self, frame: Frame):
        self.notebook = Notebook(frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=PADDING_OUTER, pady=PADDING_OUTER)

        frame_datos = Frame(self.notebook, padding=(PADDING_PANEL, PADDING_PANEL))
        frame_datos.pack(side=TOP, fill=BOTH)
        self.tab_datos(frame=frame_datos)
        self.notebook.add(frame_datos, text="Datos")

        frame_explorar = Frame(self.notebook, padding=(PADDING_PANEL, PADDING_PANEL))
        frame_explorar.pack(side=TOP, fill=BOTH, padx=PADDING_COMPACT, pady=PADDING_COMPACT, expand=True)
        self.tab_explorar(frame=frame_explorar)
        self.notebook.add(frame_explorar, text="Explorar")

    def tab_datos(self, frame):
        # --- Frame para Detalles de la Palabra Clave ---
        lf_detalles = LabelFrame(frame, text="Detalles de la Palabra Clave", padding=PADDING_PANEL)
        lf_detalles.pack(side=TOP, fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER)
        lf_detalles.columnconfigure(1, weight=1)

        # Fila 1: ID
        Label(lf_detalles, text="ID:").grid(row=0, column=0, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
        ent_id = Entry(
            lf_detalles,
            state=READONLY,
            textvariable=self.var_id_palabra_clave,
            width=10,
            justify="center",
        )
        ent_id.grid(row=0, column=1, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)

        # Fila 2: Nombre
        Label(lf_detalles, text="Palabra:").grid(row=1, column=0, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
        ent_palabra = Entry(lf_detalles, textvariable=self.var_palabra)
        ent_palabra.grid(row=1, column=1, sticky=EW, padx=PADDING_OUTER, pady=PADDING_OUTER)

        # --- Frame para Descripción ---
        lf_descripcion = LabelFrame(frame, text="Descripción", padding=PADDING_PANEL)
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

        Button(frame_buttons, text="Aplicar", command=self.on_aplicar, style=BUTTON_STYLE_PRIMARY).pack(
            side=LEFT, fill=X, expand=TRUE, padx=PADDING_PANEL, pady=PADDING_PANEL
        )
        Button(frame_buttons, text="Eliminar", command=self.on_eliminar, style=BUTTON_STYLE_OUTLINE_DANGER).pack(
            side=LEFT, fill=X, expand=TRUE, padx=PADDING_PANEL, pady=PADDING_PANEL
        )
        Button(frame_buttons, text="Nuevo", command=self.on_nuevo, style=BUTTON_STYLE_OUTLINE_SUCCESS).pack(
            side=LEFT, fill=X, expand=TRUE, padx=PADDING_PANEL, pady=PADDING_PANEL
        )

        # Botones de navegación
        Button(frame_buttons, text="|<", command=self.on_primer_elemento, style=BUTTON_STYLE_OUTLINE_SECONDARY).pack(side=LEFT)
        Button(frame_buttons, text="<", command=self.on_anterior_elemento, style=BUTTON_STYLE_OUTLINE_SECONDARY).pack(side=LEFT)
        Button(frame_buttons, text=">", command=self.on_siguiente_elemento, style=BUTTON_STYLE_OUTLINE_SECONDARY).pack(side=LEFT)
        Button(frame_buttons, text=">|", command=self.on_ultimo_elemento, style=BUTTON_STYLE_OUTLINE_SECONDARY).pack(side=LEFT)

    def tab_explorar(self, frame):
        self.table_view = Tableview(frame, searchable=True, coldata=self.coldata, bootstyle=PRIMARY)
        self.table_view.pack(side=TOP, fill=BOTH, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.table_view.view.bind("<Double-1>", self.on_seleccionar_fila)

    def panel_inferior(self, frame: Frame):
        pass

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones privadas
    # └────────────────────────────────────────────────────────────┘

    def _generar_lista(self) -> List[PalabraClave]:
        consulta = Consulta()
        return consulta.get_palabras_clave()

    def _get_descripcion(self) -> str:
        return self.txt_descripcion.get("1.0", "end-1c")

    def _set_descripcion(self, descripcion):
        self.txt_descripcion.insert("1.0", descripcion)

    def _clear_descripcion(self):
        self.txt_descripcion.delete("1.0", "end")

    def _get_palabra_clave(self) -> PalabraClave:
        id_palabra_clave = self.var_id_palabra_clave.get()
        palabra_texto = self.var_palabra.get()
        descripcion = self._get_descripcion()
        palabra_clave = None
        if id_palabra_clave == 0:
            palabra_clave = PalabraClave(palabra=palabra_texto, descripcion=descripcion)
        else:
            palabra_clave = PalabraClave(
                palabra=palabra_texto, descripcion=descripcion, id=id_palabra_clave
            )
        return palabra_clave

    def _set_palabra_clave(self, palabra_clave: PalabraClave):
        if isinstance(palabra_clave, PalabraClave):
            self.var_id_palabra_clave.set(palabra_clave.id)
            self.var_palabra.set(palabra_clave.palabra)
            self._set_descripcion(palabra_clave.descripcion)

    def _load_table(self):
        palabras_clave = self._generar_lista()
        if palabras_clave:
            row_data = [self._get_row(palabra_clave) for palabra_clave in palabras_clave]
            self.table_view.build_table_data(self.coldata, row_data)
            self.table_view.autofit_columns()

    def _get_row(self, palabra_clave: PalabraClave) -> List:
        fila = []
        if isinstance(palabra_clave, PalabraClave):
            fila.append(palabra_clave.id)
            fila.append(palabra_clave.palabra)
            fila.append(palabra_clave.creado_en)
            fila.append(palabra_clave.actualizado_en)
        return fila

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_seleccionar_fila(self, event):
        item_seleccionado = self.table_view.view.selection()
        if not item_seleccionado:
            return

        datos_fila = self.table_view.view.item(item_seleccionado[0], "values")
        if not datos_fila:
            return

        id_palabra_clave = int(datos_fila[0])

        lista_palabras_clave = self._generar_lista()
        for i, palabra_clave in enumerate(lista_palabras_clave):
            if palabra_clave.id == id_palabra_clave:
                self.desplazar = i
                self._set_palabra_clave(palabra_clave)
                self.notebook.select(0)
                break

    def on_siguiente_elemento(self):
        lista = self._generar_lista()
        if not lista:
            return
        total_elementos = len(lista)
        if self.desplazar < (total_elementos - 1):
            self.desplazar += 1
            self.on_nuevo()
            palabra_clave = lista[self.desplazar]
            self._set_palabra_clave(palabra_clave=palabra_clave)

    def on_anterior_elemento(self):
        lista = self._generar_lista()
        if not lista:
            return
        if self.desplazar > 0:
            self.desplazar -= 1
            self.on_nuevo()
            palabra_clave = lista[self.desplazar]
            self._set_palabra_clave(palabra_clave=palabra_clave)

    def on_primer_elemento(self):
        palabras_clave = self._generar_lista()
        if palabras_clave:
            self.desplazar = 0
            self.on_nuevo()
            palabra_clave = palabras_clave[0]
            self._set_palabra_clave(palabra_clave=palabra_clave)

    def on_ultimo_elemento(self):
        palabras_clave = self._generar_lista()
        if palabras_clave:
            self.desplazar = len(palabras_clave) - 1
            self.on_nuevo()
            palabra_clave = palabras_clave[self.desplazar]
            self._set_palabra_clave(palabra_clave=palabra_clave)

    def on_aplicar(self):
        id_palabra_clave = self.var_id_palabra_clave.get()
        if id_palabra_clave == 0:
            palabra_clave = self._get_palabra_clave()
            if not palabra_clave.palabra:
                messagebox.showwarning(
                    "Campo Vacío", "La palabra clave no puede estar vacía.", parent=self
                )
                return
            new_id = palabra_clave.insertar()
            self.var_id_palabra_clave.set(new_id)
            self._load_table()
        elif id_palabra_clave != 0:
            palabra_clave = self._get_palabra_clave()
            if not palabra_clave.palabra:
                messagebox.showwarning(
                    "Campo Vacío", "La palabra clave no puede estar vacía.", parent=self
                )
                return
            palabra_clave.actualizar()
            self._load_table()

    def on_nuevo(self):
        self.var_id_palabra_clave.set(0)
        self.var_palabra.set("")
        self._clear_descripcion()

    def on_eliminar(self):
        resp = messagebox.askokcancel(
            parent=self,
            title="Advertencia",
            message="Se eliminará el registro de la base de datos. ¿Está seguro?",
        )
        if resp:
            palabra_clave = self._get_palabra_clave()
            if palabra_clave.id != 0:
                palabra_clave.eliminar()
                self.on_nuevo()
                self._load_table()
