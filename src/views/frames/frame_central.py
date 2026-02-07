from ttkbootstrap import Frame, Button, Separator, Checkbutton, Notebook, IntVar, Style
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from tkinter.messagebox import showwarning
import logging
from models.controllers.configuracion_controller import ConfiguracionController
from views.dialogs.dialog_importar import DialogImportar
from views.dialogs.dialog_administrar_coleccion import DialogAdministrarColeccion
from views.dialogs.dialog_administrar_grupo import DialogAdministrarGrupos
from views.dialogs.dialog_administrar_etiquetas import DialogAdministrarEtiquetas
from views.dialogs.dialog_administrar_palabras_clave import (
    DialogAdministrarPalabrasClave,
)
from views.dialogs.dialog_administrar_categorias import (
    DialogAdministrarCategorias,
)
from views.dialogs.dialog_administrar_documentos import DialogAdministrarDocumentos
from views.dialogs.dialog_configurar_vistas import DialogConfigurarVistas
from views.dialogs.dialog_visor_metadatos import DialogVisorMetadatos
from views.frames.frame_bienvenida import FrameBienvenida
from views.frames.frame_visualizar_documentos import FrameVisualizarDocumentos
from views.frames.frame_favoritos import FrameFavoritos
from views.frames.frame_visualizar_biblioteca import FrameVisualizarBiblioteca
from views.frames.frame_visualizar_contenido import FrameVisualizarContenido
from views.frames.frame_visor_metadatos import FrameVisorMetadatos
from views.frames.frame_visualizar_estante import FrameVisualizarEstante

logger = logging.getLogger(__name__)


