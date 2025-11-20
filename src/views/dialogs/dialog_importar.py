from os.path import exists, join
from ttkbootstrap import (
    Toplevel,
    Frame,
    Combobox,
    Button,
    Label,
    Progressbar,
    Button,
    Radiobutton,
    Separator,
    Style,
    LabelFrame,
    Entry,
    StringVar,
)
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from tkinter import filedialog
from tkinter import messagebox
from os.path import expanduser
from pathlib import Path
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


class DialogImportar(Toplevel):
    def __init__(self, title="Importar", **kwargs):
        super().__init__(title, **kwargs)
        # Configuración de la ventana
        self.geometry("900x700+10+10")
        self.resizable(True, True)
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
            ("Documentos PDF", "*.pdf"),  # Muy usado para libros y documentos técnicos
            ("Archivos EPUB", "*.epub"),  # El formato estándar más común
            ("Archivos MOBI/AZW3", "*.mobi *.azw3"),  # Formatos propietarios de Kindle
            ("Todos los archivos", "*.*"),
        )
        self.var_nombre_documento = StringVar()
        self.var_opcion_importacion = StringVar()
        self.var_opcion_importacion.set("copiar")
        # para ocultar el menu
        self.ocultar_menu = False
        # obtenemos la ruta del archivo
        self.ruta_archivo = ""
        # variable para almacenar la ruta padre del archivo
        self.ruta_padre_archivo = ""
        # variable para almacenar el focus
        self.item_focus = ""

        self.estilo = Style()
        self.estilo.configure('Custom.TButton', justify=LEFT, anchor=W, bordercolor="SteelBlue1")

        # creamos los widgets
        self.crear_widgets()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):

        # Frame Superior
        self.frame_superior = Frame(self, padding=(1, 1))
        self.frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)
        self.widgets_frame_superior(frame=self.frame_superior)

        # Frame Central
        self.frame_central = Frame(self, padding=(1, 1))
        self.frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
        self.widgets_frame_central(frame=self.frame_central)

        # Frame Inferior
        self.frame_inferior = Frame(self, padding=(1, 1))
        self.frame_inferior.pack(side=TOP, fill=X, expand=False, padx=1, pady=1)
        self.widgets_frame_inferior(frame=self.frame_inferior)

    def widgets_frame_superior(self, frame: Frame):
        """Frame Superior"""

        # Menu
        self.btn_menu = Button(frame, text="Menu", command=self.on_toggle_menu)
        self.btn_menu.pack(side=LEFT, padx=1, pady=1)

        # Seleccion
        self.cbx_operaciones = Combobox(frame, values=self.operaciones, state=READONLY)
        self.cbx_operaciones.pack(side=LEFT, fill=X, expand=True, padx=1, pady=1)
        self.cbx_operaciones.current(0)

        self.btn_seleccionar = Button(
            frame, text="Seleccionar", command=self.on_seleccionar_archivos
        )
        self.btn_seleccionar.pack(side=LEFT, padx=1, pady=2)

        self.rbt_copiar = Radiobutton(
            frame, text="Copiar", variable=self.var_opcion_importacion, value="copiar"
        )
        self.rbt_copiar.pack(side=LEFT, padx=1, pady=2)

        self.rbt_mover = Radiobutton(
            frame, text="Mover", variable=self.var_opcion_importacion, value="mover"
        )
        self.rbt_mover.pack(side=LEFT, padx=1, pady=2)

        self.btn_importar = Button(frame, text="Importar", command=self.on_importar_documentos)
        self.btn_importar.pack(side=LEFT, padx=1, pady=2)

    def widgets_frame_central(self, frame: Frame):
        """Frame Central"""

        # Frame Menu
        self.frame_menu = Frame(frame, padding=(1, 1), width=200)
        self.frame_menu.pack(side=LEFT, fill=Y, padx=1, pady=1)
        self.frame_menu.pack_propagate(False)

        # Todos
        self.lbl_todos = Label(
            self.frame_menu,
            text="Todos los documentos",
            font=("Arial", 10),
            foreground="gray",
        )
        self.lbl_todos.pack(side=TOP, fill=X, padx=2, pady=2)

        # Seprador
        self.spt_todos = Separator(self.frame_menu, orient=HORIZONTAL)
        self.spt_todos.pack(side=TOP, fill=X, padx=2, pady=2)

        # Copiar todos
        self.btn_copiar_todos = Button(
            self.frame_menu, text="Copiar todos", command=self.on_copiar_todos
        )
        self.btn_copiar_todos.config(style="Custom.TButton")
        self.btn_copiar_todos.pack(side=TOP, fill=X, padx=1, pady=1)

        # Mover todos
        self.btn_mover_todos = Button(
            self.frame_menu, text="Mover todos", command=self.on_mover_todos
        )
        self.btn_mover_todos.config(style="Custom.TButton")
        self.btn_mover_todos.pack(side=TOP, fill=X, padx=1, pady=1)

        # Eliminar todos
        self.btn_eliminar_todos = Button(
            self.frame_menu, text="Eliminar todos", command=self.on_eliminar_todos
        )
        self.btn_eliminar_todos.config(style="Custom.TButton")
        self.btn_eliminar_todos.pack(side=TOP, fill=X, padx=1, pady=1)

        # Papalera todos
        self.btn_papelera_todos = Button(
            self.frame_menu, text="Papelera todos", command=self.on_papelera_todos
        )
        self.btn_papelera_todos.config(style="Custom.TButton")
        self.btn_papelera_todos.pack(side=TOP, fill=X, padx=1, pady=1)

        # Existe
        self.lbl_existe = Label(
            self.frame_menu,
            text="Existentes en la biblioteca",
            font=("Arial", 10),
            foreground="gray",
        )
        self.lbl_existe.pack(side=TOP, fill=X, padx=2, pady=2)

        # Seprador
        self.spt_existe = Separator(self.frame_menu, orient=HORIZONTAL)
        self.spt_existe.pack(side=TOP, fill=X, padx=2, pady=2)

        # Copiar Existentes
        self.btn_copiar_existentes = Button(
            self.frame_menu, text="Copiar existentes", command=self.on_copiar_existentes
        )
        self.btn_copiar_existentes.config(style="Custom.TButton")
        self.btn_copiar_existentes.pack(side=TOP, fill=X, padx=1, pady=1)

        # Mover Existentes
        self.btn_mover_existentes = Button(
            self.frame_menu, text="Mover existentes", command=self.on_mover_existentes
        )
        self.btn_mover_existentes.config(style="Custom.TButton")
        self.btn_mover_existentes.pack(side=TOP, fill=X, padx=1, pady=1)

        # Eliminar Existentes
        self.btn_eliminar_existentes = Button(
            self.frame_menu, text="Eliminar existentes", command=self.on_eliminar_existentes
        )
        self.btn_eliminar_existentes.config(style="Custom.TButton")
        self.btn_eliminar_existentes.pack(side=TOP, fill=X, padx=1, pady=1)

        # Papelera Existentes
        self.btn_papelera_existentes = Button(
            self.frame_menu, text="Papelera existentes", command=self.on_papelera_existentes
        )
        self.btn_papelera_existentes.config(style="Custom.TButton")
        self.btn_papelera_existentes.pack(side=TOP, fill=X, padx=1, pady=1)

        # Comparar Existente
        self.btn_compara_existentes = Button(
            self.frame_menu, text="Comparar existentes", command=self.on_eliminar_existentes
        )
        self.btn_compara_existentes.config(style="Custom.TButton")
        self.btn_compara_existentes.pack(side=TOP, fill=X, padx=1, pady=1)

        # Label Table
        self.lbl_tabla = Label(
            self.frame_menu,
            text="Tabla",
            font=("Arial", 10),
            foreground="gray",
        )
        self.lbl_tabla.pack(side=TOP, fill=X, padx=2, pady=2)

        # Seprador
        self.spt_table = Separator(self.frame_menu, orient=HORIZONTAL)
        self.spt_table.pack(side=TOP, fill=X, padx=2, pady=2)

        # Eliminar fila seleccionada
        self.btn_eliminar_fila = Button(
            self.frame_menu,
            text="Eliminar filas seleccionada",
            command=self.on_eliminar_filas_seleccionadas,
        )
        self.btn_eliminar_fila.config(style="Custom.TButton")
        self.btn_eliminar_fila.pack(side=TOP, fill=X, padx=1, pady=1)

        # Eliminar todas las filas
        self.btn_eliminar_filas_existentes = Button(
            self.frame_menu,
            text="Eliminar filas existentes",
            command=self.on_eliminar_filas_existentes,
        )
        self.btn_eliminar_filas_existentes.config(style="Custom.TButton")
        self.btn_eliminar_filas_existentes.pack(side=TOP, fill=X, padx=1, pady=1)

        # Eliminar todas las filas
        self.btn_eliminar_filas = Button(
            self.frame_menu,
            text="Eliminar todas las filas",
            command=lambda: self.table_view.delete_rows(),
        )
        self.btn_eliminar_filas.config(style="Custom.TButton")
        self.btn_eliminar_filas.pack(side=TOP, fill=X, padx=1, pady=1)

        # Frame Table
        self.frame_table = Frame(frame, padding=(1, 1))
        self.frame_table.pack(side="left", fill=BOTH, expand=True, padx=1, pady=1)

        # TableView
        self.table_view = Tableview(self.frame_table, coldata=self.coldata)
        self.table_view.view.bind('<Double-1>', self.on_doble_click_table_view)
        self.table_view.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)

    def widgets_frame_inferior(self, frame: Frame):
        self.label_frame = LabelFrame(frame, text="Documento seleccionado", padding=(2, 2))
        self.label_frame.pack(side=TOP, fill=X, padx=1, pady=1)

        # Nombre documento
        self.ent_nombre_documento = Entry(self.label_frame, textvariable=self.var_nombre_documento)
        self.ent_nombre_documento.pack(side=TOP, fill=X, padx=1, pady=1)

        # frame buttons
        frame_buttons = Frame(self.label_frame, padding=(1, 1))
        frame_buttons.pack(side=TOP, fill=X, padx=1, pady=1)

        # Abrir documentos
        self.btn_abrir_documento = Button(
            frame_buttons, text="Abrir", command=self.on_abrir_archivo
        )
        self.btn_abrir_documento.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        self.btn_renombrar_documento = Button(
            frame_buttons, text="Renombrar", command=self.on_renombrar_archivo
        )
        self.btn_renombrar_documento.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        self.btn_copiar_documento = Button(
            frame_buttons, text="Copiar", command=self.on_copiar_archivo
        )
        self.btn_copiar_documento.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        self.btn_mover_documento = Button(
            frame_buttons, text="Mover", command=self.on_mover_archivo
        )
        self.btn_mover_documento.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        self.btn_eliminar_documento = Button(
            frame_buttons, text="Eliminar", command=self.on_eliminar_archivo
        )
        self.btn_eliminar_documento.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        self.btn_papelera_documento = Button(
            frame_buttons, text="Papelera", command=self.on_papelera_archivo
        )
        self.btn_papelera_documento.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        self.btn_convertir_minusculas = Button(
            frame_buttons, text="Minusculas", command=self.on_convertir_minuscula
        )
        self.btn_convertir_minusculas.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        self.btn_convertir_mayusculas = Button(
            frame_buttons, text="Mayusculas", command=self.on_convertir_mayuscula
        )
        self.btn_convertir_mayusculas.pack(side=LEFT, fill=X, expand=TRUE, padx=0, pady=0)

        # Label Progreso
        self.lbl_progreso = Label(self.label_frame, padding=(1, 1), text="Progreso")
        self.lbl_progreso.pack(side=TOP, fill=X, expand=True, padx=1, pady=1)

        # Progress Bar
        self.progress_bar = Progressbar(self.label_frame, maximum=100)
        self.progress_bar.pack(side=TOP, fill=X, expand=True, padx=1, pady=1)

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

    def on_abrir_archivo(self):
        if exists(self.ruta_archivo):
            abrir_archivo(ruta_origen=self.ruta_archivo)

    def on_copiar_archivo(self):
        directorio = filedialog.askdirectory(
            parent=self, title="Directorio", initialdir=expanduser('~')
        )
        if directorio:
            ruta_origen = self.ruta_archivo
            ruta_destino = join(directorio, self.var_nombre_documento.get())
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)

    def on_mover_archivo(self):
        directorio = filedialog.askdirectory(
            parent=self, title="Directorio", initialdir=expanduser('~')
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
            parent=self,
            title="Advertencia",
            message="Se eliminara el siguiente archivo. ¿Esta seguro?",
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
            parent=self,
            title="Advertencia",
            message="Se movera a la papelera el siguiente archivo. ¿Esta seguro?",
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
        # obtenmos el tipo de importaciones
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
            parent=self,
            title="Confirmar",
            message="Se enviar todos los archivos a la papelera. ¿Está seguro?",
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
            parent=self,
            title="Confirmar",
            message="Se enviar todos los archivos a la papelera. ¿Está seguro?",
        )
        if res:
            controlar_todos = ControlarExistentes(
                label_progreso=self.lbl_progreso,
                table_view=self.table_view,
                progress_bar=self.progress_bar,
                ruta_destino="",
            )
        controlar_todos.papelara_existentes()

    def on_eliminar_todos(self):
        # mensaje de advertencia al usuario
        res = messagebox.askyesno(
            parent=self,
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
            parent=self,
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
            parent=self, title="Copiar todos los archivos", initialdir=ultima_ruta
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
            parent=self, title="Copiar todos los archivos", initialdir=ultima_ruta
        )
        # Guardamos la ubicacion
        configuracion.set_copiar_ubicacion(valor=ubicacion_copiar)

        controlar_todos = ControlarExistentes(
            label_progreso=self.lbl_progreso,
            table_view=self.table_view,
            progress_bar=self.progress_bar,
            ruta_destino=ubicacion_copiar,
        )
        controlar_todos.copiar_existes()

    def on_mover_todos(self):
        # obtenemos la ultima ubicacion de copiado
        configuracion = ConfiguracionController()
        ultima_ruta = configuracion.get_mover_ubicacion()
        if not ultima_ruta:
            ultima_ruta = expanduser('~')

        # Pedimos al usuario que seleccione una ubicacion para los archivos
        ubicacion_mover = filedialog.askdirectory(
            parent=self, title="Mover todos los archivos", initialdir=ultima_ruta
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
            parent=self, title="Mover todos los archivos", initialdir=ultima_ruta
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
                parent=self,
                title="Selecciona uno o mas archivos",
                initialdir=dir_init,
                filetypes=self.filetypes_ebooks,
            )
        elif valor == 1:
            lista_seleccionados.clear()
            extension = self._pedir_extension()
            if extension:
                directorio = filedialog.askdirectory(
                    parent=self, title="Selecciona un direcorio", initialdir=dir_init
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
                    parent=self, title="Selecciona un direcorio", initialdir=dir_init
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
            self.frame_menu.pack_forget()
            self.ocultar_menu = True
        else:
            self.frame_menu.pack(side=LEFT, fill=Y, padx=1, pady=1, before=self.frame_table)
            self.ocultar_menu = False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas
    # └────────────────────────────────────────────────────────────┘

    def _filtrar_archivos_simple(self, directorio: str, extension: str) -> list:
        """
        Filtra archivos por extensión usando endswith()
        """
        import os
        from os.path import join

        if not extension.startswith('.'):
            extension = '.' + extension

        archivos_filtrados = []
        for archivo in os.listdir(directorio):
            if archivo.endswith(extension):
                archivos_filtrados.append(join(directorio, archivo))

        return sorted(archivos_filtrados)

    def _filtrar_archivos_subdirectorios(self, directorio: str, extension: str) -> list:
        """
        Filtra archivos por extensión usando endswith() de forma recursiva
        """
        import os
        from os.path import join

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
        from tkinter import Toplevel, Label, Entry, Button, StringVar, Frame

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
        dialogo = DialogExtension(master=self)
        self.wait_window(dialogo)  # Esperar a que se cierre el diálogo

        return dialogo.resultado if dialogo.resultado else ""
