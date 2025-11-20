from ttkbootstrap import Frame, Button, Style
from ttkbootstrap.constants import *
from views.dialogs.dialog_configurar import DialogConfigurar


class FrameMenu(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Hacemos referencia al FrameCentral, desde la app principal
        self.frame_central = None

        self.estilo = Style()
        self.estilo.configure('Custom.TButton', justify=LEFT, anchor=W, bordercolor="SteelBlue1")

        # instanciamos los widgets
        self.crear_widgets()

    def set_frame_central(self, frame_central: Frame):
        """Establcemos la referencia al FrameCentral correct"""
        self.frame_central = frame_central

    def crear_widgets(self):
        # Button Menu
        button_menu = Button(
            self, text="☰", command=self.toggle_panel_lateral, style="Custom.TButton"
        )
        button_menu.pack(side=LEFT, fill=X, padx=2)

        # Button Importa
        button_importar = Button(self, text="📥", style="Custom.TButton")
        button_importar.pack(side=LEFT, fill=X, padx=2)

        # Button Configuraciones
        button_configurar = Button(
            self, text="🛠️", style="Custom.TButton", command=self.abrir_dialog_configurar
        )
        button_configurar.pack(side=LEFT, fill=X, padx=2)

    def abrir_dialog_configurar(self):
        dialog = DialogConfigurar()
        dialog.grab_set()

    def toggle_panel_lateral(self):
        """Alterna la visibilidad del panel lateral"""
        if self.frame_central:
            self.frame_central.toggle_panel_lateral()
        else:
            print("Error: No se ha establcecido frame central")
