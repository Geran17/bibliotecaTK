import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.frames.frame_menu import FrameMenu
from views.frames.frame_central import FrameCentral
from views.frames.frame_inferior import FrameInferior
from models.controllers.configuracion_controller import ConfiguracionController
from views.components.ui_tokens import DEFAULT_FONT, TABLE_ROWHEIGHT, TREE_ROWHEIGHT


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

        # intentamos establecer el tema
        try:
            self.raiz.style.theme_use(tema_user)
            self.raiz.style.configure(".", font=DEFAULT_FONT)
            self._configurar_estilos_base()
        except Exception as e:
            print(f"Ocurrio un error al establecer el tema: {e}")
            self.raiz.style.theme_use("cosmo")

        self.centrar_ventana(1000, 800)

        # llamamos a los widgets
        self.crear_widgets()

    def centrar_ventana(self, ancho, alto):
        ancho_screen = self.raiz.winfo_screenwidth()
        alto_screen = self.raiz.winfo_screenheight()
        pos_x = (ancho_screen // 2) - (ancho // 2)
        pos_y = (alto_screen // 2) - (alto // 2)
        self.raiz.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

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

    def _configurar_estilos_base(self):
        # Densidad consistente de botones y tablas para pantallas medianas/pequeñas.
        self.raiz.style.configure("TButton", padding=(10, 6))
        self.raiz.style.configure("TEntry", padding=(6, 4))
        self.raiz.style.configure("TCombobox", padding=(6, 4))
        self.raiz.style.configure("Treeview", rowheight=TREE_ROWHEIGHT)
        self.raiz.style.configure("Table.Treeview", rowheight=TABLE_ROWHEIGHT)

    def ejecutar(self):
        # ejecutamos la aplicacion
        self.raiz.mainloop()
