from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from typing import List
from views.frames.frame_administrar_bibliografia import FrameAdministrarBibliografia


class DialogAdministrarBibliografia(Toplevel):
    def __init__(self, title="Administrar Bibliografias", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("800x600+10+10")
        self.resizable(True, True)

        self.frame = FrameAdministrarBibliografia(self)
        self.frame.pack(side=TOP, fill=BOTH, expand=True)

    def obtener_documentos_seleccionados(self, documentos_seleccionados: List):
        if documentos_seleccionados:
            self.frame.obtener_documentos_seleccionados(
                documentos_seleccionados=documentos_seleccionados
            )
