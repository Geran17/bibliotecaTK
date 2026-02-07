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
    Combobox,
)
from tkinter import ttk
from typing import List, Dict
from tkinter import messagebox
from ttkbootstrap.constants import *
from views.components.ui_tokens import PADDING_COMPACT, PADDING_OUTER, PADDING_PANEL
from models.entities.categoria import Categoria
from models.entities.consulta import Consulta


class AdministrarCategorias(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # variables
        self.var_id_categoria = IntVar(value=0)
        self.var_nombre = StringVar()
        self.var_id_padre = IntVar(value=0)

        # controlar desplazamiento
        self.desplazar = 0
        self.categorias_lista: List[Categoria] = []
        self.categorias_map: Dict[int, Categoria] = {}

        # cargamos los widgets
        self.crear_widgets()

        # cargamos las categorias en la tabla y el combobox
        self._load_data()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        self.frame_superior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_superior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.panel_superior(frame=self.frame_superior)

        self.frame_central = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.panel_central(frame=self.frame_central)

        self.frame_inferior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_inferior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.panel_inferior(frame=self.frame_inferior)

    def panel_superior(self, frame: Frame):
        estilo_fuente_titulo = ('Helvetica', 14, 'bold')
        label_titulo = Label(frame, text="🗂️ Administrar Categorías", font=estilo_fuente_titulo)
        label_titulo.pack(side=TOP, fill=X, padx=PADDING_PANEL, pady=PADDING_PANEL)
        separador = Separator(frame)
        separador.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

    def panel_central(self, frame: Frame):
        self.notebook = Notebook(frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=PADDING_OUTER, pady=PADDING_OUTER)

        frame_datos = Frame(self.notebook, padding=(PADDING_PANEL, PADDING_PANEL))
        self.tab_datos(frame=frame_datos)
        self.notebook.add(frame_datos, text="Datos")

        frame_explorar = Frame(self.notebook, padding=(PADDING_PANEL, PADDING_PANEL))
        self.tab_explorar(frame=frame_explorar)
        self.notebook.add(frame_explorar, text="Explorar")

    def tab_datos(self, frame):
        # --- Frame para Detalles de la Categoría ---
        lf_detalles = LabelFrame(frame, text="Detalles de la Categoría", padding=10)
        lf_detalles.pack(side=TOP, fill=X, padx=PADDING_OUTER, pady=PADDING_OUTER)
        lf_detalles.columnconfigure(1, weight=1)

        # Fila 1: ID y Nombre
        Label(lf_detalles, text="ID:").grid(row=0, column=0, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
        Entry(
            lf_detalles,
            state=READONLY,
            textvariable=self.var_id_categoria,
            width=10,
            justify="center",
        ).grid(row=0, column=1, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)

        Label(lf_detalles, text="Nombre:").grid(row=1, column=0, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
        Entry(lf_detalles, textvariable=self.var_nombre).grid(
            row=1, column=1, sticky=EW, padx=PADDING_OUTER, pady=PADDING_OUTER
        )

        # Fila 2: Categoría Padre
        Label(lf_detalles, text="Categoría Padre:").grid(row=2, column=0, sticky=W, padx=PADDING_OUTER, pady=PADDING_OUTER)
        self.combo_padre = Combobox(lf_detalles, state="readonly")
        self.combo_padre.grid(row=2, column=1, sticky=EW, padx=PADDING_OUTER, pady=PADDING_OUTER)

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
        Button(frame_buttons, text="|<", command=self.on_primer_elemento, style="secondary.Outline.TButton").pack(side=LEFT)
        Button(frame_buttons, text="<", command=self.on_anterior_elemento, style="secondary.Outline.TButton").pack(side=LEFT)
        Button(frame_buttons, text=">", command=self.on_siguiente_elemento, style="secondary.Outline.TButton").pack(side=LEFT)
        Button(frame_buttons, text=">|", command=self.on_ultimo_elemento, style="secondary.Outline.TButton").pack(side=LEFT)

    def tab_explorar(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.treeview = ttk.Treeview(
            frame, columns=("nombre", "creado", "actualizado"), show="tree headings"
        )
        self.treeview.heading("#0", text="Categoría")
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("creado", text="Creado")
        self.treeview.heading("actualizado", text="Actualizado")

        self.treeview.column("nombre", width=200, anchor=W)
        self.treeview.column("creado", width=120, anchor=CENTER)
        self.treeview.column("actualizado", width=120, anchor=CENTER)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.treeview.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.treeview.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.treeview.bind("<Double-1>", self.on_seleccionar_fila)

    def panel_inferior(self, frame: Frame):
        pass

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones de Datos
    # └────────────────────────────────────────────────────────────┘

    def _load_data(self):
        """Carga todas las categorías y actualiza la UI."""
        self.categorias_lista = Consulta().get_categorias()
        self.categorias_map = {cat.id: cat for cat in self.categorias_lista}
        self._load_treeview()
        self._load_combobox()

    def _load_treeview(self):
        """Limpia y recarga el Treeview con las categorías anidadas."""
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        # Crear un diccionario para encontrar hijos fácilmente
        nodos_hijos = {}
        for cat in self.categorias_lista:
            parent_id = cat.id_padre if cat.id_padre is not None else 0
            if parent_id not in nodos_hijos:
                nodos_hijos[parent_id] = []
            nodos_hijos[parent_id].append(cat)

        # Función recursiva para añadir nodos
        def anadir_nodos(parent_id, parent_iid):
            if parent_id in nodos_hijos:
                for cat in sorted(nodos_hijos[parent_id], key=lambda x: x.nombre):
                    iid = self.treeview.insert(
                        parent_iid,
                        "end",
                        iid=cat.id,
                        text=f" {cat.nombre}",
                        values=(cat.nombre, cat.creado_en, cat.actualizado_en),
                    )
                    anadir_nodos(cat.id, iid)

        anadir_nodos(0, "")

    def _load_combobox(self):
        """Carga las categorías en el Combobox para seleccionar el padre."""
        self.combo_padre['values'] = ["[Ninguna]"] + [cat.nombre for cat in self.categorias_lista]
        self.combo_padre.set("[Ninguna]")

    def _get_descripcion(self) -> str:
        return self.txt_descripcion.get("1.0", "end-1c")

    def _set_descripcion(self, descripcion):
        self.txt_descripcion.delete("1.0", "end")
        if descripcion:
            self.txt_descripcion.insert("1.0", descripcion)

    def _get_categoria(self) -> Categoria:
        id_categoria = self.var_id_categoria.get()
        nombre = self.var_nombre.get()
        descripcion = self._get_descripcion()

        nombre_padre = self.combo_padre.get()
        id_padre = None
        if nombre_padre != "[Ninguna]":
            for cat in self.categorias_lista:
                if cat.nombre == nombre_padre:
                    id_padre = cat.id
                    break

        return Categoria(
            nombre=nombre,
            descripcion=descripcion,
            id=id_categoria if id_categoria != 0 else None,
            id_padre=id_padre,
        )

    def _set_categoria(self, categoria: Categoria):
        self.var_id_categoria.set(categoria.id or 0)
        self.var_nombre.set(categoria.nombre or "")
        self._set_descripcion(categoria.descripcion or "")

        if categoria.id_padre and categoria.id_padre in self.categorias_map:
            self.combo_padre.set(self.categorias_map[categoria.id_padre].nombre)
        else:
            self.combo_padre.set("[Ninguna]")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_seleccionar_fila(self, event):
        item_id = self.treeview.focus()
        if not item_id:
            return

        id_categoria = int(item_id)
        if id_categoria in self.categorias_map:
            categoria = self.categorias_map[id_categoria]
            self.desplazar = self.categorias_lista.index(categoria)
            self._set_categoria(categoria)
            self.notebook.select(0)

    def on_siguiente_elemento(self):
        if not self.categorias_lista:
            return
        if self.desplazar < (len(self.categorias_lista) - 1):
            self.desplazar += 1
            self.on_nuevo()
            self._set_categoria(self.categorias_lista[self.desplazar])

    def on_anterior_elemento(self):
        if not self.categorias_lista:
            return
        if self.desplazar > 0:
            self.desplazar -= 1
            self.on_nuevo()
            self._set_categoria(self.categorias_lista[self.desplazar])

    def on_primer_elemento(self):
        if self.categorias_lista:
            self.desplazar = 0
            self.on_nuevo()
            self._set_categoria(self.categorias_lista[0])

    def on_ultimo_elemento(self):
        if self.categorias_lista:
            self.desplazar = len(self.categorias_lista) - 1
            self.on_nuevo()
            self._set_categoria(self.categorias_lista[self.desplazar])

    def on_aplicar(self):
        categoria = self._get_categoria()
        if not categoria.nombre:
            messagebox.showwarning(
                "Campo Vacío", "El nombre de la categoría no puede estar vacío.", parent=self
            )
            return

        # Evitar que una categoría sea su propio padre
        if categoria.id is not None and categoria.id == categoria.id_padre:
            messagebox.showerror(
                "Error de Lógica",
                "Una categoría no puede ser su propia categoría padre.",
                parent=self,
            )
            return

        if categoria.id == 0 or categoria.id is None:
            new_id = categoria.insertar()
            if new_id:
                self.var_id_categoria.set(new_id)
                messagebox.showinfo("Éxito", "Categoría creada correctamente.", parent=self)
            else:
                messagebox.showerror("Error", "No se pudo crear la categoría.", parent=self)
        else:
            if categoria.actualizar():
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente.", parent=self)
            else:
                messagebox.showerror("Error", "No se pudo actualizar la categoría.", parent=self)

        self._load_data()

    def on_nuevo(self):
        self.var_id_categoria.set(0)
        self.var_nombre.set("")
        self._set_descripcion("")
        self.combo_padre.set("[Ninguna]")
        if self.categorias_lista:
            self.desplazar = len(self.categorias_lista)

    def on_eliminar(self):
        id_categoria = self.var_id_categoria.get()
        if id_categoria == 0:
            messagebox.showinfo(
                "Información", "No hay ninguna categoría seleccionada para eliminar.", parent=self
            )
            return

        # Verificar si la categoría tiene hijos
        tiene_hijos = any(cat.id_padre == id_categoria for cat in self.categorias_lista)
        if tiene_hijos:
            messagebox.showerror(
                "Error al eliminar",
                "No se puede eliminar una categoría que tiene subcategorías.",
                parent=self,
            )
            return

        resp = messagebox.askokcancel(
            parent=self,
            title="Confirmar Eliminación",
            message=f"Se eliminará la categoría '{self.var_nombre.get()}' de la base de datos. ¿Está seguro?",
        )
        if resp:
            categoria = self._get_categoria()
            if categoria.eliminar():
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente.", parent=self)
                self.on_nuevo()
                self._load_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría.", parent=self)
