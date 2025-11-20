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
    Scrollbar,
)
from typing import List
from tkinter import messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from models.entities.etiqueta import Etiqueta
from models.entities.consulta import Consulta


class AdministrarEtiquetas(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # variables
        self.var_id_etiqueta = IntVar()
        self.var_id_etiqueta.set(0)
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

        # cargamos las etiquetas en la tabla
        self._load_table()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        # Frame superior
        self.frame_superior = Frame(self, padding=(1, 1))
        self.frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)
        self.panel_superior(frame=self.frame_superior)

        # Frame central
        self.frame_central = Frame(self, padding=(1, 1))
        self.frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
        self.panel_central(frame=self.frame_central)

        # Frame inferior
        self.frame_inferior = Frame(self, padding=(1, 1))
        self.frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)
        self.panel_inferior(frame=self.frame_inferior)

    def panel_superior(self, frame: Frame):

        estilo_fuente_titulo = ('Helvetica', 14, 'bold')

        label_titulo = Label(
            frame,
            text="🏷️ Administrar Etiquetas",
            font=estilo_fuente_titulo,
        )
        label_titulo.pack(side=TOP, fill=X, padx=2, pady=2)

        separador = Separator(frame)
        separador.pack(side=TOP, fill=X, padx=1, pady=1)

    def panel_central(self, frame: Frame):
        self.notebook = Notebook(frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)

        frame_datos = Frame(self.notebook, padding=(2, 2))
        frame_datos.pack(side=TOP, fill=BOTH)
        self.tab_datos(frame=frame_datos)
        self.notebook.add(frame_datos, text="Datos")

        frame_explorar = Frame(self.notebook, padding=(2, 2))
        frame_explorar.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)
        self.tab_explorar(frame=frame_explorar)
        self.notebook.add(frame_explorar, text="Explorar")

    def tab_datos(self, frame):
        frame_nombre = Frame(frame, padding=(1, 1))
        frame_nombre.pack(side=TOP, fill=X, padx=1, pady=1)

        lbl_id = Label(frame_nombre, padding=(1, 1), text="Id: ")
        lbl_id.pack(side=LEFT, fill=X, padx=1, pady=1)

        ent_id = Entry(
            frame_nombre,
            state=READONLY,
            textvariable=self.var_id_etiqueta,
            width=10,
            justify="center",
        )
        ent_id.pack(side=LEFT, fill=X, padx=1, pady=1)

        lbl_etiqueta = Label(frame_nombre, padding=(1, 1), text="Etiqueta: ")
        lbl_etiqueta.pack(side=LEFT, fill=X, padx=1, pady=1)

        ent_etiqueta = Entry(frame_nombre, textvariable=self.var_nombre)
        ent_etiqueta.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        frame_descripcion = Frame(frame, padding=(1, 1))
        frame_descripcion.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)

        lbl_descripcion = Label(frame_descripcion, text="Descripcion: ")
        lbl_descripcion.pack(side=TOP, fill=X, padx=1, pady=1)

        scrollbar = Scrollbar(frame_descripcion)
        self.txt_descripcion = Text(
            frame_descripcion, wrap=WORD, height=10, yscrollcommand=scrollbar.set
        )
        scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_descripcion.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.txt_descripcion.yview)

        frame_buttons = Frame(frame, padding=(1, 1))
        frame_buttons.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_aplicar = Button(frame_buttons, text="Aplicar", command=self.on_aplicar)
        btn_aplicar.pack(side=LEFT, fill=X, padx=0, pady=0, expand=TRUE)

        btn_eliminar = Button(frame_buttons, text="Eliminar", command=self.on_eliminar)
        btn_eliminar.pack(side=LEFT, fill=X, padx=0, pady=0, expand=TRUE)

        btn_nuevo = Button(frame_buttons, text="Nuevo", command=self.on_nuevo)
        btn_nuevo.pack(side=LEFT, fill=X, padx=0, pady=0, expand=TRUE)

        btn_primero = Button(frame_buttons, text="|<", command=self.on_primer_elemento)
        btn_primero.pack(side=LEFT, fill=X, padx=0, pady=0)

        btn_anterior = Button(frame_buttons, text="<", command=self.on_anterior_elemento)
        btn_anterior.pack(side=LEFT, fill=X, padx=0, pady=0)

        btn_siguiente = Button(frame_buttons, text=">", command=self.on_siguiente_elemento)
        btn_siguiente.pack(side=LEFT, fill=X, padx=0, pady=0)

        btn_ultimo = Button(frame_buttons, text=">|", command=self.on_ultimo_elemento)
        btn_ultimo.pack(side=LEFT, fill=X, padx=0, pady=0)

    def tab_explorar(self, frame):
        self.table_view = Tableview(frame, searchable=True, coldata=self.coldata)
        self.table_view.pack(side=TOP, fill=BOTH, padx=1, pady=1)
        self.table_view.view.bind("<Double-1>", self.on_seleccionar_fila)

    def panel_inferior(self, frame: Frame):
        pass

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones privadas
    # └────────────────────────────────────────────────────────────┘

    def _generar_lista(self) -> List[Etiqueta]:
        consulta = Consulta()
        return consulta.get_etiquetas()

    def _get_descripcion(self) -> str:
        return self.txt_descripcion.get("1.0", "end-1c")

    def _set_descripcion(self, descripcion):
        self.txt_descripcion.insert("1.0", descripcion)

    def _clear_descripcion(self):
        self.txt_descripcion.delete("1.0", "end")

    def _get_etiqueta(self) -> Etiqueta:
        id_etiqueta = self.var_id_etiqueta.get()
        nombre = self.var_nombre.get()
        descripcion = self._get_descripcion()
        etiqueta = None
        if id_etiqueta == 0:
            etiqueta = Etiqueta(nombre=nombre, descripcion=descripcion)
        else:
            etiqueta = Etiqueta(nombre=nombre, descripcion=descripcion, id=id_etiqueta)
        return etiqueta

    def _set_etiqueta(self, etiqueta: Etiqueta):
        if isinstance(etiqueta, Etiqueta):
            self.var_id_etiqueta.set(etiqueta.id)
            self.var_nombre.set(etiqueta.nombre)
            self._set_descripcion(etiqueta.descripcion)

    def _load_table(self):
        etiquetas = self._generar_lista()
        if etiquetas:
            self.table_view.delete_rows()
            for etiqueta in etiquetas:
                fila = self._get_row(etiqueta=etiqueta)
                if fila:
                    self.table_view.insert_row(values=fila)

    def _get_row(self, etiqueta: Etiqueta) -> List:
        fila = []
        if isinstance(etiqueta, Etiqueta):
            fila.append(etiqueta.id)
            fila.append(etiqueta.nombre)
            fila.append(etiqueta.creado_en)
            fila.append(etiqueta.actualizado_en)
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

        id_etiqueta = int(datos_fila[0])

        lista_etiquetas = self._generar_lista()
        for i, etiqueta in enumerate(lista_etiquetas):
            if etiqueta.id == id_etiqueta:
                self.desplazar = i
                self._set_etiqueta(etiqueta)
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
            etiqueta = lista[self.desplazar]
            self._set_etiqueta(etiqueta=etiqueta)

    def on_anterior_elemento(self):
        lista = self._generar_lista()
        if not lista:
            return
        if self.desplazar > 0:
            self.desplazar -= 1
            self.on_nuevo()
            etiqueta = lista[self.desplazar]
            self._set_etiqueta(etiqueta=etiqueta)

    def on_primer_elemento(self):
        etiquetas = self._generar_lista()
        if etiquetas:
            self.desplazar = 0
            self.on_nuevo()
            etiqueta = etiquetas[0]
            self._set_etiqueta(etiqueta=etiqueta)

    def on_ultimo_elemento(self):
        etiquetas = self._generar_lista()
        if etiquetas:
            self.desplazar = len(etiquetas) - 1
            self.on_nuevo()
            etiqueta = etiquetas[self.desplazar]
            self._set_etiqueta(etiqueta=etiqueta)

    def on_aplicar(self):
        id_etiqueta = self.var_id_etiqueta.get()
        if id_etiqueta == 0:
            etiqueta = self._get_etiqueta()
            if not etiqueta.nombre:
                messagebox.showwarning(
                    "Campo Vacío", "El nombre de la etiqueta no puede estar vacío.", parent=self
                )
                return
            new_id = etiqueta.insertar()
            self.var_id_etiqueta.set(new_id)
            self._load_table()
        elif id_etiqueta != 0:
            etiqueta = self._get_etiqueta()
            if not etiqueta.nombre:
                messagebox.showwarning(
                    "Campo Vacío", "El nombre de la etiqueta no puede estar vacío.", parent=self
                )
                return
            etiqueta.actualizar()
            self._load_table()

    def on_nuevo(self):
        self.var_id_etiqueta.set(0)
        self.var_nombre.set("")
        self._clear_descripcion()

    def on_eliminar(self):
        resp = messagebox.askokcancel(
            parent=self,
            title="Advertencia",
            message="Se eliminará el registro de la base de datos. ¿Está seguro?",
        )
        if resp:
            etiqueta = self._get_etiqueta()
            if etiqueta.id != 0:
                etiqueta.eliminar()
                self.on_nuevo()
                self._load_table()
