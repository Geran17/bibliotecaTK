from ttkbootstrap import Toplevel
from views.frames.frame_visualizar_metadatos import FrameVisualizarMetadatos
from models.entities.documento import Documento


class DialogVisualizarMetadatos(Toplevel):
    def __init__(self, title="Visualizar metadatos", **kwargs):
        super().__init__(title=title, **kwargs)
        # Configuraciones de la ventana
        self.resizable(True, True)

        # Crear el frame de visualización de metadatos dentro del dialog
        self.frame_metadatos = FrameVisualizarMetadatos(self)
        self.frame_metadatos.pack(fill="both", expand=True, padx=10, pady=10)

        # Calcular el tamaño requerido del contenido
        self.update_idletasks()
        ancho = self.frame_metadatos.winfo_reqwidth()
        alto = self.frame_metadatos.winfo_reqheight()

        # Aplicar máximos para no exceder la pantalla (80% del ancho y alto de la pantalla)
        ancho_max = int(self.winfo_screenwidth() * 0.8)
        alto_max = int(self.winfo_screenheight() * 0.8)

        ancho = min(ancho, ancho_max)
        alto = min(alto, alto_max)

        # Centrar en la pantalla
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def set_documento(self, documento: Documento):
        """Establece el documento para cargar metadatos desde la base de datos."""
        self.frame_metadatos.set_documento(documento)

    def set_path_file(self, path_file: str):
        """Establece la ruta del archivo para cargar metadatos directamente del archivo."""
        self.frame_metadatos.set_path_file(path_file)