class FrameCentral(Frame):
    """
    Frame principal que contiene el panel lateral de navegación y el área central
    de contenido de la aplicación.
    """

    def __init__(self, master=None, **kwargs):
        """
        Inicializa el FrameCentral.

        Args:
            master: El widget padre.
            **kwargs: Argumentos adicionales para el Frame.
        """
        super().__init__(master=master, **kwargs)

        # --- Variables de estado ---
        self.panel_lateral_visible = True
        self.var_archivo = IntVar(value=0)
        self.var_organizar = IntVar(value=0)
        self.notebook_central = None
        self.tab_bienvenida = None

        # --- Referencias a las pestañas para refrescar ---
        self.tab_visualizar = None
        self.tab_favoritos = None
        self.tab_biblioteca = None
        self.tab_contenido = None
        self.tab_metadatos = None
        self.tab_estante = None

        # --- Estilos ---
        self.estilo = Style()
        self.estilo.configure("Link.TButton", anchor="w", relief="flat")

        # --- Creación de la interfaz ---
        self.crear_widgets()

        # --- Estado inicial de la interfaz ---
        self.show_panel_lateral()
        self.show_panel_archivo()
        self.show_panel_organizar()

        # --- Vinculación de eventos ---
        self.var_archivo.trace_add("write", self.on_ckb_archivo)
        self.var_organizar.trace_add("write", self.on_ckb_organizar)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Creación de Widgets de la Interfaz
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        """Crea y organiza los widgets principales del frame."""
        self._crear_panel_lateral()
        self._crear_panel_central()

    def _crear_panel_lateral(self):
        """Crea el panel de navegación lateral con sus secciones."""
        self.panel_lateral = Frame(self, padding=(2, 2), width=200)
        self.panel_lateral.pack(side=LEFT, fill=Y, padx=2, pady=2, anchor=W)
        self.panel_lateral.pack_propagate(False)

        # --- Sección "Archivo" ---
        ckb_archivos = Checkbutton(
            self.panel_lateral, text="Archivo", offvalue=0, onvalue=1, variable=self.var_archivo
        )
        ckb_archivos.pack(side=TOP, fill=X, padx=2, pady=2)

        self.separator_archivo = Separator(self.panel_lateral)
        self.separator_archivo.pack(side=TOP, fill=X, padx=1, pady=1)

        self.panel_archivos = Frame(self.panel_lateral, padding=(2, 2))
        self.panel_archivos.pack(side=TOP, fill=Y, padx=1, pady=1, anchor=W)

        btn_importar = Button(
            self.panel_archivos,
            text="📥 Importar",
            style="Link.TButton",
            command=lambda: self.on_dialog_importar(None),
        )
        btn_importar.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_importar, "Importar nuevos documentos a la biblioteca")

        btn_documentos = Button(
            self.panel_archivos,
            text="📜 Documentos",
            style="Link.TButton",
            command=lambda: self.on_dialog_documentos(None),
        )
        btn_documentos.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_documentos, "Administrar todos los documentos")

        btn_metadato = Button(
            self.panel_archivos,
            text="📝 Metadatos",
            style="Link.TButton",
            command=self.on_dialog_metadatos,
        )
        btn_metadato.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_metadato, "Abrir el visor de metadatos")

        btn_cerrar = Button(
            self.panel_archivos,
            text="⏻ Cerrar",
            style="Link.TButton",
            command=self.winfo_toplevel().quit,
        )
        btn_cerrar.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_cerrar, "Cerrar la aplicación")

        # --- Separador y Configuración ---
        Separator(self.panel_lateral).pack(side=TOP, fill=X, padx=1, pady=5)

        btn_config_vistas = Button(
            self.panel_lateral,
            text="⚙️ Configurar Vistas",
            style="Link.TButton",
            command=self.on_dialog_config_vistas,
        )
        btn_config_vistas.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_config_vistas, "Elegir qué pestañas mostrar u ocultar")

        # --- Sección "Organizar" ---
        ckb_organizar = Checkbutton(
            self.panel_lateral, text="Organizar", offvalue=0, onvalue=1, variable=self.var_organizar
        )
        ckb_organizar.pack(side=TOP, fill=X, padx=2, pady=2)

        self.separator_organizar = Separator(self.panel_lateral)
        self.separator_organizar.pack(side=TOP, fill=X, padx=1, pady=1)

        self.panel_organizar = Frame(self.panel_lateral, padding=(2, 2))
        self.panel_organizar.pack(side=TOP, fill=Y, padx=1, pady=1, anchor=W)

        btn_coleccion = Button(
            self.panel_organizar,
            text="📚 Colecciones",
            style="Link.TButton",
            command=lambda: self.on_dialog_colecciones(None),
        )
        btn_coleccion.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_coleccion, "Administrar colecciones")

        btn_grupo = Button(
            self.panel_organizar,
            text="🗂️ Grupos",
            style="Link.TButton",
            command=lambda: self.on_dialog_grupos(None),
        )
        btn_grupo.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_grupo, "Administrar grupos")

        btn_categoria = Button(
            self.panel_organizar,
            text="🗃️ Categorías",
            style="Link.TButton",
            command=lambda: self.on_dialog_categorias(None),
        )
        btn_categoria.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_categoria, "Administrar categorías")

        btn_etiqueta = Button(
            self.panel_organizar,
            text="🏷️ Etiquetas",
            style="Link.TButton",
            command=lambda: self.on_dialog_etiquetas(None),
        )
        btn_etiqueta.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_etiqueta, "Administrar etiquetas")

        btn_palabra_clave = Button(
            self.panel_organizar,
            text="🔑 Palabras Clave",
            style="Link.TButton",
            command=lambda: self.on_dialog_palabras_clave(None),
        )
        btn_palabra_clave.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_palabra_clave, "Administrar palabras clave")

        # --- Separador final y botón de refrescar ---
        Separator(self.panel_lateral).pack(side=TOP, fill=X, padx=1, pady=5)

        btn_refrescar = Button(
            self.panel_lateral,
            text="🔄 Refrescar",
            style="Link.TButton",
            command=self.on_refrescar_pestanas,
        )
        btn_refrescar.pack(side=TOP, fill=X, padx=5, pady=2)
        ToolTip(btn_refrescar, "Refrescar todas las pestañas")

    def _crear_panel_central(self):
        """Crea el panel central que contendrá el contenido principal."""
        self.panel_central = Frame(self, padding=(2, 2))
        self.panel_central.pack(side=LEFT, fill=BOTH, padx=2, pady=2, expand=True)

        self.notebook_central = Notebook(self.panel_central)
        self.notebook_central.pack(side=TOP, fill=BOTH, expand=True)

        # Obtener la configuración de visibilidad de pestañas
        config = ConfiguracionController()
        visibilidad = config.obtener_visibilidad_pestanas()

        # --- Pestaña de Bienvenida ---
        if visibilidad.get("bienvenida", True):
            self.tab_bienvenida = FrameBienvenida(
                self.notebook_central,
                command_importar=lambda: self.on_dialog_importar(None),
                command_documentos=lambda: self.on_dialog_documentos(None),
                command_config=lambda: print("Botón de configuraciones presionado"),
            )
            self.notebook_central.add(self.tab_bienvenida, text="🏠 Bienvenida")

        # --- Pestaña de Visualizar Documentos ---
        if visibilidad.get("visualizar", True):
            self.tab_visualizar = FrameVisualizarDocumentos(self.notebook_central)
            self.notebook_central.add(self.tab_visualizar, text="🔎 Visualizar")

        # --- Pestaña de Favoritos ---
        if visibilidad.get("favoritos", True):
            self.tab_favoritos = FrameFavoritos(self.notebook_central)
            self.notebook_central.add(self.tab_favoritos, text="⭐ Favoritos")

        # --- Pestaña de Visualizar Biblioteca ---
        if visibilidad.get("biblioteca", True):
            self.tab_biblioteca = FrameVisualizarBiblioteca(self.notebook_central)
            self.notebook_central.add(self.tab_biblioteca, text="📖 Biblioteca")

        # --- Pestaña de Visualizar Contenido ---
        if visibilidad.get("contenido", True):
            self.tab_contenido = FrameVisualizarContenido(self.notebook_central)
            self.notebook_central.add(self.tab_contenido, text="📑 Contenido")

        # --- Pestaña de Visualizar Metadatos ---
        if visibilidad.get("metadatos", True):
            self.tab_metadatos = FrameVisorMetadatos(self.notebook_central)
            self.notebook_central.add(self.tab_metadatos, text="🧮 Metadatos")

        # --- Pestaña de Visualizar Estante ---
        if visibilidad.get("estante", True):
            self.tab_estante = FrameVisualizarEstante(self.notebook_central)
            self.notebook_central.add(self.tab_estante, text="📚 Estante")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Manejo del Estado de la Interfaz
    # └────────────────────────────────────────────────────────────┘

    def toggle_panel_lateral(self):
        """Alterna la visibilidad del panel lateral"""
        configuracion = ConfiguracionController()
        if self.panel_lateral_visible:
            self.panel_lateral.pack_forget()
            self.panel_lateral_visible = False
            # configuracion
            configuracion.set_toggle_panel_lateral(valor=0)
        else:
            self.panel_lateral.pack(
                side=LEFT, fill=Y, padx=2, pady=2, anchor=W, before=self.panel_central
            )
            self.panel_lateral_visible = True
            # configuracion
            configuracion.set_toggle_panel_lateral(valor=1)

    def show_panel_lateral(self):
        """Muestra u oculta el panel lateral según el estado guardado en la configuración."""
        try:
            configuracion = ConfiguracionController()
            valor = configuracion.get_toogle_panel_lateral()
            if valor == 0:
                # esta oculto
                self.panel_lateral.pack_forget()
                self.panel_lateral_visible = False
            else:
                self.panel_lateral.pack(
                    side=LEFT, fill=Y, padx=2, pady=2, anchor=W, before=self.panel_central
                )
                self.panel_lateral_visible = True
        except Exception as e:
            self.panel_lateral.pack(
                side=LEFT, fill=Y, padx=2, pady=2, anchor=W, before=self.panel_central
            )
            self.panel_lateral_visible = True

    def show_panel_archivo(self):
        """Muestra u oculta la sección 'Archivo' del panel lateral según la configuración."""
        try:
            configuracion = ConfiguracionController()
            valor = configuracion.get_toogle_panel_archivo()
            self.var_archivo.set(valor)
            self._actualizar_visibilidad_panel_archivo(valor)
        except Exception:
            self.var_archivo.set(1)
            self._actualizar_visibilidad_panel_archivo(1)

    def show_panel_organizar(self):
        """Muestra u oculta la sección 'Organizar' del panel lateral según la configuración."""
        try:
            # NOTA: Asumo que tendrás una función similar a esta en tu controlador
            # configuracion = ConfiguracionController()
            # valor = configuracion.get_toogle_panel_organizar()
            valor = 1  # Valor por defecto mientras no exista en la config
            self.var_organizar.set(valor)
            self._actualizar_visibilidad_panel_organizar(valor)
        except Exception:
            self.var_organizar.set(1)
            self._actualizar_visibilidad_panel_organizar(1)

    def _actualizar_visibilidad_panel_organizar(self, valor: int):
        """Función auxiliar para mostrar u ocultar el panel de organizar."""
        if valor == 0:
            self.panel_organizar.pack_forget()
        else:
            self.panel_organizar.pack(
                side=TOP, fill=Y, padx=1, pady=1, anchor=W, after=self.separator_organizar
            )

    def _actualizar_visibilidad_panel_archivo(self, valor: int):
        """Función auxiliar para mostrar u ocultar el panel de archivos."""
        if valor == 0:
            self.panel_archivos.pack_forget()
        else:
            self.panel_archivos.pack(
                side=TOP, fill=Y, padx=1, pady=1, anchor=W, after=self.separator_archivo
            )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Manejadores de Eventos (Callbacks)
    # └────────────────────────────────────────────────────────────┘

    def on_ckb_archivo(self, *args):
        """Se ejecuta cuando cambia el estado del Checkbutton 'Archivo'."""
        valor = self.var_archivo.get()
        configuracion = ConfiguracionController()
        configuracion.set_toggle_panel_archivo(valor=valor)
        self._actualizar_visibilidad_panel_archivo(valor)

    def on_ckb_organizar(self, *args):
        """Se ejecuta cuando cambia el estado del Checkbutton 'Organizar'."""
        valor = self.var_organizar.get()
        # NOTA: Asumo que tendrás una función similar a esta en tu controlador
        # configuracion = ConfiguracionController()
        # configuracion.set_toggle_panel_organizar(valor=valor)
        self._actualizar_visibilidad_panel_organizar(valor)

    def on_dialog_importar(self, event):
        """Abre el diálogo para importar documentos."""
        dialog = DialogImportar()
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_config_vistas(self):
        """Abre el diálogo para configurar la visibilidad de las pestañas."""
        dialog = DialogConfigurarVistas(master=self)
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_colecciones(self, event):
        """Abre el diálogo para administrar colecciones."""
        dialog = DialogAdministrarColeccion()
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_grupos(self, event):
        """Abre el diálogo para administrar grupos."""
        dialog = DialogAdministrarGrupos()
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_etiquetas(self, event):
        """Abre el diálogo para administrar etiquetas."""
        dialog = DialogAdministrarEtiquetas()
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_palabras_clave(self, event):
        """Abre el diálogo para administrar palabras clave."""
        dialog = DialogAdministrarPalabrasClave()
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_categorias(self, event):
        """Abre el diálogo para administrar categorías."""
        dialog = DialogAdministrarCategorias()
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_documentos(self, event):
        """Abre el diálogo para administrar categorías."""
        dialog = DialogAdministrarDocumentos()
        dialog.update_idletasks()
        dialog.grab_set()

    def on_dialog_metadatos(self):
        """Abre la vista de metadatos desde el panel lateral."""
        if self.tab_metadatos and self.notebook_central:
            self.notebook_central.select(self.tab_metadatos)
            return

        dialog = DialogVisorMetadatos(master=self)
        dialog.update_idletasks()
        dialog.grab_set()

    def on_refrescar_pestanas(self):
        """Refrescar todas las pestañas activas."""
        pestanas = [
            ("Visualizar", self.tab_visualizar),
            ("Favoritos", self.tab_favoritos),
            ("Biblioteca", self.tab_biblioteca),
            ("Contenido", self.tab_contenido),
            ("Metadatos", self.tab_metadatos),
            ("Estante", self.tab_estante),
        ]
        errores = []

        for nombre, tab in pestanas:
            if tab and hasattr(tab, "actualizar_tabla"):
                try:
                    tab.actualizar_tabla()
                except Exception as ex:
                    logger.exception("Error al refrescar pestaña '%s'", nombre)
                    errores.append(f"{nombre}: {ex}")

        if errores:
            detalle = "\n".join(f"- {error}" for error in errores[:5])
            if len(errores) > 5:
                detalle += f"\n- ... y {len(errores) - 5} error(es) adicional(es)"
            showwarning(
                title="Refresco incompleto",
                message=f"Algunas pestañas no se pudieron refrescar:\n{detalle}",
                parent=self,
            )
