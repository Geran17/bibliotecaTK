from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_administrar_palabras_clave import AdministrarPalabrasClave


class DialogAdministrarPalabrasClave(Toplevel):
    def __init__(self, title="Administrar Palabras Clave", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("600x400+15+15")
        self.resizable(True, True)

        frame = AdministrarPalabrasClave(self)
        frame.pack(side=TOP, fill=BOTH, expand=True)
