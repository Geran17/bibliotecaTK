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
        """Barra superior compacta y funcional."""
        btn_panel = Button(
            self,
            text="Panel",
            style="primary.Outline.TButton",
            command=self.toggle_panel_lateral,
        )
        btn_panel.pack(side=LEFT, padx=(5, 2), pady=5)
        ToolTip(btn_panel, "Mostrar u ocultar navegación lateral")

        menu_acciones_btn = Menubutton(self, text="Acciones", style="primary.Outline.TButton")
        menu_acciones_btn.pack(side=LEFT, padx=2, pady=5)
        ToolTip(menu_acciones_btn, "Acciones principales de la biblioteca")

        menu_acciones = Menu(menu_acciones_btn, tearoff=0)
        menu_acciones.add_command(label="Importar documentos", command=self.on_importar)
        menu_acciones.add_command(
            label="Administrar documentos",
            command=self.on_administrar_documentos,
        )
        menu_acciones.add_separator()
        menu_acciones.add_command(label="Colecciones", command=self.on_administrar_colecciones)
        menu_acciones.add_command(label="Grupos", command=self.on_administrar_grupos)
        menu_acciones.add_command(label="Categorías", command=self.on_administrar_categorias)
        menu_acciones.add_command(label="Etiquetas", command=self.on_administrar_etiquetas)
        menu_acciones.add_command(
            label="Palabras clave",
            command=self.on_administrar_palabras_clave,
        )
        menu_acciones_btn["menu"] = menu_acciones

        separator = Separator(self, orient=VERTICAL)
        separator.pack(side=RIGHT, fill=Y, padx=5, pady=8)

        btn_config = Button(
            self,
            text="Config",
            style="primary.Outline.TButton",
            command=self.abrir_dialog_configurar,
        )
        btn_config.pack(side=RIGHT, padx=(2, 5), pady=5)
        ToolTip(btn_config, "Configuración")

        btn_ayuda = Button(
            self,
            text="Ayuda",
            style="primary.Outline.TButton",
            command=self.abrir_dialog_acerca_de,
        )
        btn_ayuda.pack(side=RIGHT, padx=(2, 2), pady=5)
        ToolTip(btn_ayuda, "Ayuda y acerca de")

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
