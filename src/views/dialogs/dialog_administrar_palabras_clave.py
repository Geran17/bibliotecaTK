from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from views.frames.frame_administrar_palabras_clave import AdministrarPalabrasClave


class DialogAdministrarPalabrasClave(Toplevel):
    def __init__(self, title="Administrar Palabras Clave", **kwargs):
        super().__init__(title=title, **kwargs)
        # configuraciones de la ventana
        self.resizable(True, True)

        frame = AdministrarPalabrasClave(self)
        frame.pack(side=TOP, fill=BOTH, expand=True)

        # Calcular el tamaño requerido del contenido
        self.update_idletasks()
        ancho = frame.winfo_reqwidth()
        alto = frame.winfo_reqheight()

        # Aplicar máximos para no exceder la pantalla (80% del ancho y alto de la pantalla)
        ancho_max = int(self.winfo_screenwidth() * 0.8)
        alto_max = int(self.winfo_screenheight() * 0.8)

        ancho = min(ancho, ancho_max)
        alto = min(alto, alto_max)

        # Centrar en la pantalla
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")
