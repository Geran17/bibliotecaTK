from os.path import expanduser
from ttkbootstrap import (
    Frame,
    Button,
    Entry,
    Label,
    StringVar,
    Combobox,
    Separator,
    LabelFrame,
    IntVar,
    Progressbar,
)
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *
from tkinter.messagebox import showinfo, askokcancel
from tkinter.filedialog import askdirectory
from models.controllers.configuracion_controller import ConfiguracionController
from models.controllers.controlar_administrar_documentos import ControlarAdministrarDocumentos
from models.controllers.controlar_operaciones_documentos import ControlarOperacionesDocumentos
from models.controllers.controlar_documento_seleccionado import ControlarDocumentoSeleccionado
from views.dialogs.dialog_seleccionar_colecciones import DialogSeleccionarColecciones
from views.dialogs.dialog_seleccionar_grupos import DialogSeleccionarGrupos
from views.dialogs.dialog_seleccionar_categorias import DialogSeleccionarCategorias
from views.dialogs.dialog_seleccionar_etiquetas import DialogSeleccionarEtiquetas
from views.dialogs.dialog_seleccionar_palabras_clave import DialogSeleccionarPalabrasClave
from views.dialogs.dialog_adminstrar_bibliografia import DialogAdministrarBibliografia
from views.dialogs.dialog_administrar_contenido import DialogAdministrarContenido
from typing import Dict, Any


