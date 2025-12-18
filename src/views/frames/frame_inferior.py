from ttkbootstrap import Frame, Label, Separator
from ttkbootstrap.constants import *
import math
from models.controllers.configuracion_controller import ConfiguracionController
from models.entities.consulta import Consulta


class FrameInferior(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Instanciamos los widgets
        self.crear_widgets()
        # Actualizamos la información al iniciar
        self.actualizar_informacion()

    def crear_widgets(self):
        """
        Crea los widgets para mostrar la información del estado de la biblioteca
        en la parte inferior de la aplicación.
        """
        # Separador para dar un aspecto más limpio
        separator = Separator(self, orient=HORIZONTAL)
        separator.pack(side=TOP, fill=X, padx=5, pady=(0, 2))

        # Frame para contener la información
        info_frame = Frame(self)
        info_frame.pack(side=BOTTOM, fill=X, padx=10, pady=(2, 5))

        # Label para la ubicación de la biblioteca (inicialmente con placeholder)
        self.lbl_ubicacion = Label(
            info_frame, text="📂 Ubicación: Cargando...", bootstyle="secondary", anchor=W
        )
        self.lbl_ubicacion.pack(side=LEFT, padx=5)

        # Label para la cantidad de archivos (inicialmente con placeholder)
        self.lbl_cantidad = Label(
            info_frame, text="📄 Archivos: Cargando...", bootstyle="secondary", anchor=W
        )
        self.lbl_cantidad.pack(side=LEFT, padx=5)

        # Label para el tamaño total (inicialmente con placeholder)
        self.lbl_tamano = Label(
            info_frame, text="💾 Tamaño: Cargando...", bootstyle="secondary", anchor=W
        )
        self.lbl_tamano.pack(side=LEFT, padx=5)

    def actualizar_informacion(self):
        """
        Actualiza los labels con la información actual de la biblioteca:
        ubicación, cantidad de archivos y tamaño total.
        """
        config = ConfiguracionController()
        consulta = Consulta()

        # 1. Ubicación de la biblioteca
        ubicacion = config.obtener_ubicacion_biblioteca()
        if ubicacion:
            self.lbl_ubicacion.config(text=f"📂 Ubicación: {ubicacion}")
        else:
            self.lbl_ubicacion.config(text="📂 Ubicación: No configurada")

        # 2. Cantidad de archivos
        total_documentos = consulta.get_total_documentos()
        self.lbl_cantidad.config(text=f"📄 Archivos: {total_documentos}")

        # 3. Tamaño total
        total_tamano_bytes = consulta.get_total_tamano_documentos()
        tamano_formateado = self._formatear_tamano(total_tamano_bytes)
        self.lbl_tamano.config(text=f"💾 Tamaño: {tamano_formateado}")

    def _formatear_tamano(self, bytes_size: int) -> str:
        """
        Formatea el tamaño de un archivo de bytes a una unidad legible (B, KB, MB, GB, TB, PB).
        """
        if not isinstance(bytes_size, (int, float)) or bytes_size < 0:
            return "0 B"

        if bytes_size == 0:
            return "0 B"

        unidades = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        # Calcular el índice de la unidad apropiada
        indice = min(int(math.log(bytes_size, 1024)), len(unidades) - 1)

        valor = bytes_size / (1024**indice)
        return f"{valor:.2f} {unidades[indice]}"
