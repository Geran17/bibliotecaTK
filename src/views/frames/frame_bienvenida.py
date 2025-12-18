from ttkbootstrap import Frame, Label, Separator, Button, Style
from ttkbootstrap.constants import *


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
            command_config: Función a ejecutar para el botón 'Configuraciones'.
            **kwargs: Argumentos adicionales para el Frame.
        """
        super().__init__(master, **kwargs)

        # --- Estilos ---
        self.estilo = Style()
        self.estilo.configure("Titulo.TLabel", font=("Helvetica", 24, "bold"))
        self.estilo.configure("Subtitulo.TLabel", font=("Helvetica", 14))
        self.estilo.configure("Seccion.TLabel", font=("Helvetica", 12, "bold"))
        self.estilo.configure("Pie.TLabel", font=("Helvetica", 8, "italic"))
        # Estilo para los botones de acceso rápido con fuente más grande
        self.estilo.configure("Grande.Outline.TButton", font=("Helvetica", 11, "bold"))

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
        lbl_titulo.pack(pady=(20, 10))

        # --- Subtítulo o Lema ---
        lbl_subtitulo = Label(
            frame_contenido,
            text="Gestiona, organiza y explora tus documentos de forma eficiente.",
            bootstyle="secondary",
            style="Subtitulo.TLabel",
        )
        lbl_subtitulo.pack(pady=(0, 25))

        # --- Separador Visual ---
        Separator(frame_contenido).pack(fill=X, padx=50, pady=10)

        # --- Sección de "Primeros Pasos" ---
        lbl_primeros_pasos = Label(
            frame_contenido,
            text="Primeros Pasos",
            bootstyle="info",
            style="Seccion.TLabel",
        )
        lbl_primeros_pasos.pack(pady=(15, 10))

        # Contenedor para los pasos, para que se alineen correctamente
        frame_pasos = Frame(frame_contenido)
        frame_pasos.pack(pady=5, padx=20)

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
        Separator(frame_contenido).pack(fill=X, padx=50, pady=(25, 10))

        # --- Sección de "Acceso Rápido" ---
        lbl_acceso_rapido = Label(
            frame_contenido,
            text="Acceso Rápido",
            bootstyle="info",
            style="Seccion.TLabel",
        )
        lbl_acceso_rapido.pack(pady=(15, 10))

        frame_botones_rapidos = Frame(frame_contenido)
        frame_botones_rapidos.pack(pady=10)

        # Botón Importar Documentos
        btn_importar = Button(
            frame_botones_rapidos,
            text="📥\nImportar Documentos",
            style="Grande.Outline.TButton",  # Aplicar el nuevo estilo
            compound=TOP,
            command=self.command_importar,
        )
        btn_importar.grid(row=0, column=0, padx=10, pady=5, ipady=10, ipadx=10, sticky="nswe")

        # Botón Administrar Documentos
        btn_admin_docs = Button(
            frame_botones_rapidos,
            text="📜\nAdministrar Documentos",
            style="Grande.Outline.TButton",  # Aplicar el nuevo estilo
            compound=TOP,
            command=self.command_documentos,
        )
        btn_admin_docs.grid(row=0, column=1, padx=10, pady=5, ipady=10, ipadx=10, sticky="nswe")

        # Botón Configuraciones
        btn_config = Button(
            frame_botones_rapidos,
            text="⚙️\nConfiguraciones",
            style="Grande.Outline.TButton",  # Aplicar el nuevo estilo
            compound=TOP,
            command=self.command_config,
        )
        btn_config.grid(row=0, column=2, padx=10, pady=5, ipady=10, ipadx=10, sticky="nswe")

        # --- Pie de Página con información del creador ---
        # Este frame se empaqueta en 'self' (el FrameBienvenida) para que se alinee en la parte inferior.
        frame_pie = Frame(self, padding=5)
        frame_pie.pack(side=BOTTOM, fill=X, padx=10, pady=5)

        lbl_creador = Label(
            frame_pie, text="Creado por: Geran @ 2025", style="Pie.TLabel", bootstyle="secondary"
        )
        lbl_creador.pack(side=LEFT)

        lbl_version = Label(
            frame_pie, text="Versión 0.1.0", style="Pie.TLabel", bootstyle="secondary"
        )
        lbl_version.pack(side=RIGHT)
