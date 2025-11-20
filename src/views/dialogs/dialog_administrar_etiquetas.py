from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_administrar_etiquetas import AdministrarEtiquetas


class DialogAdministrarEtiquetas(Toplevel):
    def __init__(self, title="Administrar etiquetas", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("600x400+15+15")
        self.resizable(True, True)

        frame = AdministrarEtiquetas(self)
        frame.pack(side=TOP, fill=BOTH, expand=True)
