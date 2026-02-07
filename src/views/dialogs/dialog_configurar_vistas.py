from tkinter.messagebox import showinfo
from typing import Dict

from ttkbootstrap import Toplevel, LabelFrame, Frame, Checkbutton, Button, IntVar
from ttkbootstrap.constants import *

from models.controllers.configuracion_controller import ConfiguracionController


class DialogConfigurarVistas(Toplevel):
    """
    Diálogo para que el usuario seleccione qué pestañas (vistas)
    desea mostrar en la interfaz principal.
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Configurar Vistas")
        self.transient(master)

        self.config_controller = ConfiguracionController()
        self.vars_pestanas: Dict[str, IntVar] = {}

        # Nombres de pestañas y sus textos para la UI
        self.map_pestanas = {
            "bienvenida": "🏠 Bienvenida",
            "visualizar": "🔎 Visualizar",
            "favoritos": "⭐ Favoritos",
            "biblioteca": "📖 Biblioteca",
            "contenido": "📑 Contenido",
            "metadatos": "🧮 Metadatos",
            "estante": "📚 Estante",
        }

        self._crear_widgets()
        self._cargar_configuracion_actual()

        # Calcular el tamaño requerido del contenido
        self.update_idletasks()
        ancho = self.winfo_reqwidth()
        alto = self.winfo_reqheight()

        # Aplicar máximos para no exceder la pantalla (80% del ancho y alto de la pantalla)
        ancho_max = int(self.winfo_screenwidth() * 0.8)
        alto_max = int(self.winfo_screenheight() * 0.8)

        ancho = min(ancho, ancho_max)
        alto = min(alto, alto_max)

        # Centrar en la pantalla
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_widgets(self):
        """Crea los widgets del diálogo."""
        main_frame = LabelFrame(self, text="Seleccione las pestañas a mostrar", padding=10)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        for key, texto in self.map_pestanas.items():
            var = IntVar()
            self.vars_pestanas[key] = var
            cb = Checkbutton(main_frame, text=texto, variable=var)
            cb.pack(anchor=W, padx=5, pady=2)

        button_frame = Frame(self)
        button_frame.pack(fill=X, padx=10, pady=(0, 10))

        btn_guardar = Button(
            button_frame, text="Guardar", command=self.on_guardar, style="success.TButton"
        )
        btn_guardar.pack(side=RIGHT, padx=(5, 0))

        btn_cancelar = Button(
            button_frame, text="Cancelar", command=self.destroy, style="secondary.TButton"
        )
        btn_cancelar.pack(side=RIGHT)

    def _cargar_configuracion_actual(self):
        """Lee la configuración y establece el estado de los Checkbuttons."""
        visibilidad = self.config_controller.obtener_visibilidad_pestanas()
        for key, var in self.vars_pestanas.items():
            # Si la clave existe en la config, usa su valor. Si no, True por defecto.
            var.set(1 if visibilidad.get(key, True) else 0)

    def on_guardar(self):
        """
        Guarda la configuración actual de los Checkbuttons y cierra el diálogo.
        """
        nueva_visibilidad = {key: bool(var.get()) for key, var in self.vars_pestanas.items()}

        self.config_controller.guardar_visibilidad_pestanas(nueva_visibilidad)

        showinfo(
            title="Configuración Guardada",
            message="La configuración de las vistas se ha guardado.\n\n"
            "Por favor, reinicie la aplicación para ver los cambios.",
            parent=self,
        )

        self.destroy()
