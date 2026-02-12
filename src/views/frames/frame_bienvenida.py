from ttkbootstrap import Frame, Label, Separator, Button, Style
from ttkbootstrap.constants import *
from views.components.ui_tokens import (
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_SECTION,
    FONT_CAPTION,
    PADDING_OUTER,
    PADDING_PANEL,
)


class FrameBienvenida(Frame):
    """
    Un frame de bienvenida para mostrar al iniciar la aplicación.
    Proporciona una introducción visual y guías rápidas sobre las
    funcionalidades principales.
    """

    def __init__(
        self,
        master=None,
        command_importar=None,
        command_documentos=None,
        command_config=None,
        **kwargs,
    ):
        """
        Inicializa el frame de bienvenida.

        Args:
            master: El widget padre.
            command_importar: Función a ejecutar para el botón 'Importar'.
            command_documentos: Función a ejecutar para el botón 'Administrar Documentos'.
            command_config: Función a ejecutar para el botón 'Configuración'.
            **kwargs: Argumentos adicionales para el Frame.
        """
        super().__init__(master, **kwargs)

        # --- Estilos ---
        self.estilo = Style()
        self.estilo.configure("Titulo.TLabel", font=FONT_TITLE)
        self.estilo.configure("Subtitulo.TLabel", font=FONT_SUBTITLE)
        self.estilo.configure("Seccion.TLabel", font=FONT_SECTION)
        self.estilo.configure("Pie.TLabel", font=FONT_CAPTION)
        # Estilo para los botones de acceso rápido con fuente más grande
        self.estilo.configure("Grande.Outline.TButton", font=FONT_SECTION)

        # --- Comandos ---
        self.command_importar = command_importar
        self.command_documentos = command_documentos
        self.command_config = command_config

        # --- Creación de la interfaz de bienvenida ---
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y organiza todos los widgets dentro del frame de bienvenida.
        """
        # Frame principal para centrar el contenido verticalmente
        frame_contenido = Frame(self)
        frame_contenido.pack(expand=True)

        # --- Título Principal ---
        lbl_titulo = Label(
            frame_contenido,
            text="📚 Bienvenido a tu Biblioteca Digital",
            bootstyle="primary",
            style="Titulo.TLabel",
        )
        lbl_titulo.pack(pady=(PADDING_OUTER * 2, PADDING_PANEL))

        # --- Subtítulo o Lema ---
        lbl_subtitulo = Label(
            frame_contenido,
            text="Gestiona, organiza y explora tus documentos de forma eficiente.",
            bootstyle="secondary",
            style="Subtitulo.TLabel",
        )
        lbl_subtitulo.pack(pady=(0, PADDING_OUTER * 3))

        # --- Separador Visual ---
        Separator(frame_contenido).pack(fill=X, padx=PADDING_OUTER * 6, pady=PADDING_OUTER)

        # --- Sección de "Primeros Pasos" ---
        lbl_primeros_pasos = Label(
            frame_contenido,
            text="Primeros Pasos",
            bootstyle="info",
            style="Seccion.TLabel",
        )
        lbl_primeros_pasos.pack(pady=(PADDING_OUTER * 2, PADDING_OUTER))

        # Contenedor para los pasos, para que se alineen correctamente
        frame_pasos = Frame(frame_contenido)
        frame_pasos.pack(pady=PADDING_PANEL, padx=PADDING_OUTER * 2)

        # Paso 1: Importar
        lbl_paso1 = Label(
            frame_pasos,
            text="1. 📥 Importa tus documentos usando el menú 'Archivo > Importar'.",
        )
        lbl_paso1.pack(anchor=W, pady=2)

        # Paso 2: Administrar
        lbl_paso2 = Label(
            frame_pasos,
            text="2. 📜 Administra tus archivos desde 'Archivo > Documentos'.",
        )
        lbl_paso2.pack(anchor=W, pady=2)

        # Paso 3: Organizar
        lbl_paso3 = Label(
            frame_pasos,
            text="3. 🗂️ Organiza tus documentos con colecciones, categorías, etiquetas y más.",
        )
        lbl_paso3.pack(anchor=W, pady=2)

        # --- Separador Visual ---
        Separator(frame_contenido).pack(
            fill=X,
            padx=PADDING_OUTER * 6,
            pady=(PADDING_OUTER * 3, PADDING_OUTER),
        )

        # --- Sección de "Acceso Rápido" ---
        lbl_acceso_rapido = Label(
            frame_contenido,
            text="Acceso Rápido",
            bootstyle="info",
            style="Seccion.TLabel",
        )
        lbl_acceso_rapido.pack(pady=(PADDING_OUTER * 2, PADDING_OUTER))

        frame_botones_rapidos = Frame(frame_contenido)
        frame_botones_rapidos.pack(pady=PADDING_OUTER)

        # Botón Importar Documentos
        btn_importar = Button(
            frame_botones_rapidos,
            text="📥\nImportar Documentos",
            style="Grande.Outline.TButton",  # Aplicar el nuevo estilo
            compound=TOP,
            command=self.command_importar,
        )
        btn_importar.grid(
            row=0,
            column=0,
            padx=PADDING_OUTER,
            pady=PADDING_PANEL,
            ipady=PADDING_OUTER,
            ipadx=PADDING_OUTER,
            sticky="nswe",
        )

        # Botón Administrar Documentos
        btn_admin_docs = Button(
            frame_botones_rapidos,
            text="📜\nAdministrar Documentos",
            style="Grande.Outline.TButton",  # Aplicar el nuevo estilo
            compound=TOP,
            command=self.command_documentos,
        )
        btn_admin_docs.grid(
            row=0,
            column=1,
            padx=PADDING_OUTER,
            pady=PADDING_PANEL,
            ipady=PADDING_OUTER,
            ipadx=PADDING_OUTER,
            sticky="nswe",
        )

        # Botón Configuración
        btn_config = Button(
            frame_botones_rapidos,
            text="⚙️\nConfiguración",
            style="Grande.Outline.TButton",  # Aplicar el nuevo estilo
            compound=TOP,
            command=self.command_config,
        )
        btn_config.grid(
            row=0,
            column=2,
            padx=PADDING_OUTER,
            pady=PADDING_PANEL,
            ipady=PADDING_OUTER,
            ipadx=PADDING_OUTER,
            sticky="nswe",
        )

        # --- Pie de Página con información del creador ---
        # Este frame se empaqueta en 'self' (el FrameBienvenida) para que se alinee en la parte inferior.
        frame_pie = Frame(self, padding=PADDING_PANEL)
        frame_pie.pack(side=BOTTOM, fill=X, padx=PADDING_OUTER, pady=PADDING_PANEL)

        lbl_creador = Label(
            frame_pie, text="Creado por: Geran @ 2025", style="Pie.TLabel", bootstyle="secondary"
        )
        lbl_creador.pack(side=LEFT)

        lbl_version = Label(
            frame_pie, text="Versión 0.1.0", style="Pie.TLabel", bootstyle="secondary"
        )
        lbl_version.pack(side=RIGHT)

    def actualizar_tabla(self):
        """
        Método para compatibilidad con el sistema de refrescado de pestañas.
        La pestaña de bienvenida no tiene tabla que refrescar.
        """
        pass