class AdministrarDocumentos(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Variables Globales
        # ---------------------------
        # icons
        self.icon_favorito = "⭐"
        self.icon_grupo = "🗂️"
        self.icon_coleccion = "📚"
        self.icon_categoria = "🗃️"
        self.icon_etiqueta = "🏷️"
        self.icon_palabra_clave = "🔑"
        self.icon_libro = "📕"
        self.icon_bibliografia = "🧬"
        self.icon_exclamacion = "❗"  # este icono servira para indicar, que existe un registro en la bd, pero no existe el archivo
        # variables
        self.var_buscar = StringVar()
        self.campos = ["Nombre", "Extension", "Hash"]
        self.var_nombre = StringVar()
        self.var_id = IntVar()
        # variables de visualizacion
        self.mostrar_asociaciones = False
        self.mostrar_datos_bibliograficos = False
        self.mostrar_operaciones = False
        self.mostrar_menu = False
        self.coldata = [
            {"text": "Id", "stretch": False, "width": 50},  # 0
            {"text": "Info.", "stretch": False, "width": 50},  # 1
            {"text": "", "stretch": False, "width": 50},  # 2
            {"text": "Nombre", "stretch": False},  # 3
            {"text": "Extension", "stretch": False, "width": 80},  # 4
            {"text": "Tamaño", "stretch": False, "width": 80},  # 5
            {"text": "Activo", "stretch": False, "width": 50},  # 6
            {"text": "Creado", "stretch": False},  # 7
            {"text": "Actualizado", "stretch": False},  # 8
            {"text": "Hash", "stretch": True},  # 9 Ocultar columna
        ]
        # cargamos los widgets
        self.crear_widgets()

        # cargamos los paneles
        self._cargar_paneles()

        # Map Vars
        self.map_vars: Dict[str, Any] = {
            "id_documento": self.var_id,
            "nombre_documento": self.var_nombre,
        }

        # Map Widgets
        self.map_widgets: Dict[str, Any] = {
            "btn_abrir": self.btn_abrir,
            "btn_abrir_carpeta": self.btn_abrir_carpeta,
            "btn_renombrar": self.btn_renombrar,
            "btn_copiar": self.btn_copiar,
            "btn_mover": self.btn_mover,
            "btn_eliminar": self.btn_eliminar,
            "btn_papelera": self.btn_papelera,
            "btn_propiedades": self.btn_propiedades,
            "btn_metadatos": self.btn_metadatos,
            "btn_renombrar_bibliografico": self.btn_renombrar_bibliografico,
        }

        # Instaciamos el documento seleccionado en el TableView
        ControlarDocumentoSeleccionado(
            table_view=self.table_view,
            map_vars=self.map_vars,
            map_widgets=self.map_widgets,
            master=self,
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):

        # Panel Superior
        frame_superior = Frame(self, padding=(1, 1))
        frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)
        self.panel_superior(frame=frame_superior)

        # Panel Central
        frame_central = Frame(self, padding=(1, 1))
        frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
        self.panel_central(frame=frame_central)

        # Panel Inferior
        frame_inferior = Frame(self, padding=(1, 1))
        frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)
        self.panel_inferior(frame=frame_inferior)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Superior
    # └────────────────────────────────────────────────────────────┘

    def panel_superior(self, frame: Frame):
        """Este panel sera para navegar y buscar en la base de datos los diferentes libros"""

        lbl_titulo = Label(frame, text="📂 Administrar Documentos", font=("Helvetica", 14, "bold"))
        lbl_titulo.pack(side=TOP, fill=X, padx=10, pady=(5, 10))

        # Button Menu
        btn_menu = Button(frame, text="☰", command=self.on_mostrar_menu, style="primary.Toolbutton")
        btn_menu.pack(side=LEFT, padx=(5, 2), pady=5)
        ToolTip(btn_menu, "Mostrar/Ocultar panel de acciones")

        # Entry Buscar
        ent_buscar = Entry(frame, textvariable=self.var_buscar)
        ent_buscar.bind('<Return>', self._filtrar_documentos)
        ent_buscar.pack(side=LEFT, fill=X, expand=True, padx=2, pady=5)
        ToolTip(ent_buscar, "Escribe aquí para buscar y presiona Enter")

        # Combobox Campos
        self.cbx_campos = Combobox(frame, values=self.campos, state=READONLY)
        self.cbx_campos.current(0)
        self.cbx_campos.pack(side=LEFT, fill=X, padx=2, pady=5)

        # Button Filtrar
        btn_filtrar = Button(frame, text="Filtrar", command=self._filtrar_documentos)
        btn_filtrar.pack(side=LEFT, fill=X, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Central
    # └────────────────────────────────────────────────────────────┘

    def panel_central(self, frame: Frame):
        # Frame Izquierdo
        self.frame_izquierdo = Frame(frame, padding=(1, 1), width=250)
        self.frame_izquierdo.pack(side=LEFT, fill=Y, padx=1, pady=1)
        self.panel_izquierdo(frame=self.frame_izquierdo)

        # Frame Derecho
        self.frame_derecho = Frame(frame, padding=(1, 1))
        self.frame_derecho.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=1)
        self.panel_derecho(frame=self.frame_derecho)

    def panel_izquierdo(self, frame: Frame):
        """Para mostrar el menu de asociasiones de los archivos"""

        # ┌────────────────────────────────────────────────────────────┐
        # │ Asociaciones en los libros
        # └────────────────────────────────────────────────────────────┘

        lbl_asociar = Label(frame, text="Asociar documentos a: ", bootstyle="secondary")
        lbl_asociar.bind("<Double-Button-1>", self.on_mostrar_asociaciones)
        lbl_asociar.pack(side=TOP, fill=X, padx=2, pady=2)

        self.separador1 = Separator(frame, orient=HORIZONTAL)
        self.separador1.pack(side=TOP, fill=X, padx=2, pady=2, ipady=2)

        self.frame_asociar = Frame(frame, padding=(1, 1))
        self.frame_asociar.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_coleccion = Button(
            self.frame_asociar,
            text=f"{self.icon_coleccion} Coleccion",
            style='Link.TButton',
            command=self.on_coleccion,
        )
        btn_coleccion.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_coleccion, "Asociar documentos a colecciones")

        btn_categoria = Button(
            self.frame_asociar,
            text=f"{self.icon_categoria} Categoria",
            style='Link.TButton',
            command=self.on_categoria,
        )
        btn_categoria.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_categoria, "Asociar documentos a categorías")

        btn_grupo = Button(
            self.frame_asociar,
            text=f"{self.icon_grupo} Grupo",
            style='Link.TButton',
            command=self.on_grupo,
        )
        btn_grupo.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_grupo, "Asociar documentos a grupos")

        btn_etiqueta = Button(
            self.frame_asociar,
            text=f"{self.icon_etiqueta} Etiqueta",
            style='Link.TButton',
            command=self.on_etiqueta,
        )
        btn_etiqueta.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_etiqueta, "Asociar documentos a etiquetas")

        btn_palabra_clave = Button(
            self.frame_asociar,
            text=f"{self.icon_palabra_clave} Palabra Clave",
            style='Link.TButton',
            command=self.on_palabra_clave,
        )
        btn_palabra_clave.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_palabra_clave, "Asociar documentos a palabras clave")

        btn_favorito = Button(
            self.frame_asociar,
            text=f"{self.icon_favorito} Favorito",
            style='Link.TButton',
            command=self.on_favoritos,
        )
        btn_favorito.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_favorito, "Marcar/Desmarcar documentos como favoritos")

        # ┌────────────────────────────────────────────────────────────┐
        # │ Datos Bibliograficos
        # └────────────────────────────────────────────────────────────┘
        lbl_datos_bibliograficos = Label(frame, text="Datos del Libro: ", bootstyle="secondary")
        lbl_datos_bibliograficos.bind("<Double-Button-1>", self.on_mostrar_datos_bibliograficos)
        lbl_datos_bibliograficos.pack(side=TOP, fill=X, padx=2, pady=2)

        self.separador2 = Separator(frame, orient=HORIZONTAL)
        self.separador2.pack(side=TOP, fill=X, padx=2, pady=2, ipady=2)

        self.frame_datos_bibliograficos = Frame(frame, padding=(1, 1))
        self.frame_datos_bibliograficos.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_bibliografia = Button(
            self.frame_datos_bibliograficos,
            text=f"{self.icon_bibliografia} Bibliografia",
            style='Link.TButton',
            command=self.on_bibliografia,
        )
        btn_bibliografia.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_bibliografia, "Administrar la información bibliográfica")

        btn_contenido = Button(
            self.frame_datos_bibliograficos,
            text="📑 Contenido",
            style='Link.TButton',
            command=self.on_contenido,
        )
        btn_contenido.pack(side=TOP, fill=X, padx=1, pady=1)
        ToolTip(btn_contenido, "Administrar capítulos y secciones (no implementado)")

        # ┌────────────────────────────────────────────────────────────┐
        # │ Operaciones de los seleccionados
        # └────────────────────────────────────────────────────────────┘

        lbl_operaciones = Label(
            frame, text="Opereciones en los seleccionados: ", bootstyle="secondary"
        )
        lbl_operaciones.bind("<Double-Button-1>", self.on_mostrar_operaciones)
        lbl_operaciones.pack(side=TOP, fill=X, padx=2, pady=2)

        self.separador3 = Separator(frame, orient=HORIZONTAL)
        self.separador3.pack(side=TOP, fill=X, padx=2, pady=2, ipady=2)

        self.frame_operaciones = Frame(frame, padding=(1, 1))
        self.frame_operaciones.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_copiar = Button(
            self.frame_operaciones,
            text="Copiar",
            style='Link.TButton',
            command=self.on_copiar_seleccionados,
        )
        btn_copiar.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_mover = Button(
            self.frame_operaciones,
            text="Mover",
            style='Link.TButton',
            command=self.on_mover_seleccionados,
        )
        btn_mover.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_eliminar = Button(
            self.frame_operaciones,
            text="Eliminar",
            style='Link.TButton',
            command=self.on_eliminar_seleccionado,
        )
        btn_eliminar.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_eliminar_filas = Button(
            self.frame_operaciones,
            text="Eliminar filas",
            style='Link.TButton',
            command=self.on_eliminar_filas_seleccionadas,
        )
        btn_eliminar_filas.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_eliminar_registro = Button(
            self.frame_operaciones,
            text="Eliminar registro",
            style='Link.TButton',
            command=self.on_eliminar_registros,
        )
        btn_eliminar_registro.pack(side=TOP, fill=X, padx=1, pady=1)

        btn_limpiar = Button(self.frame_operaciones, text="Limpiar", style='Link.TButton')
        btn_limpiar.pack(side=TOP, fill=X, padx=1, pady=1)

    def panel_derecho(self, frame: Frame):
        """para mostrar la tabla de busqueda"""
        self.table_view = Tableview(frame, bootstyle="primary", coldata=self.coldata)
        self.table_view.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Inferior
    # └────────────────────────────────────────────────────────────┘

    def panel_inferior(self, frame: Frame):
        """Para trabajar con el archivo seleccionado en la tabla"""
        label_frame_seleccionado = LabelFrame(frame, text="Documento Seleccionado", padding=5)
        label_frame_seleccionado.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)

        # Frame id, nombre
        frame_nombre = Frame(label_frame_seleccionado, padding=(1, 1))
        frame_nombre.pack(side=TOP, fill=X, padx=1, pady=1)

        ent_id = Entry(
            frame_nombre, state=READONLY, justify=CENTER, width=10, textvariable=self.var_id
        )
        ent_id.pack(side=LEFT, fill=X, padx=1, pady=1)

        ent_nombre = Entry(frame_nombre, textvariable=self.var_nombre)
        ent_nombre.pack(side=LEFT, fill=X, expand=True, padx=1, pady=1)

        frame_buttons = Frame(label_frame_seleccionado, padding=(1, 1))
        frame_buttons.pack(side=TOP, fill=X, padx=1, pady=2)
        frame_buttons.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.btn_abrir = Button(frame_buttons, text="Abrir")
        self.btn_abrir.grid(row=0, column=0, sticky=EW, padx=2, pady=2)

        self.btn_abrir_carpeta = Button(frame_buttons, text="Abrir Carpeta")
        self.btn_abrir_carpeta.grid(row=0, column=1, sticky=EW, padx=2, pady=2)

        self.btn_renombrar = Button(frame_buttons, text="Renombar")
        self.btn_renombrar.grid(row=0, column=2, sticky=EW, padx=2, pady=2)

        self.btn_copiar = Button(frame_buttons, text="Copiar")
        self.btn_copiar.grid(row=0, column=3, sticky=EW, padx=2, pady=2)

        self.btn_mover = Button(frame_buttons, text="Mover")
        self.btn_mover.grid(row=0, column=4, sticky=EW, padx=2, pady=2)

        self.btn_eliminar = Button(frame_buttons, text="Eliminar")
        self.btn_eliminar.grid(row=1, column=0, sticky=EW, padx=2, pady=2)

        self.btn_papelera = Button(frame_buttons, text="Papelera")
        self.btn_papelera.grid(row=1, column=1, sticky=EW, padx=2, pady=2)

        self.btn_propiedades = Button(frame_buttons, text="Propiedades")
        self.btn_propiedades.grid(row=1, column=2, sticky=EW, padx=2, pady=2)

        self.btn_metadatos = Button(frame_buttons, text="Metadatos")
        self.btn_metadatos.grid(row=1, column=3, sticky=EW, padx=2, pady=2)

        self.btn_renombrar_bibliografico = Button(
            frame_buttons, text="Renombrar Bibliográficamente"
        )
        self.btn_renombrar_bibliografico.grid(row=1, column=4, sticky=EW, padx=2, pady=2)

        frame_pregreso = Frame(frame, padding=(1, 1))
        frame_pregreso.pack(side=TOP, fill=X, padx=1, pady=1)

        self.lbl_progreso = Label(frame_pregreso, text="")
        self.lbl_progreso.pack(side=TOP, fill=X, padx=1, pady=1, expand=True)

        self.progress_bar = Progressbar(frame_pregreso, maximum=100, bootstyle="primary")
        self.progress_bar.pack(side=TOP, fill=X, padx=1, pady=1, expand=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Funciones Privadas
    # └────────────────────────────────────────────────────────────┘

    def _cargar_paneles(self):
        conf = ConfiguracionController()
        # obtenemos los valores
        panel_asociaciones = conf.get_mostrar_asociaciones()
        panel_datos_bibliograficos = conf.get_mostrar_datos_bibliograficos()
        panel_operaciones = conf.get_mostrar_operaciones()
        # Mostramos o ocultamos
        if panel_asociaciones:
            if int(panel_asociaciones) == 0:
                self.frame_asociar.pack_forget()

        if panel_datos_bibliograficos:
            if int(panel_datos_bibliograficos) == 0:
                self.frame_datos_bibliograficos.pack_forget()

        if panel_operaciones:
            if int(panel_operaciones) == 0:
                self.frame_operaciones.pack_forget()

    def _abrir_dialogo_seleccion(self, dialog_class):
        controlar = ControlarAdministrarDocumentos(
            progress_bar=self.progress_bar,
            lbl_progreso=self.lbl_progreso,
            table_view=self.table_view,
        )
        documentos_seleccionados = controlar.get_documentos_seleccionados()

        if not documentos_seleccionados:
            showinfo(title="Error", message="No hay documentos seleccionados")
            return

        # abrimos el Dialog
        dialog = dialog_class()
        dialog.obtener_documentos_seleccionados(documentos_seleccionados)
        dialog.grab_set()

    def _administrar_favoritos(self):
        controlar = ControlarAdministrarDocumentos(
            progress_bar=self.progress_bar,
            lbl_progreso=self.lbl_progreso,
            table_view=self.table_view,
        )
        documentos_seleccionados = controlar.get_documentos_seleccionados()

        if not documentos_seleccionados:
            showinfo(title="Error", message="No hay documentos seleccionados")
            return

        controlar.controlar_favoritos()
        showinfo(title="Favoritos", message="Lista de favoritos actualizados")

    def _filtrar_documentos(self, event=None):
        controlar = ControlarAdministrarDocumentos(
            progress_bar=self.progress_bar,
            lbl_progreso=self.lbl_progreso,
            table_view=self.table_view,
        )
        campo = self.cbx_campos.get()
        buscar = self.var_buscar.get()

        if not campo or not buscar:
            return

        controlar.buscar_datos(campo=campo, buscar=buscar)
        controlar.ejecutar_encontrados()

    def _copiar_seleccionados(self):
        # abrimos el archivo de configuraciones
        conf = ConfiguracionController()
        # obtenmos la ultima ubicacion de copiado
        last_copy = conf.get_copiar_ubicacion()
        if not last_copy:
            last_copy = expanduser("~")
        path_copy = askdirectory(initialdir=last_copy, title="Seleccione la ubicacion", parent=self)

        if not path_copy:
            showinfo(title="Cancelado", message="Operacion cancelada por el usuario", parent=self)
            return

        operaciones = ControlarOperacionesDocumentos(
            master=self,
            table_view=self.table_view,
            lbl_progreso=self.lbl_progreso,
            progress_bar=self.progress_bar,
        )
        operaciones.set_path_copy(path_copy=path_copy)
        operaciones.ejecutar_copia_seleccionados()

        conf.set_copiar_ubicacion(valor=path_copy)

    def _mover_seleccionados(self):
        # abrimos el archivo de configuraciones
        conf = ConfiguracionController()
        # obtenmos la ultima ubicacion de copiado
        last_move = conf.get_mover_ubicacion()
        if not last_move:
            last_move = expanduser("~")
        path_move = askdirectory(initialdir=last_move, title="Seleccione la ubicacion", parent=self)

        if not path_move:
            showinfo(title="Cancelado", message="Operacion cancelada por el usuario", parent=self)
            return

        operaciones = ControlarOperacionesDocumentos(
            master=self,
            table_view=self.table_view,
            lbl_progreso=self.lbl_progreso,
            progress_bar=self.progress_bar,
        )
        operaciones.set_path_move(path_move=path_move)
        operaciones.ejecutar_mover_seleccionados()

        # cargamos en la configuracion la ubicacion seleccioda por el usuario
        conf.set_mover_ubicacion(valor=path_move)

    def _eliminar_seleccionados(self):
        resp = askokcancel(
            title="Advertencia",
            message="Esto eliminara los archivos y los registro de los documentos en la BD",
            icon="warning",
        )
        if resp:
            operaciones = ControlarOperacionesDocumentos(
                master=self,
                table_view=self.table_view,
                lbl_progreso=self.lbl_progreso,
                progress_bar=self.progress_bar,
            )
            operaciones.ejecutar_eliminar_seleccionados()

    def _eliminar_registros(self):
        resp = askokcancel(
            title="Advertencia",
            message="Esto eliminara los registro de los documentos en la BD",
            icon="warning",
        )
        if resp:
            operaciones = ControlarOperacionesDocumentos(
                master=self,
                table_view=self.table_view,
                lbl_progreso=self.lbl_progreso,
                progress_bar=self.progress_bar,
            )
            operaciones.ejecutar_eliminar_registros()

    def _eliminar_filas_seleccionadas(self):
        operaciones = ControlarOperacionesDocumentos(
            master=self,
            table_view=self.table_view,
            lbl_progreso=self.lbl_progreso,
            progress_bar=self.progress_bar,
        )
        operaciones.ejecutar_eliminar_filas_seleccionados()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_eliminar_registros(self):
        self._eliminar_registros()

    def on_eliminar_filas_seleccionadas(self):
        self._eliminar_filas_seleccionadas()

    def on_eliminar_seleccionado(self):
        self._eliminar_seleccionados()

    def on_mover_seleccionados(self):
        self._mover_seleccionados()

    def on_copiar_seleccionados(self):
        self._copiar_seleccionados()

    def on_favoritos(self):
        self._administrar_favoritos()

    def on_coleccion(self):
        self._abrir_dialogo_seleccion(DialogSeleccionarColecciones)

    def on_grupo(self):
        self._abrir_dialogo_seleccion(DialogSeleccionarGrupos)

    def on_categoria(self):
        self._abrir_dialogo_seleccion(DialogSeleccionarCategorias)

    def on_etiqueta(self):
        self._abrir_dialogo_seleccion(DialogSeleccionarEtiquetas)

    def on_palabra_clave(self):
        self._abrir_dialogo_seleccion(DialogSeleccionarPalabrasClave)

    def on_bibliografia(self):
        self._abrir_dialogo_seleccion(DialogAdministrarBibliografia)

    def on_contenido(self):
        self._abrir_dialogo_seleccion(DialogAdministrarContenido)

    def on_mostrar_asociaciones(self, event):
        conf = ConfiguracionController()
        if self.mostrar_asociaciones:
            self.frame_asociar.pack(side=TOP, fill=X, padx=1, pady=1, before=self.separador1)
            self.mostrar_asociaciones = False
            conf.set_mostrar_asociaciones("1")
        else:
            self.frame_asociar.pack_forget()
            self.mostrar_asociaciones = True
            conf.set_mostrar_asociaciones("0")

    def on_mostrar_datos_bibliograficos(self, event):
        conf = ConfiguracionController()
        if self.mostrar_datos_bibliograficos:
            self.frame_datos_bibliograficos.pack(
                side=TOP, fill=X, padx=1, pady=1, before=self.separador2
            )
            self.mostrar_datos_bibliograficos = False
            conf.set_mostrar_datos_bibliograficos("1")
        else:
            self.frame_datos_bibliograficos.pack_forget()
            self.mostrar_datos_bibliograficos = True
            conf.set_mostrar_datos_bibliograficos("0")

    def on_mostrar_operaciones(self, event):
        conf = ConfiguracionController()
        if self.mostrar_operaciones:
            self.frame_operaciones.pack(side=TOP, fill=X, padx=1, pady=1, before=self.separador3)
            self.mostrar_operaciones = False
            conf.set_mostrar_operaciones("1")
        else:
            self.frame_operaciones.pack_forget()
            self.mostrar_operaciones = True
            conf.set_mostrar_operaciones("0")

    def on_mostrar_menu(self):
        if self.mostrar_menu:
            self.frame_izquierdo.pack(side=LEFT, fill=Y, padx=1, pady=1, before=self.frame_derecho)
            self.mostrar_menu = False
        else:
            self.frame_izquierdo.pack_forget()
            self.mostrar_menu = True
