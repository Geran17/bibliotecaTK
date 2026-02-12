from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_visor_metadatos import FrameVisorMetadatos


class DialogVisorMetadatos(Toplevel):
    def __init__(self, title="Visor de metadatos", **kwargs):
        super().__init__(title=title, **kwargs)
        self.resizable(True, True)

        self.frame = FrameVisorMetadatos(self)
        self.frame.pack(side=TOP, fill=BOTH, expand=True)

        self.update_idletasks()
        ancho = self.frame.winfo_reqwidth()
        alto = self.frame.winfo_reqheight()

        ancho_max = int(self.winfo_screenwidth() * 0.8)
        alto_max = int(self.winfo_screenheight() * 0.8)

        ancho = min(ancho, ancho_max)
        alto = min(alto, alto_max)

        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
