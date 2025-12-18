from ttkbootstrap import Toplevel
from typing import List
from ttkbootstrap.constants import *
from views.frames.frame_seleccionar_colecciones import FrameSeleccionarColecciones


class DialogSeleccionarColecciones(Toplevel):
    def __init__(self, title="Seleccionar colecciones", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.geometry("800x600+10+10")
        self.resizable(True, True)

        self.frame = FrameSeleccionarColecciones(self)
        self.frame.pack(side=TOP, fill=BOTH, expand=True)

    def obtener_documentos_seleccionados(self, documentos_seleccionados: List):
        if documentos_seleccionados:
            self.frame.obtener_documentos_seleccionados(
                documetos_seleccionados=documentos_seleccionados
            )
