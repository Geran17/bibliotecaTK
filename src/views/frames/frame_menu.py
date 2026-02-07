from ttkbootstrap import Frame, Button, Style, Separator, Menubutton, Menu
from ttkbootstrap.constants import *
from views.dialogs.dialog_configurar import DialogConfigurar
from views.dialogs.dialog_acerca_de import DialogAcercaDe
from ttkbootstrap.tooltip import ToolTip
import logging

logger = logging.getLogger(__name__)


class FrameMenu(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Hacemos referencia al FrameCentral, desde la app principal
        self.frame_central = None

        # instanciamos los widgets
        self.crear_widgets()

    def set_frame_central(self, frame_central: Frame):
        """Establcemos la referencia al FrameCentral correct"""
        self.frame_central = frame_central

    def crear_widgets(self):
        """
        Crea los botones de la barra de menú a partir de una lista de diccionarios
        para mejorar la escalabilidad y mantenibilidad del código.
        """
        # --- Definición de los botones ---
        botones_derecha = [
            {
                "text": "🛠️",
                "command": self.abrir_dialog_configurar,
                "tooltip": "Abrir configuración",
                "padx": (2, 5),
            },
            {
                "text": "❓",
                "command": self.abrir_dialog_acerca_de,
                "tooltip": "Ayuda / Acerca de",
                "padx": (2, 2),
            },
        ]

        botones_izquierda = [
            {
                "text": "☰",
                "command": self.toggle_panel_lateral,
                "tooltip": "Mostrar/Ocultar panel lateral",
                "padx": (5, 2),
            },
            {
                "text": "📜",
                "command": self.on_administrar_documentos,
                "tooltip": "Administrar documentos",
                "padx": 2,
            },
            {
                "text": "📥",
                "command": self.on_importar,
                "tooltip": "Importar documentos",
                "padx": 2,
            },
        ]

        # --- Creación de botones (los de la derecha primero) ---
        for config in botones_derecha:
            btn = Button(
                self,
                text=config["text"],
                style="primary.Outline.TButton",
                command=config["command"],
            )
            btn.pack(side=RIGHT, padx=config["padx"], pady=5)
            ToolTip(btn, config["tooltip"])

        # --- Separador vertical ---
        separator = Separator(self, orient=VERTICAL)
        separator.pack(side=RIGHT, fill=Y, padx=5, pady=8)

        # --- Menú desplegable "Administrar" ---
        menu_administrar_btn = Menubutton(
            self, text="🗄️ Administrar", style="primary.Outline.TButton"
        )
        menu_administrar_btn.pack(side=LEFT, padx=2, pady=5)
        ToolTip(menu_administrar_btn, "Administrar elementos de la biblioteca")

        # Crear el menú asociado
        menu_items = [
            {"label": "📚 Colecciones", "command": self.on_administrar_colecciones},
            {"label": "🗂️ Grupos", "command": self.on_administrar_grupos},
            {"label": "🗃️ Categorías", "command": self.on_administrar_categorias},
            {"label": "🏷️ Etiquetas", "command": self.on_administrar_etiquetas},
            {"label": "🔑 Palabras Clave", "command": self.on_administrar_palabras_clave},
        ]

        menu_desplegable = Menu(menu_administrar_btn, tearoff=0)
        for item in menu_items:
            menu_desplegable.add_command(label=item["label"], command=item["command"])

        menu_administrar_btn["menu"] = menu_desplegable

        for config in botones_izquierda:
            btn = Button(
                self,
                text=config["text"],
                style="primary.Outline.TButton",
                command=config["command"],
            )
            btn.pack(side=LEFT, padx=config["padx"], pady=5)
            ToolTip(btn, config["tooltip"])

    def abrir_dialog_configurar(self):
        dialog = DialogConfigurar()
        dialog.grab_set()

    def abrir_dialog_acerca_de(self):
        dialog = DialogAcercaDe()
        dialog.grab_set()

    def on_importar(self):
        """Abre el diálogo para importar documentos."""
        if self.frame_central:
            self.frame_central.on_dialog_importar(event=None)
        else:
            logger.warning("No se ha establecido frame central para la importación")

    def on_administrar_documentos(self):
        """Abre el diálogo para administrar documentos."""
        if self.frame_central:
            self.frame_central.on_dialog_documentos(event=None)
        else:
            logger.warning("No se ha establecido frame central para administrar documentos")

    def toggle_panel_lateral(self):
        """Alterna la visibilidad del panel lateral"""
        if self.frame_central:
            self.frame_central.toggle_panel_lateral()
        else:
            logger.warning("No se ha establecido frame central para toggle_panel_lateral")

    def on_administrar_colecciones(self):
        """Abre el diálogo para administrar colecciones."""
        if self.frame_central:
            self.frame_central.on_dialog_colecciones(event=None)
        else:
            logger.warning("No se ha establecido frame central para administrar colecciones")

    def on_administrar_grupos(self):
        """Abre el diálogo para administrar grupos."""
        if self.frame_central:
            self.frame_central.on_dialog_grupos(event=None)
        else:
            logger.warning("No se ha establecido frame central para administrar grupos")

    def on_administrar_categorias(self):
        """Abre el diálogo para administrar categorías."""
        if self.frame_central:
            self.frame_central.on_dialog_categorias(event=None)
        else:
            logger.warning("No se ha establecido frame central para administrar categorías")

    def on_administrar_etiquetas(self):
        """Abre el diálogo para administrar etiquetas."""
        if self.frame_central:
            self.frame_central.on_dialog_etiquetas(event=None)
        else:
            logger.warning("No se ha establecido frame central para administrar etiquetas")

    def on_administrar_palabras_clave(self):
        """Abre el diálogo para administrar palabras clave."""
        if self.frame_central:
            self.frame_central.on_dialog_palabras_clave(event=None)
        else:
            logger.warning("No se ha establecido frame central para administrar palabras clave")
