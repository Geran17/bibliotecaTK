from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_administrar_categorias import AdministrarCategorias


class DialogAdministrarCategorias(Toplevel):
    def __init__(self, title="Administrar Categorías", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("700x500+20+20")
        self.resizable(True, True)

        frame = AdministrarCategorias(self)
        frame.pack(side=TOP, fill=BOTH, expand=True)
