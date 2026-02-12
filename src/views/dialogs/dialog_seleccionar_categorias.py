from ttkbootstrap import Toplevel
from typing import List
from ttkbootstrap.constants import *
from views.frames.frame_seleccionar_categorias import FrameSeleccionarCategorias


class DialogSeleccionarCategorias(Toplevel):
    def __init__(self, title="Seleccionar categorías", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.resizable(True, True)

        self.frame = FrameSeleccionarCategorias(self)
        self.frame.pack(side=TOP, fill=BOTH, expand=True)

        # Calcular el tamaño requerido del contenido
        self.update_idletasks()
        ancho = self.frame.winfo_reqwidth()
        alto = self.frame.winfo_reqheight()

        # Aplicar máximos para no exceder la pantalla (80% del ancho y alto de la pantalla)
        ancho_max = int(self.winfo_screenwidth() * 0.8)
        alto_max = int(self.winfo_screenheight() * 0.8)

        ancho = min(ancho, ancho_max)
        alto = min(alto, alto_max)

        # Centrar en la pantalla
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def obtener_documentos_seleccionados(self, documentos_seleccionados: List):
        if documentos_seleccionados:
            self.frame.obtener_documentos_seleccionados(
                documentos_seleccionados=documentos_seleccionados
            )
