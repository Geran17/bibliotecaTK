from os.path import exists, join, expanduser
from pathlib import Path
from tkinter import filedialog, messagebox, Toplevel, Label, Entry, Button, StringVar, Frame
from ttkbootstrap import (
    Frame as TTFrame,
    Combobox,
    Button as TTButton,
    Menubutton,
    Menu,
    Label as TTLabel,
    Progressbar,
    Radiobutton,
    LabelFrame,
    Entry as TTEntry,
    StringVar as TTStringVar,
    Notebook,
    Separator,
    PanedWindow,
)
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from models.controllers.configuracion_controller import ConfiguracionController
from models.controllers.controlar_seleccion_documentos import ControlarSeleccionDocumentos
from models.controllers.controlar_todos import ControlarTodos
from models.controllers.controlar_importacion_documento import ControlarImporetacionDocumento
from models.controllers.controlar_existentes import ControlarExistentes
from utilities.auxiliar import (
    abrir_archivo,
    copiar_archivo,
    mover_archivo,
    eliminar_archivo,
    renombrar_archivo,
    papelera_archivo,
)
from views.components.context_menu_factory import ContextMenuFactory
from views.components.ui_tokens import PADDING_COMPACT, PADDING_OUTER, PADDING_PANEL


class FrameImportarDocumento(TTFrame):
    """Frame principal para la importación de documentos"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Variables
        self.coldata = [
            {"text": "Nombre", "stretch": False},
            {"text": "Tamaño", "stretch": False},
            {"text": "Creado", "stretch": False},
            {"text": "Modificado", "stretch": False},
            {"text": "Existe", "stretch": False},
            {"text": "Hash", "stretch": True},  # Ocultar columna
            {"text": "Ruta", "stretch": True},  # Ocultar columna
        ]
        self.operaciones = [
            "Seleccionar uno o mas archivos",
            "Seleccionar archivos por extension",
            "Seleccionar archivos por extension incluir directorios",
        ]
        self.filetypes_ebooks = (
            ("Documentos PDF", "*.pdf"),
            ("Archivos EPUB", "*.epub"),
            ("Archivos MOBI/AZW3", "*.mobi *.azw3"),
            ("Todos los archivos", "*.*"),
        )
        self.var_nombre_documento = TTStringVar()
        self.var_opcion_importacion = TTStringVar()
        self.var_opcion_importacion.set("copiar")

        # para ocultar el menu
        self.ocultar_menu = False
        # obtenemos la ruta del archivo
        self.ruta_archivo = ""
        # variable para almacenar la ruta padre del archivo
        self.ruta_padre_archivo = ""
        # variable para almacenar el focus
        self.item_focus = ""

        # creamos los widgets
        self.crear_widgets()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        """Crea todos los widgets del frame"""
        # Frame Superior
        self.frame_superior = TTFrame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_superior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)
        self.widgets_frame_superior(frame=self.frame_superior)

        # Frame Central
        self.frame_central = TTFrame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_central.pack(
            side=TOP,
            fill=BOTH,
            expand=True,
            padx=PADDING_COMPACT,
            pady=PADDING_COMPACT,
        )
        self.widgets_frame_central(frame=self.frame_central)

        # Frame Inferior
        self.frame_inferior = TTFrame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_inferior.pack(
            side=TOP,
            fill=X,
            expand=False,
            padx=PADDING_COMPACT,
            pady=PADDING_COMPACT,
        )
        self.widgets_frame_inferior(frame=self.frame_inferior)

    def widgets_frame_superior(self, frame):
        """Frame Superior - Controles principales"""
        frame.configure(padding=(PADDING_OUTER, PADDING_OUTER))

        # Menu
        self.btn_menu = TTButton(
            frame, text="☰ Menú", command=self.on_toggle_menu, style="info.Outline.TButton"
        )
        self.btn_menu.pack(side=LEFT, padx=5, pady=5)

        # Selección
        self.cbx_operaciones = Combobox(frame, values=self.operaciones, state=READONLY)
        self.cbx_operaciones.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        self.cbx_operaciones.current(0)

        self.btn_seleccionar = TTButton(
            frame,
            text="📁 Seleccionar",
            command=self.on_seleccionar_archivos,
            style="success.Outline.TButton",
        )
        self.btn_seleccionar.pack(side=LEFT, padx=5, pady=5)

        # Separador visual
        sep = Separator(frame, orient='vertical')
        sep.pack(side=LEFT, fill=Y, padx=5)

        self.rbt_copiar = Radiobutton(
            frame, text="📋 Copiar", variable=self.var_opcion_importacion, value="copiar"
        )
        self.rbt_copiar.pack(side=LEFT, padx=5, pady=5)

        self.rbt_mover = Radiobutton(
            frame, text="✂️ Mover", variable=self.var_opcion_importacion, value="mover"
        )
        self.rbt_mover.pack(side=LEFT, padx=5, pady=5)

        self.btn_importar = TTButton(
            frame, text="▶️ Importar", command=self.on_importar_documentos, style="danger.TButton"
        )
        self.btn_importar.pack(side=LEFT, padx=5, pady=5)

    def widgets_frame_central(self, frame):
        """Frame Central - Menu con pestañas y tabla"""
        # Crear PanedWindow para permitir redimensionamiento entre Notebook y TableView
        self.paned_window = PanedWindow(frame, orient="horizontal")
        self.paned_window.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Frame para el Notebook (lado izquierdo)
        self.frame_notebook = TTFrame(
            self.paned_window,
            padding=(PADDING_OUTER, PADDING_OUTER),
            width=220,
        )
        self.paned_window.add(self.frame_notebook, weight=0)
        self.frame_notebook.pack_propagate(False)

        # Frame Menu (dentro del frame del Notebook)
        self.frame_menu = TTFrame(self.frame_notebook, padding=(PADDING_OUTER, PADDING_OUTER))
        self.frame_menu.pack(fill=BOTH, expand=True)

        # Crear el Notebook (pestañas)
        notebook = Notebook(self.frame_menu)
        notebook.pack(fill=BOTH, expand=True, padx=2, pady=2)

        # --- Pestaña "Todos los documentos" ---
        frame_todos = TTFrame(notebook, padding=8)
        notebook.add(frame_todos, text="Todos")

        btn_copiar_todos = TTButton(
            frame_todos,
            text="Copiar todos",
            command=self.on_copiar_todos,
            style="info.TButton",
        )
        btn_copiar_todos.pack(side=TOP, fill=X, padx=3, pady=3)
        ToolTip(btn_copiar_todos, "Copiar todos los archivos de la tabla a una nueva ubicación")

        btn_mover_todos = TTButton(
            frame_todos,
            text="Mover todos",
            command=self.on_mover_todos,
            style="warning.TButton",
        )
        btn_mover_todos.pack(side=TOP, fill=X, padx=3, pady=3)
        ToolTip(btn_mover_todos, "Mover todos los archivos de la tabla a una nueva ubicación")

        btn_mas_todos = Menubutton(frame_todos, text="Más", style="secondary.Outline.TButton")
        btn_mas_todos.pack(side=TOP, fill=X, padx=3, pady=3)
        menu_todos = Menu(btn_mas_todos, tearoff=0)
        menu_todos.add_command(label="Eliminar todos", command=self.on_eliminar_todos)
        menu_todos.add_command(label="Enviar todos a papelera", command=self.on_papelera_todos)
        btn_mas_todos["menu"] = menu_todos

        # --- Pestaña "Existentes en la biblioteca" ---
        frame_existentes = TTFrame(notebook, padding=8)
        notebook.add(frame_existentes, text="Existentes")

        btn_copiar_existentes = TTButton(
            frame_existentes,
            text="Copiar existentes",
            command=self.on_copiar_existentes,
            style="info.TButton",
        )
        btn_copiar_existentes.pack(side=TOP, fill=X, padx=3, pady=3)
        ToolTip(btn_copiar_existentes, "Copiar solo los archivos que ya existen en la biblioteca")

        btn_mover_existentes = TTButton(
            frame_existentes,
            text="Mover existentes",
            command=self.on_mover_existentes,
            style="warning.TButton",
        )
        btn_mover_existentes.pack(side=TOP, fill=X, padx=3, pady=3)
        ToolTip(btn_mover_existentes, "Mover solo los archivos que ya existen en la biblioteca")

        btn_compara_existentes = TTButton(
            frame_existentes,
            text="Comparar existentes",
            command=self.on_comparar_existentes,
            style="light.Outline.TButton",
        )
        btn_compara_existentes.pack(side=TOP, fill=X, padx=3, pady=3)
        ToolTip(btn_compara_existentes, "Comparar archivos existentes por hash y nombre")

        btn_mas_existentes = Menubutton(
            frame_existentes,
            text="Más",
            style="secondary.Outline.TButton",
        )
        btn_mas_existentes.pack(side=TOP, fill=X, padx=3, pady=3)
        menu_existentes = Menu(btn_mas_existentes, tearoff=0)
        menu_existentes.add_command(label="Eliminar existentes", command=self.on_eliminar_existentes)
        menu_existentes.add_command(
            label="Enviar existentes a papelera",
            command=self.on_papelera_existentes,
        )
        btn_mas_existentes["menu"] = menu_existentes

        # --- Pestaña "Tabla" ---
        frame_tabla_ops = TTFrame(notebook, padding=8)
        notebook.add(frame_tabla_ops, text="Tabla")

        btn_eliminar_fila = TTButton(
            frame_tabla_ops,
            text="Quitar seleccionadas",
            command=self.on_eliminar_filas_seleccionadas,
            style="danger.Outline.TButton",
        )
        btn_eliminar_fila.pack(side=TOP, fill=X, padx=3, pady=3)
        ToolTip(btn_eliminar_fila, "Quitar de la tabla las filas seleccionadas")

        btn_eliminar_filas = TTButton(
            frame_tabla_ops,
            text="Limpiar tabla",
            command=lambda: self.table_view.delete_rows(),
            style="secondary.Outline.TButton",
        )
        btn_eliminar_filas.pack(side=TOP, fill=X, padx=3, pady=3)
        ToolTip(btn_eliminar_filas, "Quitar todas las filas de la tabla")

        btn_mas_tabla = Menubutton(frame_tabla_ops, text="Más", style="secondary.Outline.TButton")
        btn_mas_tabla.pack(side=TOP, fill=X, padx=3, pady=3)
        menu_tabla = Menu(btn_mas_tabla, tearoff=0)
        menu_tabla.add_command(
            label="Quitar filas existentes",
            command=self.on_eliminar_filas_existentes,
        )
        btn_mas_tabla["menu"] = menu_tabla

        # Frame Table
        self.frame_table = TTFrame(self.paned_window, padding=(PADDING_OUTER, PADDING_OUTER))
        self.paned_window.add(self.frame_table, weight=1)

        # TableView
        self.table_view = Tableview(
            self.frame_table,
            coldata=self.coldata,
            height=15,
            bootstyle=PRIMARY,
        )
        self.table_view.view.bind('<Double-1>', self.on_doble_click_table_view)
        self.table_view.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=2)
        self._crear_menu_contextual_tabla()

    def widgets_frame_inferior(self, frame):
        """Frame Inferior - Documento seleccionado y controles"""
        frame.configure(padding=(PADDING_OUTER, PADDING_OUTER))

        self.label_frame = LabelFrame(frame, text="Documento seleccionado", padding=(8, 8))
        self.label_frame.pack(side=TOP, fill=X, padx=5, pady=5)

        # Nombre documento
        self.ent_nombre_documento = TTEntry(
            self.label_frame, textvariable=self.var_nombre_documento
        )
        self.ent_nombre_documento.pack(side=TOP, fill=X, padx=5, pady=5)

        # frame buttons
        frame_buttons = TTFrame(self.label_frame, padding=(5, 5))
        frame_buttons.pack(side=TOP, fill=X, padx=5, pady=5)

        frame_buttons.columnconfigure((0, 1, 2, 3), weight=1)

        # Abrir documentos
        self.btn_abrir_documento = TTButton(
            frame_buttons, text="Abrir", command=self.on_abrir_archivo, style="info.TButton"
        )
        self.btn_abrir_documento.grid(row=0, column=0, padx=3, pady=3, sticky=EW)

        self.btn_renombrar_documento = TTButton(
            frame_buttons,
            text="Renombrar",
            command=self.on_renombrar_archivo,
            style="primary.TButton",
        )
        self.btn_renombrar_documento.grid(row=0, column=1, padx=3, pady=3, sticky=EW)

        self.btn_copiar_documento = TTButton(
            frame_buttons,
            text="Copiar",
            command=self.on_copiar_archivo,
            style="info.Outline.TButton",
        )
        self.btn_copiar_documento.grid(row=0, column=2, padx=3, pady=3, sticky=EW)

        # Botones secundarios conservados para compatibilidad (invocados desde menú Más)
        self.btn_mover_documento = TTButton(
            frame_buttons,
            text="Mover",
            command=self.on_mover_archivo,
            style="warning.Outline.TButton",
        )

        self.btn_eliminar_documento = TTButton(
            frame_buttons,
            text="Eliminar",
            command=self.on_eliminar_archivo,
            style="danger.Outline.TButton",
        )

        self.btn_papelera_documento = TTButton(
            frame_buttons,
            text="Papelera",
            command=self.on_papelera_archivo,
            style="secondary.TButton",
        )

        self.btn_convertir_minusculas = TTButton(
            frame_buttons,
            text="Minúsculas",
            command=self.on_convertir_minuscula,
            style="light.TButton",
        )

        self.btn_convertir_mayusculas = TTButton(
            frame_buttons,
            text="MAYÚSCULAS",
            command=self.on_convertir_mayuscula,
            style="light.TButton",
        )

        self.btn_mas_documento = Menubutton(
            frame_buttons,
            text="Más",
            style="secondary.Outline.TButton",
        )
        self.btn_mas_documento.grid(row=0, column=3, padx=3, pady=3, sticky=EW)
        menu_doc = Menu(self.btn_mas_documento, tearoff=0)
        menu_doc.add_command(label="Mover", command=lambda: self.btn_mover_documento.invoke())
        menu_doc.add_command(label="Eliminar", command=lambda: self.btn_eliminar_documento.invoke())
        menu_doc.add_command(label="Enviar a papelera", command=lambda: self.btn_papelera_documento.invoke())
        menu_doc.add_separator()
        menu_doc.add_command(label="Convertir a minúsculas", command=lambda: self.btn_convertir_minusculas.invoke())
        menu_doc.add_command(label="Convertir a MAYÚSCULAS", command=lambda: self.btn_convertir_mayusculas.invoke())
        self.btn_mas_documento["menu"] = menu_doc

        # Label Progreso
        self.lbl_progreso = TTLabel(self.label_frame, padding=(5, 5), text="Progreso: Listo")
        self.lbl_progreso.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)

        # Progress Bar
        self.progress_bar = Progressbar(self.label_frame, maximum=100, length=400)
        self.progress_bar.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_convertir_mayuscula(self):
        original = self.var_nombre_documento.get()
        if original:
            mayuscula = original.upper()
            self.var_nombre_documento.set(mayuscula)

    def on_convertir_minuscula(self):
        original = self.var_nombre_documento.get()
        if original:
            minuscula = original.lower()
            self.var_nombre_documento.set(minuscula)

    def on_renombrar_archivo(self):
        if exists(self.ruta_archivo):
            ruta_origen = self.ruta_archivo
            if self.var_nombre_documento.get():
                ruta_destino = join(self.ruta_padre_archivo, self.var_nombre_documento.get())
                renombrar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)
                self.table_view.view.set(
                    self.item_focus, "#1", f"📗 {self.var_nombre_documento.get()}"
                )
                self.ruta_archivo = ruta_destino

    def on_abrir_archivo(self):
        if exists(self.ruta_archivo):
            abrir_archivo(ruta_origen=self.ruta_archivo)

    def on_copiar_archivo(self):
        directorio = filedialog.askdirectory(
            parent=self.winfo_toplevel(), title="Directorio", initialdir=expanduser('~')
        )
        if directorio:
            ruta_origen = self.ruta_archivo
            ruta_destino = join(directorio, self.var_nombre_documento.get())
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)

    def on_mover_archivo(self):
        directorio = filedialog.askdirectory(
            parent=self.winfo_toplevel(), title="Directorio", initialdir=expanduser('~')
        )
        if directorio:
            ruta_origen = self.ruta_archivo
            ruta_destino = join(directorio, self.var_nombre_documento.get())
            mover_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)
            self.table_view.view.delete(self.item_focus)
            # Re-establecemos los valores
            self.var_nombre_documento.set("")
            self.ruta_archivo = ""
            self.ruta_archivo = ""
            self.item_focus = ""

    def on_eliminar_archivo(self):
        resp = messagebox.askokcancel(
            parent=self.winfo_toplevel(),
            title="Advertencia",
            message="Se eliminará el siguiente archivo. ¿Está seguro?",
        )
        if resp:
            if exists(self.ruta_archivo):
                eliminar_archivo(ruta_destino=self.ruta_archivo)
                self.table_view.view.delete(self.item_focus)
                # Re-establecemos los valores
                self.var_nombre_documento.set("")
                self.ruta_archivo = ""
                self.ruta_archivo = ""
                self.item_focus = ""

    def on_papelera_archivo(self):
        resp = messagebox.askokcancel(
            parent=self.winfo_toplevel(),
            title="Advertencia",
            message="Se moverá a la papelera el siguiente archivo. ¿Está seguro?",
        )
        if resp:
            if exists(self.ruta_archivo):
                papelera_archivo(ruta_origen=self.ruta_archivo)
                self.table_view.view.delete(self.item_focus)
                # Re-establecemos los valores
                self.var_nombre_documento.set("")
                self.ruta_archivo = ""
                self.ruta_archivo = ""
                self.item_focus = ""

    def on_doble_click_table_view(self, event):
        item = self.table_view.view.focus()
        if item:
            self.item_focus = item
            fila = self.table_view.view.item(item, 'values')
            self.ruta_archivo = fila[6]
            archivo = Path(self.ruta_archivo)
            self.var_nombre_documento.set(archivo.name)
            self.ruta_padre_archivo = archivo.parent

    def _crear_menu_contextual_tabla(self):
        acciones = [
            {"label": "👁️ Abrir", "command": self._on_contextual_abrir},
            {"label": "📋 Copiar", "command": self._on_contextual_copiar},
            {"label": "✂️ Mover", "command": self._on_contextual_mover},
            {"separator": True},
            {"label": "🗑️ Eliminar", "command": self._on_contextual_eliminar},
            {"label": "♻️ Papelera", "command": self._on_contextual_papelera},
            {"separator": True},
            {"label": "❌ Quitar fila", "command": self.on_eliminar_filas_seleccionadas},
        ]
        self.menu_contextual_tabla = ContextMenuFactory.build_for_treeview(
            master=self,
            treeview=self.table_view.view,
            actions=acciones,
        )

    def _sincronizar_contexto_fila(self):
        self.on_doble_click_table_view(None)

    def _on_contextual_abrir(self):
        self._sincronizar_contexto_fila()
        self.on_abrir_archivo()

    def _on_contextual_copiar(self):
        self._sincronizar_contexto_fila()
        self.on_copiar_archivo()

    def _on_contextual_mover(self):
        self._sincronizar_contexto_fila()
        self.on_mover_archivo()

    def _on_contextual_eliminar(self):
        self._sincronizar_contexto_fila()
        self.on_eliminar_archivo()

    def _on_contextual_papelera(self):
        self._sincronizar_contexto_fila()
        self.on_papelera_archivo()

    def on_eliminar_filas_seleccionadas(self):
        items = self.table_view.view.selection()
        if items:
            self.table_view.view.delete(*items)

    def on_eliminar_filas_existentes(self):
        items = self.table_view.view.get_children()
        if items:
            for item in items:
                fila = self.table_view.view.item(item, 'values')
                existente = True if fila[4] == "🔴 Ya Existe" else False
                if existente:
                    self.table_view.view.delete(item)

    def on_importar_documentos(self):
        # obtenemos el tipo de importaciones
        tipo_importacion = self.var_opcion_importacion.get()
        controlar_importaciones = ControlarImporetacionDocumento(
            label_progress=self.lbl_progreso,
            progress_bar=self.progress_bar,
            table_view=self.table_view,
            tipo_importacion=tipo_importacion,
        )
        controlar_importaciones.importar()

    def on_papelera_todos(self):
        # mensaje de advertencia al usuario
        res = messagebox.askyesno(
            parent=self.winfo_toplevel(),
            title="Confirmar",
            message="Se enviarán todos los archivos a la papelera. ¿Está seguro?",
        )
        if res:
            controlar_todos = ControlarTodos(
                label_progreso=self.lbl_progreso,
                table_view=self.table_view,
                progress_bar=self.progress_bar,
                ruta_destino="",
            )
            controlar_todos.papelara_todos()

    def on_papelera_existentes(self):
        # mensaje de advertencia al usuario
        res = messagebox.askyesno(
            parent=self.winfo_toplevel(),
            title="Confirmar",
            message="Se enviarán todos los archivos a la papelera. ¿Está seguro?",
        )
        if res:
            controlar_todos = ControlarExistentes(
                label_progreso=self.lbl_progreso,
                table_view=self.table_view,
                progress_bar=self.progress_bar,
                ruta_destino="",
            )
            controlar_todos.papelera_existentes()

    def on_eliminar_todos(self):
        # mensaje de advertencia al usuario
        res = messagebox.askyesno(
            parent=self.winfo_toplevel(),
            title="Confirmar",
            message="Se eliminarán todos los archivos. ¿Está seguro?",
        )
        if res:
            controlar_todos = ControlarTodos(
                label_progreso=self.lbl_progreso,
                table_view=self.table_view,
                progress_bar=self.progress_bar,
                ruta_destino="",
            )
            controlar_todos.eliminar_todos()

    def on_eliminar_existentes(self):
        # mensaje de advertencia al usuario
        res = messagebox.askyesno(
            parent=self.winfo_toplevel(),
            title="Confirmar",
            message="Se eliminarán todos los archivos. ¿Está seguro?",
        )
        if res:
            controlar_todos = ControlarExistentes(
                label_progreso=self.lbl_progreso,
                table_view=self.table_view,
                progress_bar=self.progress_bar,
                ruta_destino="",
            )
            controlar_todos.eliminar_existentes()

    def on_copiar_todos(self):
        # obtenemos la ultima ubicacion de copiado
        configuracion = ConfiguracionController()
        ultima_ruta = configuracion.get_copiar_ubicacion()
        if not ultima_ruta:
            ultima_ruta = expanduser('~')

        # Pedimos al usuario que seleccione una ubicacion para los archivos
        ubicacion_copiar = filedialog.askdirectory(
            parent=self.winfo_toplevel(), title="Copiar todos los archivos", initialdir=ultima_ruta
        )
        # Guardamos la ubicacion
        configuracion.set_copiar_ubicacion(valor=ubicacion_copiar)

        controlar_todos = ControlarTodos(
            label_progreso=self.lbl_progreso,
            table_view=self.table_view,
            progress_bar=self.progress_bar,
            ruta_destino=ubicacion_copiar,
        )
        controlar_todos.copiar_todos()

    def on_copiar_existentes(self):
        # obtenemos la ultima ubicacion de copiado
        configuracion = ConfiguracionController()
        ultima_ruta = configuracion.get_copiar_ubicacion()
        if not ultima_ruta:
            ultima_ruta = expanduser('~')

        # Pedimos al usuario que seleccione una ubicacion para los archivos
        ubicacion_copiar = filedialog.askdirectory(
            parent=self.winfo_toplevel(), title="Copiar todos los archivos", initialdir=ultima_ruta
        )
        # Guardamos la ubicacion
        configuracion.set_copiar_ubicacion(valor=ubicacion_copiar)

        controlar_todos = ControlarExistentes(
            label_progreso=self.lbl_progreso,
            table_view=self.table_view,
            progress_bar=self.progress_bar,
            ruta_destino=ubicacion_copiar,
        )
        controlar_todos.copiar_existentes()

    def on_mover_todos(self):
        # obtenemos la ultima ubicacion de copiado
        configuracion = ConfiguracionController()
        ultima_ruta = configuracion.get_mover_ubicacion()
        if not ultima_ruta:
            ultima_ruta = expanduser('~')

        # Pedimos al usuario que seleccione una ubicacion para los archivos
        ubicacion_mover = filedialog.askdirectory(
            parent=self.winfo_toplevel(), title="Mover todos los archivos", initialdir=ultima_ruta
        )
        # Guardamos la ubicacion
        configuracion.set_mover_ubicacion(valor=ubicacion_mover)

        controlar_todos = ControlarTodos(
            label_progreso=self.lbl_progreso,
            table_view=self.table_view,
            progress_bar=self.progress_bar,
            ruta_destino=ubicacion_mover,
        )
        controlar_todos.mover_todos()

    def on_mover_existentes(self):
        # obtenemos la ultima ubicacion de copiado
        configuracion = ConfiguracionController()
        ultima_ruta = configuracion.get_mover_ubicacion()
        if not ultima_ruta:
            ultima_ruta = expanduser('~')

        # Pedimos al usuario que seleccione una ubicacion para los archivos
        ubicacion_mover = filedialog.askdirectory(
            parent=self.winfo_toplevel(), title="Mover todos los archivos", initialdir=ultima_ruta
        )
        # Guardamos la ubicacion
        configuracion.set_mover_ubicacion(valor=ubicacion_mover)

        controlar_todos = ControlarExistentes(
            label_progreso=self.lbl_progreso,
            table_view=self.table_view,
            progress_bar=self.progress_bar,
            ruta_destino=ubicacion_mover,
        )
        controlar_todos.mover_existentes()

    def on_comparar_existentes(self):
        items = self.table_view.view.get_children()
        if not items:
            messagebox.showinfo(
                parent=self.winfo_toplevel(),
                title="Comparar existentes",
                message="No hay archivos cargados para comparar.",
            )
            return

        filas = [self.table_view.view.item(item, "values") for item in items]
        existentes = [fila for fila in filas if len(fila) > 4 and fila[4] == "🔴 Ya Existe"]
        no_existentes = [fila for fila in filas if len(fila) > 4 and fila[4] == "🟢 No Existe"]

        # Duplicados por hash dentro de la selección
        mapa_hash = {}
        for fila in filas:
            if len(fila) < 7:
                continue
            hash_archivo = fila[5]
            nombre_archivo = Path(fila[6]).name
            mapa_hash.setdefault(hash_archivo, []).append(nombre_archivo)
        duplicados_hash = [nombres for nombres in mapa_hash.values() if len(nombres) > 1]

        # Duplicados por nombre dentro de la selección
        mapa_nombre = {}
        for fila in filas:
            if len(fila) < 7:
                continue
            nombre_archivo = Path(fila[6]).name.lower()
            mapa_nombre.setdefault(nombre_archivo, 0)
            mapa_nombre[nombre_archivo] += 1
        duplicados_nombre = [nombre for nombre, total in mapa_nombre.items() if total > 1]

        total = len(filas)
        mensaje = [
            f"Total analizados: {total}",
            f"Existentes en biblioteca: {len(existentes)}",
            f"No existentes: {len(no_existentes)}",
            f"Duplicados por hash en selección: {len(duplicados_hash)}",
            f"Duplicados por nombre en selección: {len(duplicados_nombre)}",
        ]

        if duplicados_hash:
            ejemplo = ", ".join(duplicados_hash[0][:3])
            mensaje.append(f"Ejemplo hash duplicado: {ejemplo}")
        if duplicados_nombre:
            mensaje.append(f"Ejemplo nombre duplicado: {duplicados_nombre[0]}")

        messagebox.showinfo(
            parent=self.winfo_toplevel(),
            title="Resultado de comparación",
            message="\n".join(mensaje),
        )

    def on_seleccionar_archivos(self):
        # limpiamos la tabla
        self.table_view.delete_rows()

        configuracion = ConfiguracionController()
        dir_init = configuracion.get_ultima_ubicacion()

        if not dir_init:
            dir_init = expanduser('~')

        valor = self.cbx_operaciones.current()

        lista_seleccionados = []

        if valor == 0:
            lista_seleccionados = filedialog.askopenfilenames(
                parent=self.winfo_toplevel(),
                title="Selecciona uno o mas archivos",
                initialdir=dir_init,
                filetypes=self.filetypes_ebooks,
            )
        elif valor == 1:
            lista_seleccionados.clear()
            extension = self._pedir_extension()
            if extension:
                directorio = filedialog.askdirectory(
                    parent=self.winfo_toplevel(),
                    title="Selecciona un direcorio",
                    initialdir=dir_init,
                )
                if directorio:
                    lista_seleccionados = self._filtrar_archivos_simple(
                        directorio=directorio, extension=extension
                    )

        elif valor == 2:
            lista_seleccionados.clear()
            extension = self._pedir_extension()
            if extension:
                directorio = filedialog.askdirectory(
                    parent=self.winfo_toplevel(),
                    title="Selecciona un direcorio",
                    initialdir=dir_init,
                )
                if directorio:
                    lista_seleccionados = self._filtrar_archivos_subdirectorios(
                        directorio=directorio, extension=extension
                    )

        if lista_seleccionados:
            # limpiamos la tabla para la nueve seleccion
            # obtenemos el directorio padre
            dir_parent = Path(lista_seleccionados[0]).parent
            # lo guardamos en la configuracion setting.ini
            configuracion.set_ultima_ubicacion(dir_parent)
            # llamamos a controlar lar seleccion
            controlarSeleccion = ControlarSeleccionDocumentos(
                label_progreso=self.lbl_progreso,
                progress_bar=self.progress_bar,
                table_view=self.table_view,
                lista_archivos=lista_seleccionados,
            )
            controlarSeleccion.cargar_archivos_seleccionados()

    def on_toggle_menu(self):
        if self.ocultar_menu is False:
            self.paned_window.remove(self.frame_notebook)
            self.ocultar_menu = True
        else:
            # Remover y reagregar frame_table para que frame_notebook quede al inicio
            self.paned_window.remove(self.frame_table)
            self.paned_window.add(self.frame_notebook, weight=0)
            self.paned_window.add(self.frame_table, weight=1)
            self.ocultar_menu = False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas
    # └────────────────────────────────────────────────────────────┘

    def _filtrar_archivos_simple(self, directorio: str, extension: str) -> list:
        """Filtra archivos por extensión usando endswith()"""
        import os

        if not extension.startswith('.'):
            extension = '.' + extension

        archivos_filtrados = []
        for archivo in os.listdir(directorio):
            if archivo.endswith(extension):
                archivos_filtrados.append(join(directorio, archivo))

        return sorted(archivos_filtrados)

    def _filtrar_archivos_subdirectorios(self, directorio: str, extension: str) -> list:
        """Filtra archivos por extensión usando endswith() de forma recursiva"""
        import os

        if not extension.startswith('.'):
            extension = '.' + extension

        archivos_filtrados = []

        # Recorrer recursivamente el directorio y sus subdirectorios
        for raiz, carpetas, archivos in os.walk(directorio):
            for archivo in archivos:
                if archivo.endswith(extension):
                    archivos_filtrados.append(join(raiz, archivo))

        return sorted(archivos_filtrados)

    def _pedir_extension(self) -> str:
        """Muestra un diálogo para solicitar una extensión de archivo"""

        class DialogExtension(Toplevel):
            def __init__(self, master, **kwargs):
                super().__init__(master=master, **kwargs)

                self.var_extension = StringVar()
                self.resultado = None

                # Configurar el diálogo
                self.title("Escribe la extensión")
                self.resizable(False, False)
                self.grab_set()  # Hacer modal

                # Crear widgets
                self.crear_widgets()

                # Centrar en la ventana padre
                self.transient(master)
                self.update_idletasks()
                x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
                y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
                self.geometry(f"+{x}+{y}")

            def crear_widgets(self):
                # Frame principal con padding
                frame = Frame(self, padx=20, pady=20)
                frame.pack(fill="both", expand=True)

                # Etiqueta
                label = Label(frame, text="Extensión del archivo (ej: txt, pdf, jpg):")
                label.pack(pady=(0, 10))

                # Entry para la extensión
                entry = Entry(frame, textvariable=self.var_extension, width=30)
                entry.pack(pady=(0, 15))
                entry.focus_set()
                entry.bind("<Return>", lambda e: self.aceptar())

                # Frame para botones
                frame_botones = Frame(frame)
                frame_botones.pack()

                # Botones
                btn_aceptar = Button(frame_botones, text="Aceptar", command=self.aceptar, width=10)
                btn_aceptar.pack(side="left", padx=5)

                btn_cancelar = Button(
                    frame_botones, text="Cancelar", command=self.cancelar, width=10
                )
                btn_cancelar.pack(side="left", padx=5)

            def aceptar(self):
                extension = self.var_extension.get().strip()
                if extension:
                    # Limpiar la extensión (quitar punto si lo tiene)
                    self.resultado = extension.lstrip(".")
                    self.destroy()

            def cancelar(self):
                self.resultado = None
                self.destroy()

        # Crear y mostrar el diálogo
        dialogo = DialogExtension(master=self.winfo_toplevel())
        self.winfo_toplevel().wait_window(dialogo)

        return dialogo.resultado if dialogo.resultado else ""
