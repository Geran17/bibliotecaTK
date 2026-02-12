from ttkbootstrap import Toplevel, LabelFrame, Frame, Label, Entry, Button, StringVar, Combobox
from tkinter import filedialog, messagebox
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from os.path import expanduser
from models.controllers.configuracion_controller import ConfiguracionController
from views.components.ui_tokens import (
    FONT_TITLE,
    FONT_CAPTION,
    PADDING_OUTER,
    PADDING_PANEL,
)


class DialogConfigurar(Toplevel):
    def __init__(self, title="Configuración", **kwargs):
        super().__init__(title=title, **kwargs)

        # Configuración de la ventana
        self.resizable(True, True)

        # variables
        self.ubicacion_biblioteca = StringVar()
        self.temas = self.style.theme_names()
        self.entornos_ui = ["tkinter"]
        self.estilo_citacion = StringVar()
        self.estilos_citacion_lista = [
            "APA",
            "MLA",
            "Chicago",
            "Harvard",
            "Vancouver",
        ]
        self.ejemplo_citacion_var = StringVar()
        self.ejemplos_citacion = {
            "APA": "Apellido, A. A. (Año). Título del trabajo. Editorial.",
            "MLA": "Apellido, Nombre. Título del Trabajo. Editorial, Año.",
            "Chicago": "Apellido, Nombre. Título del trabajo. Lugar de publicación: Editorial, Año.",
            "Harvard": "Apellido, Inicial(es) (Año) Título del trabajo. Lugar de publicación: Editorial.",
            "Vancouver": "Apellido AA. Título del trabajo. Lugar de publicación: Editorial; Año.",
        }

        # Asignar el valor inicial a la variable de ejemplo
        estilo_inicial = self.estilos_citacion_lista[0]
        self.estilo_citacion.set(estilo_inicial)
        self.ejemplo_citacion_var.set(self.ejemplos_citacion[estilo_inicial])

        # instanciamos los widgets
        self.crear_widgets()

        # Cargamos las configuraciones guardadas
        self._cargar_configuraciones()

        # Calcular el tamaño requerido del contenido
        self.update_idletasks()
        ancho = self.winfo_reqwidth()
        alto = self.winfo_reqheight()

        # Aplicar máximos para no exceder la pantalla (80% del ancho y alto de la pantalla)
        ancho_max = int(self.winfo_screenwidth() * 0.8)
        alto_max = int(self.winfo_screenheight() * 0.8)

        ancho = min(ancho, ancho_max)
        alto = min(alto, alto_max)

        # Centrar en la pantalla
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_widgets(self):
        """
        Crea y organiza los widgets principales de la ventana de configuraciones.
        Utiliza un ScrolledFrame para permitir el desplazamiento si el contenido
        excede el tamaño de la ventana.
        """
        # Frame principal que contendrá todo
        frame_principal = Frame(self, padding=PADDING_OUTER)
        frame_principal.pack(
            side=TOP,
            fill=BOTH,
            expand=TRUE,
            padx=PADDING_OUTER,
            pady=PADDING_PANEL,
        )

        # Título de la ventana
        lbl_titulo = Label(
            frame_principal,
            text="Configuración general",
            font=FONT_TITLE,
        )
        lbl_titulo.pack(side=TOP, fill=X, pady=(0, PADDING_OUTER * 2))

        # Frame con scroll para el contenido de las configuraciones
        scrolled_content = ScrolledFrame(frame_principal, autohide=True)
        scrolled_content.pack(side=TOP, fill=BOTH, expand=TRUE, padx=5, pady=5)

        # --- Sección de Ubicación de la Biblioteca ---
        self._crear_seccion_biblioteca(scrolled_content)

        # --- Sección de Apariencia ---
        self._crear_seccion_apariencia(scrolled_content)

        # --- Sección de Estilo de Citación ---
        self._crear_seccion_citacion(scrolled_content)

    def _crear_seccion_biblioteca(self, parent: Frame):
        """
        Crea la sección para configurar la ubicación de la biblioteca.

        Args:
            parent (Frame): El widget padre donde se colocará esta sección.
        """
        lf_biblioteca = LabelFrame(parent, text="Ubicación de la biblioteca", padding=10)
        lf_biblioteca.pack(side=TOP, fill=X, pady=5, padx=5)
        lf_biblioteca.columnconfigure(0, weight=1)

        lbl_indicacion_bib = Label(lf_biblioteca, text="Ruta donde se guardarán los documentos:")
        lbl_indicacion_bib.grid(column=0, row=0, sticky=W, columnspan=2, padx=5, pady=(0, 5))

        # Entry Ubicacion
        self.entry_ubicacion = Entry(
            lf_biblioteca,
            state=READONLY,
            textvariable=self.ubicacion_biblioteca,
            bootstyle="info",
        )
        self.entry_ubicacion.grid(column=0, row=1, sticky=EW, padx=5, pady=5)

        # Button Seleccionar
        btn_seleccionar = Button(
            lf_biblioteca, text="Seleccionar", command=self.seleccionar_carpeta
        )
        btn_seleccionar.grid(column=1, row=1, sticky=EW, padx=5, pady=5)
        ToolTip(btn_seleccionar, "Seleccionar una carpeta")

        # Label info ubicación
        lbl_info_ubicacion = Label(
            lf_biblioteca,
            text="*En la ubicación seleccionada se creará la carpeta 'BibliotecaTK' para almacenar los archivos.",
            bootstyle="secondary",
        )
        lbl_info_ubicacion.configure(font=FONT_CAPTION)
        lbl_info_ubicacion.grid(column=0, row=2, sticky=W, columnspan=2, padx=5, pady=(5, 0))

    def _crear_seccion_apariencia(self, parent: Frame):
        """
        Crea la sección para configurar la apariencia y el tema de la aplicación.

        Args:
            parent (Frame): El widget padre donde se colocará esta sección.
        """
        lf_tema = LabelFrame(parent, text="Apariencia", padding=10)
        lf_tema.pack(side=TOP, fill=X, pady=5, padx=5)
        lf_tema.columnconfigure(1, weight=1)

        lbl_seleccionar_tema = Label(lf_tema, text="Tema de la aplicación:")
        lbl_seleccionar_tema.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        self.combobox_temas = Combobox(lf_tema, state=READONLY, values=self.temas, bootstyle="info")
        self.combobox_temas.grid(column=1, row=0, sticky=EW, padx=5, pady=5)

        btn_aplicar_tema = Button(lf_tema, text="Aplicar", command=self.on_tema_seleccionado)
        btn_aplicar_tema.grid(column=2, row=0, sticky=EW, padx=5, pady=5)
        ToolTip(btn_aplicar_tema, "Aplicar el tema seleccionado a la aplicación")

        lbl_seleccionar_entorno = Label(lf_tema, text="Entorno visual:")
        lbl_seleccionar_entorno.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        self.combobox_entorno_ui = Combobox(
            lf_tema,
            state=READONLY,
            values=self.entornos_ui,
            bootstyle="info",
        )
        self.combobox_entorno_ui.grid(column=1, row=1, sticky=EW, padx=5, pady=5)

        btn_aplicar_entorno = Button(
            lf_tema,
            text="Aplicar",
            command=self.on_entorno_ui_seleccionado,
        )
        btn_aplicar_entorno.grid(column=2, row=1, sticky=EW, padx=5, pady=5)
        ToolTip(btn_aplicar_entorno, "Guardar el entorno visual para el proximo inicio")

        # Label info tema
        lbl_info_tema = Label(
            lf_tema,
            text="*El tema se aplica al instante. El entorno visual se aplica al reiniciar.",
            bootstyle="secondary",
        )
        lbl_info_tema.configure(font=FONT_CAPTION)
        lbl_info_tema.grid(column=0, row=2, sticky=W, columnspan=3, padx=5, pady=(5, 0))

    def _crear_seccion_citacion(self, parent: Frame):
        """
        Crea la sección para configurar el estilo de citación bibliográfica.

        Args:
            parent (Frame): El widget padre donde se colocará esta sección.
        """
        lf_citacion = LabelFrame(parent, text="Estilo de citación bibliográfica", padding=10)
        lf_citacion.pack(side=TOP, fill=X, pady=5, padx=5)
        lf_citacion.columnconfigure(1, weight=1)

        lbl_seleccionar_citacion = Label(lf_citacion, text="Estilo de citación:")
        lbl_seleccionar_citacion.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        self.combobox_citacion = Combobox(
            lf_citacion,
            state=READONLY,
            values=self.estilos_citacion_lista,
            textvariable=self.estilo_citacion,
            bootstyle="info",
        )
        self.combobox_citacion.bind("<<ComboboxSelected>>", self.on_estilo_citacion_cambiado)
        self.combobox_citacion.grid(column=1, row=0, sticky=EW, padx=5, pady=5)

        btn_aplicar_citacion = Button(
            lf_citacion, text="Aplicar", command=self.on_estilo_citacion_seleccionado
        )
        btn_aplicar_citacion.grid(column=2, row=0, sticky=EW, padx=5, pady=5)
        ToolTip(btn_aplicar_citacion, "Guardar el estilo de citación seleccionado")

        # Label para mostrar el ejemplo de la citación
        lbl_ejemplo_titulo = Label(lf_citacion, text="Ejemplo:")
        lbl_ejemplo_titulo.grid(column=0, row=1, sticky=W, padx=5, pady=(10, 0))

        lbl_ejemplo = Label(
            lf_citacion,
            textvariable=self.ejemplo_citacion_var,
            bootstyle="secondary",
            wraplength=450,  # Ajustar para que el texto no se salga
            justify=LEFT,
        )
        lbl_ejemplo.configure(font=FONT_CAPTION)
        lbl_ejemplo.grid(column=0, row=2, sticky=W, columnspan=3, padx=5, pady=(0, 5))

    def on_estilo_citacion_cambiado(self, event=None):
        """Actualiza el ejemplo de citación cuando se selecciona un nuevo estilo."""
        estilo_seleccionado = self.estilo_citacion.get()
        ejemplo = self.ejemplos_citacion.get(estilo_seleccionado, "Ejemplo no disponible.")
        self.ejemplo_citacion_var.set(ejemplo)

    def _cargar_configuraciones(self):
        """Carga todas las configuraciones al iniciar el diálogo."""
        configuracion = ConfiguracionController()
        # Cargar ubicación de la biblioteca
        ubicacion = configuracion.obtener_ubicacion_biblioteca()
        if ubicacion:
            self.ubicacion_biblioteca.set(ubicacion)

        # Cargar tema
        tema = configuracion.obtener_tema()
        if tema:
            self.combobox_temas.set(tema)

        entorno_ui = configuracion.obtener_entorno_ui()
        if entorno_ui:
            self.combobox_entorno_ui.set(entorno_ui)
        else:
            self.combobox_entorno_ui.set("tkinter")

        # Cargar estilo de citación
        estilo = configuracion.obtener_estilo_citacion()
        if estilo and estilo in self.estilos_citacion_lista:
            self.combobox_citacion.set(estilo)
        else:
            self.combobox_citacion.current(0)  # Seleccionar APA por defecto
        self.on_estilo_citacion_cambiado()

    def on_tema_seleccionado(self):
        tema = self.combobox_temas.get()
        if tema != "":
            configuracion = ConfiguracionController()
            configuracion.establecer_tema(tema=tema)
            self.style.theme_use(themename=tema)

    def on_estilo_citacion_seleccionado(self):
        estilo = self.combobox_citacion.get()
        if estilo:
            configuracion = ConfiguracionController()
            configuracion.establecer_estilo_citacion(estilo=estilo)

    def on_entorno_ui_seleccionado(self):
        entorno_ui = self.combobox_entorno_ui.get()
        if entorno_ui:
            try:
                configuracion = ConfiguracionController()
                if configuracion.establecer_entorno_ui(entorno_ui=entorno_ui):
                    messagebox.showinfo(
                        "Entorno visual guardado",
                        f"Se guardo '{entorno_ui}'. Se aplicara al reiniciar la aplicacion.",
                        parent=self,
                    )
            except Exception as e:
                messagebox.showerror(
                    "Error al guardar",
                    f"No se pudo guardar el entorno visual: {e}",
                    parent=self,
                )

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(
            title="Seleccione la ubicación de la biblioteca",
            initialdir=expanduser("~"),
            parent=self,
        )
        configuracion = ConfiguracionController()
        if isinstance(configuracion, ConfiguracionController):
            if carpeta:
                resp = configuracion.establecer_ubicacion_biblioteca(directrio=carpeta)
                if resp:
                    self.ubicacion_biblioteca.set(configuracion.obtener_ubicacion_biblioteca())
