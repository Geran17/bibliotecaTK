from ttkbootstrap import Frame, Label, Separator, Checkbutton, Notebook, IntVar, Style
from ttkbootstrap.constants import *
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

        # --- Creación de la interfaz ---
        self.crear_widgets()

        # --- Estado inicial de la interfaz ---
        self.show_panel_lateral()
        self.show_panel_archivo()

        # --- Vinculación de eventos ---
        self.var_archivo.trace_add("write", self.on_ckb_archivo)

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

        label_importar = Label(
            self.panel_archivos,
            text="📥 Importar",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_importar.bind("<Double-Button-1>", self.on_dialog_importar)
        label_importar.pack(side=TOP, fill=X, padx=1, pady=1)

        label_metadato = Label(
            self.panel_archivos,
            text="📝 Metadato",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_metadato.pack(side=TOP, fill=X, padx=1, pady=1)

        label_cerrar = Label(
            self.panel_archivos,
            text="⏻ Cerrar",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_cerrar.pack(side=TOP, fill=X, padx=1, pady=1)

        # --- Sección "Organizar" ---
        ckb_organizar = Checkbutton(
            self.panel_lateral, text="Organizar", offvalue=0, onvalue=1, variable=self.var_organizar
        )
        ckb_organizar.pack(side=TOP, fill=X, padx=2, pady=2)

        self.separator_organizar = Separator(self.panel_lateral)
        self.separator_organizar.pack(side=TOP, fill=X, padx=1, pady=1)

        self.panel_organizar = Frame(self.panel_lateral, padding=(2, 2))
        self.panel_organizar.pack(side=TOP, fill=Y, padx=1, pady=1, anchor=W)

        label_coleccion = Label(
            self.panel_organizar,
            text="📚 Coleccion",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_coleccion.bind("<Double-Button-1>", self.on_dialog_colecciones)
        label_coleccion.pack(side=TOP, fill=X, padx=1, pady=1)

        label_grupo = Label(
            self.panel_organizar,
            text="🗂️ Grupo",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_grupo.bind("<Double-Button-1>", self.on_dialog_grupos)
        label_grupo.pack(side=TOP, fill=X, padx=1, pady=1)

        label_categoria = Label(
            self.panel_organizar,
            text="🗂️ Categoría",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_categoria.bind("<Double-Button-1>", self.on_dialog_categorias)
        label_categoria.pack(side=TOP, fill=X, padx=1, pady=1)

        label_etiqueta = Label(
            self.panel_organizar,
            text="🏷️ Etiqueta",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_etiqueta.bind("<Double-Button-1>", self.on_dialog_etiquetas)
        label_etiqueta.pack(side=TOP, fill=X, padx=1, pady=1)

        label_palabra_clave = Label(
            self.panel_organizar,
            text="🔑 Palabra clave",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        label_palabra_clave.bind("<Double-Button-1>", self.on_dialog_palabras_clave)
        label_palabra_clave.pack(side=TOP, fill=X, padx=1, pady=1)

        label_favorito = Label(
            self.panel_organizar,
            text="⭐ Favorito",
            padding=(1, 1),
            font=("Arial", 10),
            foreground="gray",
        )
        # label_favorito.bind("<Double-Button-1>", self.on_dialog_favorito)
        label_favorito.pack(side=TOP, fill=X, padx=1, pady=1)

    def _crear_panel_central(self):
        """Crea el panel central que contendrá el contenido principal."""
        self.panel_central = Frame(self, padding=(2, 2))
        self.panel_central.pack(side=LEFT, fill=BOTH, padx=2, pady=2, expand=True)

        notebook_central = Notebook(self.panel_central)
        notebook_central.pack(side=TOP, fill=BOTH, expand=True)

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

    def on_dialog_importar(self, event):
        """Abre el diálogo para importar documentos."""
        dialog = DialogImportar()
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
