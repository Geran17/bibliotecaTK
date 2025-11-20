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
            text="🔑 Administrar Palabras Clave",
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
            textvariable=self.var_id_palabra_clave,
            width=10,
            justify="center",
        )
        ent_id.pack(side=LEFT, fill=X, padx=1, pady=1)

        lbl_palabra = Label(frame_nombre, padding=(1, 1), text="Palabra Clave: ")
        lbl_palabra.pack(side=LEFT, fill=X, padx=1, pady=1)

        ent_palabra = Entry(frame_nombre, textvariable=self.var_palabra)
        ent_palabra.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

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
        btn_aplicar.pack(side=LEFT, fill=X, padx=1, pady=1, expand=TRUE)

        btn_eliminar = Button(frame_buttons, text="Eliminar", command=self.on_eliminar)
        btn_eliminar.pack(side=LEFT, fill=X, padx=1, pady=1, expand=TRUE)

        btn_nuevo = Button(frame_buttons, text="Nuevo", command=self.on_nuevo)
        btn_nuevo.pack(side=LEFT, fill=X, padx=1, pady=1, expand=TRUE)

        btn_primero = Button(frame_buttons, text="|<", command=self.on_primer_elemento)
        btn_primero.pack(side=LEFT, fill=X, padx=1, pady=1)

        btn_anterior = Button(frame_buttons, text="<", command=self.on_anterior_elemento)
        btn_anterior.pack(side=LEFT, fill=X, padx=1, pady=1)

        btn_siguiente = Button(frame_buttons, text=">", command=self.on_siguiente_elemento)
        btn_siguiente.pack(side=LEFT, fill=X, padx=1, pady=1)

        btn_ultimo = Button(frame_buttons, text=">|", command=self.on_ultimo_elemento)
        btn_ultimo.pack(side=LEFT, fill=X, padx=1, pady=1)

    def tab_explorar(self, frame):
        self.table_view = Tableview(frame, searchable=True, coldata=self.coldata)
        self.table_view.pack(side=TOP, fill=BOTH, padx=1, pady=1)
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
            self.table_view.delete_rows()
            for palabra_clave in palabras_clave:
                fila = self._get_row(palabra_clave=palabra_clave)
                if fila:
                    self.table_view.insert_row(values=fila)

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
