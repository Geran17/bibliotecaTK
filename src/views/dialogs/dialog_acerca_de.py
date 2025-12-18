from ttkbootstrap import Toplevel, Label, Button, Separator, Frame, Style
from ttkbootstrap.constants import *


class DialogAcercaDe(Toplevel):
    """
    Diálogo que muestra información sobre la aplicación, como la versión
    y el autor.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Acerca de Biblioteca Digital")
        self.geometry("400x250")
        self.transient(master)
        self.resizable(False, False)

        # --- Estilos ---
        self.estilo = Style()
        self.estilo.configure("Titulo.TLabel", font=("Helvetica", 18, "bold"))
        self.estilo.configure("Info.TLabel", font=("Helvetica", 10))

        self._crear_widgets()
        self.grab_set()

    def _crear_widgets(self):
        """Crea y organiza los widgets del diálogo."""
        frame_contenido = Frame(self, padding=20)
        frame_contenido.pack(expand=True, fill=BOTH)

        # --- Título ---
        lbl_titulo = Label(
            frame_contenido,
            text="📚 Biblioteca Digital",
            style="Titulo.TLabel",
            bootstyle="primary",
        )
        lbl_titulo.pack(pady=(0, 10))

        # --- Versión ---
        lbl_version = Label(
            frame_contenido, text="Versión 0.1.0", style="Info.TLabel", bootstyle="secondary"
        )
        lbl_version.pack(pady=2)

        # --- Autor ---
        lbl_autor = Label(
            frame_contenido,
            text="Creado por: Geran @ 2025",
            style="Info.TLabel",
            bootstyle="secondary",
        )
        lbl_autor.pack(pady=2)

        # --- Separador ---
        Separator(frame_contenido).pack(fill=X, pady=20)

        # --- Botón de Cerrar ---
        btn_cerrar = Button(
            frame_contenido,
            text="Cerrar",
            command=self.destroy,
            bootstyle="primary-outline",
        )
        btn_cerrar.pack(pady=(10, 0))
