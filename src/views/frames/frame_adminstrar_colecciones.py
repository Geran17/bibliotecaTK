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
            text="📚 Administrar Colecciones",
            font=estilo_fuente_titulo,  # Aplicamos la fuente
        )
        label_titulo.pack(side=TOP, fill=X, padx=2, pady=2)

        separador = Separator(frame)
        separador.pack(side=TOP, fill=X, padx=1, pady=1)

    def panel_central(self, frame: Frame):
        # 1. Crear el widget Notebook
        self.notebook = Notebook(frame)
        self.notebook.pack(
            fill=BOTH, expand=True, padx=5, pady=5
        )  # Lo expandimos para que ocupe el frame central

        # frame datos
        frame_datos = Frame(self.notebook, padding=(2, 2))
        frame_datos.pack(side=TOP, fill=BOTH)
        self.tab_datos(frame=frame_datos)
        self.notebook.add(frame_datos, text="Datos")

        # frame explorar
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
            textvariable=self.var_id_coleccion,
            width=10,
            justify="center",
        )
        ent_id.pack(side=LEFT, fill=X, padx=1, pady=1)

        lbl_coleccion = Label(frame_nombre, padding=(1, 1), text="Coleccion: ")
        lbl_coleccion.pack(side=LEFT, fill=X, padx=1, pady=1)

        ent_coleccion = Entry(frame_nombre, textvariable=self.var_nombre)
        ent_coleccion.pack(side=LEFT, fill=X, padx=1, pady=1, expand=True)

        frame_descripcion = Frame(frame, padding=(1, 1))
        frame_descripcion.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)

        lbl_descripcion = Label(frame_descripcion, text="Descripcion: ")
        lbl_descripcion.pack(side=TOP, fill=X, padx=1, pady=1)

        # barra de desplazamiento
        scrollbar = Scrollbar(frame_descripcion)

        self.txt_descripcion = Text(
            frame_descripcion, wrap=WORD, height=10, yscrollcommand=scrollbar.set
        )

        # empaquetamos el scrollbar
        scrollbar.pack(side=RIGHT, fill=Y)

        # empaquetamos el Text
        self.txt_descripcion.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # vinculamos
        scrollbar.config(command=self.txt_descripcion.yview)

        # frame buttons
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
        consulta = Consulta()
        colecciones = consulta.get_colecciones()
        if colecciones:
            # limpiamos la tabla
            self.table_view.delete_rows()
            for coleccion in colecciones:
                fila = self._get_row(coleccion=coleccion)
                if fila:
                    self.table_view.insert_row(values=fila)

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
