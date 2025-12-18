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
from ttkbootstrap.tableview import Tableview
from models.entities.grupo import Grupo
from models.entities.consulta import Consulta


class AdministrarGrupos(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # variables
        self.var_id_grupo = IntVar()
        self.var_id_grupo.set(0)
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

        # cargamos los grupos en la tabla
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
            text="🗂️ Administrar Grupos",
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
        # --- Frame para Detalles del Grupo ---
        lf_detalles = LabelFrame(frame, text="Detalles del Grupo", padding=10)
        lf_detalles.pack(side=TOP, fill=X, padx=5, pady=5)
        lf_detalles.columnconfigure(1, weight=1)

        # Fila 1: ID
        Label(lf_detalles, text="ID:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        ent_id = Entry(
            lf_detalles,
            state=READONLY,
            textvariable=self.var_id_grupo,
            width=10,
            justify="center",
        )
        ent_id.grid(row=0, column=1, sticky=W, padx=5, pady=5)

        # Fila 2: Nombre
        Label(lf_detalles, text="Nombre:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        ent_grupo = Entry(lf_detalles, textvariable=self.var_nombre)
        ent_grupo.grid(row=1, column=1, sticky=EW, padx=5, pady=5)

        # --- Frame para Descripción ---
        lf_descripcion = LabelFrame(frame, text="Descripción", padding=10)
        lf_descripcion.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=True)

        scrollbar = Scrollbar(lf_descripcion)
        self.txt_descripcion = Text(
            lf_descripcion, wrap=WORD, height=5, yscrollcommand=scrollbar.set
        )
        scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_descripcion.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.config(command=self.txt_descripcion.yview)

        # --- Frame para Botones de Acción ---
        frame_buttons = Frame(frame, padding=(1, 1))
        frame_buttons.pack(side=TOP, fill=X, padx=1, pady=1)
        frame_buttons.columnconfigure((0, 1, 2), weight=1)

        Button(frame_buttons, text="Aplicar", command=self.on_aplicar).pack(
            side=LEFT, fill=X, expand=TRUE, padx=2, pady=2
        )
        Button(frame_buttons, text="Eliminar", command=self.on_eliminar).pack(
            side=LEFT, fill=X, expand=TRUE, padx=2, pady=2
        )
        Button(frame_buttons, text="Nuevo", command=self.on_nuevo).pack(
            side=LEFT, fill=X, expand=TRUE, padx=2, pady=2
        )

        # Botones de navegación
        Button(frame_buttons, text="|<", command=self.on_primer_elemento).pack(side=LEFT)
        Button(frame_buttons, text="<", command=self.on_anterior_elemento).pack(side=LEFT)
        Button(frame_buttons, text=">", command=self.on_siguiente_elemento).pack(side=LEFT)
        Button(frame_buttons, text=">|", command=self.on_ultimo_elemento).pack(side=LEFT)

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

    def _generar_lista(self) -> List[Grupo]:
        consulta = Consulta()
        return consulta.get_grupos()

    def _get_descripcion(self) -> str:
        return self.txt_descripcion.get("1.0", "end-1c")

    def _set_descripcion(self, descripcion):
        self.txt_descripcion.insert("1.0", descripcion)

    def _clear_descripcion(self):
        self.txt_descripcion.delete("1.0", "end")

    def _get_grupo(self) -> Grupo:
        id_grupo = self.var_id_grupo.get()
        nombre = self.var_nombre.get()
        descipcion = self._get_descripcion()
        grupo = None
        if id_grupo == 0:
            grupo = Grupo(nombre=nombre, descripcion=descipcion)
        else:
            grupo = Grupo(nombre=nombre, descripcion=descipcion, id=id_grupo)
        return grupo

    def _set_grupo(self, grupo: Grupo):
        if isinstance(grupo, Grupo):
            self.var_id_grupo.set(grupo.id)
            self.var_nombre.set(grupo.nombre)
            self._set_descripcion(grupo.descripcion)

    def _load_table(self):
        grupos = self._generar_lista()
        if grupos:
            row_data = [self._get_row(grupo) for grupo in grupos]
            self.table_view.build_table_data(self.coldata, row_data)
            self.table_view.autofit_columns()

    def _get_row(self, grupo: Grupo) -> List:
        fila = []
        if isinstance(grupo, Grupo):
            fila.append(grupo.id)
            fila.append(grupo.nombre)
            fila.append(grupo.creado_en)
            fila.append(grupo.actualizado_en)
        return fila

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_seleccionar_fila(self, event):
        """
        Maneja el evento de doble clic en una fila de la tabla.
        Carga los datos del grupo seleccionado en el formulario de la pestaña 'Datos'.
        """
        # Obtener el item seleccionado
        item_seleccionado = self.table_view.view.selection()
        if not item_seleccionado:
            return

        # Obtener los datos de la fila
        datos_fila = self.table_view.view.item(item_seleccionado[0], "values")
        if not datos_fila:
            return

        id_grupo = int(datos_fila[0])

        # Buscar el objeto Grupo correspondiente y actualizar el formulario
        lista_grupos = self._generar_lista()
        for i, grupo in enumerate(lista_grupos):
            if grupo.id == id_grupo:
                self.desplazar = i
                self._set_grupo(grupo)
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
            grupo = lista[self.desplazar]
            self._set_grupo(grupo=grupo)

    def on_anterior_elemento(self):
        lista = self._generar_lista()
        if not lista:
            return
        if self.desplazar > 0:
            self.desplazar -= 1
            self.on_nuevo()
            grupo = lista[self.desplazar]
            self._set_grupo(grupo=grupo)

    def on_primer_elemento(self):
        grupos = self._generar_lista()
        if grupos:
            self.desplazar = 0
            self.on_nuevo()
            grupo = grupos[0]
            self._set_grupo(grupo=grupo)

    def on_ultimo_elemento(self):
        grupos = self._generar_lista()
        if grupos:
            self.desplazar = len(grupos) - 1
            self.on_nuevo()
            grupo = grupos[self.desplazar]
            self._set_grupo(grupo=grupo)

    def on_aplicar(self):
        id_grupo = self.var_id_grupo.get()
        if id_grupo == 0:
            # insertamos los datos del grupo
            grupo = self._get_grupo()
            if not grupo.nombre:
                return
            new_id = grupo.insertar()
            self.var_id_grupo.set(new_id)
            # refrscamos la tabla
            self._load_table()
        elif id_grupo != 0:
            # actualizamos los datos del grupo
            grupo = self._get_grupo()
            if not grupo.nombre:
                return
            grupo.actualizar()
            # refrscamos la tabla
            self._load_table()

    def on_nuevo(self):
        # limpiamos los datos, para un nuevo registro
        self.var_id_grupo.set(0)
        self.var_nombre.set("")
        self._clear_descripcion()

    def on_eliminar(self):
        resp = messagebox.askokcancel(
            parent=self,
            title="Advertencia",
            message="Se eliminara el registro de la base de datos. ¿Esta seguro?",
        )
        if resp:
            grupo = self._get_grupo()
            if grupo.id != 0:
                grupo.eliminar()
                self.on_nuevo()
                self._load_table()
