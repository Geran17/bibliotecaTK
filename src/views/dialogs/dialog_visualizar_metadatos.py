from ttkbootstrap import Toplevel
from views.frames.frame_visualizar_metadatos import FrameVisualizarMetadatos
from models.entities.documento import Documento


class DialogVisualizarMetadatos(Toplevel):
    def __init__(self, title="Visualizar Metadatos", **kwargs):
        super().__init__(title=title, **kwargs)
        # Configuraciones de la ventana
        self.geometry("600x400+20+20")
        self.resizable(True, True)

        # Crear el frame de visualización de metadatos dentro del dialog
        self.frame_metadatos = FrameVisualizarMetadatos(self)
        self.frame_metadatos.pack(fill="both", expand=True, padx=10, pady=10)

    def set_documento(self, documento: Documento):
        """Establece el documento para cargar metadatos desde la base de datos."""
        self.frame_metadatos.set_documento(documento)

    def set_path_file(self, path_file: str):
        """Establece la ruta del archivo para cargar metadatos directamente del archivo."""
        self.frame_metadatos.set_path_file(path_file)
