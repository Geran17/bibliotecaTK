from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_adminstrar_colecciones import AdministrarColecciones


class DialogAdministrarColeccion(Toplevel):
    def __init__(self, title="Administrar colecciones", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("600x400+10+10")
        self.resizable(True, True)

        frame = AdministrarColecciones(self)
        frame.pack(side=TOP, fill=BOTH, expand=True)
