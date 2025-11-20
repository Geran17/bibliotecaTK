from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_administrar_grupos import AdministrarGrupos


class DialogAdministrarGrupos(Toplevel):
    def __init__(self, title="Administrar grupos", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("600x400+10+10")
        self.resizable(True, True)

        frame = AdministrarGrupos(self)
        frame.pack(side=TOP, fill=BOTH, expand=True)
