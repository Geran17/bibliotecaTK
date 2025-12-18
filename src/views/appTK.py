import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.frames.frame_menu import FrameMenu
from views.frames.frame_central import FrameCentral
from views.frames.frame_inferior import FrameInferior
from models.controllers.configuracion_controller import ConfiguracionController


class AppTK:
    def __init__(self):

        # obtenemos el tema seleccionado por el usuario
        tema_user = "cosmo"
        configuracion = ConfiguracionController()
        tema_user = configuracion.obtener_tema()
        if not tema_user:
            tema_user = "cosmo"

        # creamos la ventana principal de la aplicacion
        self.raiz = ttk.Window(
            title="📚 BibliotecaTK by German Cespedes @ 2025",
            size=(1000, 800),
            resizable=(True, True),
        )

        # intemamos establecer el tema
        try:
            self.raiz.style.theme_use(tema_user)
            self.raiz.style.configure('.', font=('Noto Sans', 9))
        except Exception as e:
            print(f"Ocurrio un error al establcer el tema: {e}")
            self.raiz.style.theme_use("cosmo")

        ancho_screen = self.raiz.winfo_screenwidth()
        alto_screen = self.raiz.winfo_screenheight()

        pos_x = ancho_screen - 1000 - 5
        pos_y = alto_screen - 800 - 5

        self.raiz.geometry(f"1000x800+{pos_x}+5")

        # llamamos a los widgets
        self.crear_widgets()

    def crear_widgets(self):
        # Para ir insertando los widgets principales de la aplicacion
        frame_principal = ttk.Frame(self.raiz, padding=4)
        frame_principal.pack(fill=BOTH, expand=YES)

        # Frame Cabecera
        frame_menu = FrameMenu(frame_principal)
        frame_menu.pack(side=TOP, fill=X)

        # Frame Central
        frame_central = FrameCentral(frame_principal)
        frame_central.pack(side=TOP, expand=True, fill=BOTH)

        # Frame Inferior
        frame_inferior = FrameInferior(frame_principal)
        frame_inferior.pack(side=TOP, fill=X)

        # Conectamos el frame_menu con el FrameCentral
        frame_menu.set_frame_central(frame_central=frame_central)

    def ejeuctar(self):
        # ejecutamos la aplicacion
        self.raiz.mainloop()
