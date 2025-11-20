from ttkbootstrap import Toplevel, LabelFrame, Frame, Label, Entry, Button, StringVar, Combobox
from tkinter import filedialog
from ttkbootstrap.constants import *
from os.path import expanduser
from models.controllers.configuracion_controller import ConfiguracionController


class DialogConfigurar(Toplevel):
    def __init__(self, title="Configuraciones", **kwargs):
        super().__init__(title=title, **kwargs)

        # Configuración de la ventana
        self.geometry("600x400+10+10")
        self.resizable(True, True)

        # variables
        self.ubicacion_biblioteca = StringVar()
        self.temas = self.style.theme_names()

        # instanciamos los widgets
        self.crear_widgets()

        # establecemos la ubicacion de la bibliteca si existe
        self.establecer_ubicacion_biblioteca()
        self.establecer_tema()

    def crear_widgets(self):

        # frame principal
        frame_principal = Frame(self, padding=2)
        frame_principal.pack(side=TOP, fill=BOTH, expand=TRUE)

        # --------------- LabelFrame: Ubicacion de la Biblioteca ----------------------#

        # Ubicacion de la biblioteca
        label_frame_biblioteca = LabelFrame(frame_principal, text="Biblioteca")
        label_frame_biblioteca.pack(side=TOP, fill=X, padx=2, pady=2)

        label_frame_biblioteca.columnconfigure(0, weight=1)

        # Label indicacion
        label_biblioteca = Label(
            label_frame_biblioteca, text="Seleccione la ubicación de tu ubicación: ", padding=(2, 2)
        )
        label_biblioteca.grid(column=0, row=0, sticky=EW, columnspan=2)

        # Entry Ubicacion
        self.entry_ubicacion = Entry(
            label_frame_biblioteca,
            state=READONLY,
            textvariable=self.ubicacion_biblioteca,
            bootstyle="info",
        )
        self.entry_ubicacion.grid(column=0, row=1, sticky=EW, padx=2, pady=2)

        # Button Seleccionar
        button_seleccionar = Button(
            label_frame_biblioteca, text="Seleccionar", command=self.seleccionar_carpeta
        )
        button_seleccionar.grid(column=1, row=1, sticky=EW, padx=2, pady=2)

        # Label Info Ubicacion
        label_info_ubicacion = Label(
            label_frame_biblioteca,
            text="*Seleccione la ubicacion para la biblioteca. En la ubicacion se creara la carpeta 'BibliotecaTK'",
            padding=(2, 2),
        )
        label_info_ubicacion.configure(font=("Arial", 8, "italic"), foreground="gray")
        label_info_ubicacion.grid(column=0, row=2, sticky=EW, padx=2, pady=2)

        # ----------------------- LabelFrame: Seleccionar Tema -----------------------------#
        label_frame_tema = LabelFrame(frame_principal, text="Seleccionar Tema")
        label_frame_tema.pack(side=TOP, fill=X, padx=2, pady=2)
        label_frame_tema.columnconfigure(1, weight=1)

        label_selecionar_tema = Label(label_frame_tema, text="Seleccione un tema:")
        label_selecionar_tema.grid(column=0, row=0, sticky=EW, padx=2, pady=2)

        self.combobox_temas = Combobox(
            label_frame_tema, state=READONLY, values=self.temas, bootstyle="info"
        )
        self.combobox_temas.grid(column=1, row=0, sticky=EW, padx=2, pady=2)

        button_aplicar_tema = Button(
            label_frame_tema, text="Aplicar", command=self.on_tema_seleccionado
        )
        button_aplicar_tema.grid(column=2, row=0, sticky=EW, padx=2, pady=2)

        # Label Info Ubicacion
        label_info_tema = Label(
            label_frame_tema,
            text="*Seleccione un tema de la lista. El tema seleccionado se aplicara luego que la aplicacion se reinicie",
            padding=(2, 2),
        )
        label_info_tema.configure(font=("Arial", 8, "italic"), foreground="gray")
        label_info_tema.grid(column=0, row=1, sticky=EW, padx=2, pady=2, columnspan=3)

    def establecer_ubicacion_biblioteca(self):
        configuracion = ConfiguracionController()
        if isinstance(configuracion, ConfiguracionController):
            if configuracion.obtener_ubicacion_biblioteca() != "":
                self.ubicacion_biblioteca.set(configuracion.obtener_ubicacion_biblioteca())

    def establecer_tema(self):
        configuracion = ConfiguracionController()
        if isinstance(configuracion, ConfiguracionController):
            if configuracion.obtener_tema() != "":
                self.combobox_temas.set(configuracion.obtener_tema())

    def on_tema_seleccionado(self):
        tema = self.combobox_temas.get()
        if tema != "":
            configuracion = ConfiguracionController()
            configuracion.establecer_tema(tema=tema)
            self.style.theme_use(themename=tema)

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(
            title="Seleccione la ubicacion para la biblioteca",
            initialdir=expanduser("~"),
            parent=self,
        )
        configuracion = ConfiguracionController()
        if isinstance(configuracion, ConfiguracionController):
            if carpeta:
                resp = configuracion.establecer_ubicacion_biblioteca(directrio=carpeta)
                if resp:
                    self.ubicacion_biblioteca.set(configuracion.obtener_ubicacion_biblioteca())
