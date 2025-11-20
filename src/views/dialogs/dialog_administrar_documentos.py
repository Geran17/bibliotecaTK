from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_administrar_documentos import AdministrarDocumentos


class DialogAdministrarDocumentos(Toplevel):
    def __init__(self, title="Administrar documentos", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("900x700+10+10")
        self.resizable(True, True)

        frame = AdministrarDocumentos(self)
        frame.pack(side=TOP, fill=BOTH, expand=True)
