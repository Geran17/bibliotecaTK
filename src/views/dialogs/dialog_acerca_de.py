from ttkbootstrap import Toplevel, Label, Button, Separator, Frame, Style
from ttkbootstrap.constants import *
from views.components.ui_tokens import FONT_TITLE, FONT_SUBTITLE, PADDING_OUTER


class DialogAcercaDe(Toplevel):
    """
    Diálogo que muestra información sobre la aplicación, como la versión
    y el autor.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Acerca de Biblioteca Digital")
        self.transient(master)
        self.resizable(True, True)

        # --- Estilos ---
        self.estilo = Style()
        self.estilo.configure("Titulo.TLabel", font=FONT_TITLE)
        self.estilo.configure("Info.TLabel", font=FONT_SUBTITLE)

        self._crear_widgets()

        # Calcular el tamaño requerido del contenido
        self.update_idletasks()
        ancho = self.winfo_reqwidth()
        alto = self.winfo_reqheight()

        # Aplicar mínimos
        ancho = max(ancho, 350)
        alto = max(alto, 250)

        # Centrar en la pantalla
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.grab_set()

    def _crear_widgets(self):
        """Crea y organiza los widgets del diálogo."""
        frame_contenido = Frame(self, padding=PADDING_OUTER * 2)
        frame_contenido.pack(expand=True, fill=BOTH)

        # --- Título ---
        lbl_titulo = Label(
            frame_contenido,
            text="Biblioteca Digital",
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
