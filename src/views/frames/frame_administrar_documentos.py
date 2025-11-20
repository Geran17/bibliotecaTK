from ttkbootstrap import Frame, Button, Entry, Label, StringVar, Combobox, Checkbutton, BooleanVar
from ttkbootstrap.constants import *


class AdministrarDocumentos(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Variables Globales
        # ---------------------------
        # icons
        self.icon_favorito = "⭐"
        self.icon_grupo = "🗂️"
        self.icon_coleccion = "📚"
        self.icon_categoria = "🗃️"
        self.icon_etiqueta = "🏷️"
        self.icon_palabra_clave = "🔑"
        self.icon_libro = "📕"
        self.icon_bibliografia = "🧬"
        self.icon_exclamacion = "❗"  # este icono servira para indicar, que existe un registro en la bd, pero no existe el archivo
        # variables
        self.var_buscar = StringVar()
        self.campos = ["Nombre", "Extension", "Hash"]
        self.var_activo = BooleanVar()
        self.var_activo.set(True)

        # cargamos los widgets
        self.crear_widgets()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):

        # Panel Superior
        frame_superior = Frame(self, padding=(1, 1))
        frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)
        self.panel_superior(frame=frame_superior)

        # Panel Central
        frame_central = Frame(self, padding=(1, 1))
        frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
        self.panel_central(frame=frame_central)

        # Panel Inferior
        frame_inferior = Frame(self, padding=(1, 1))
        frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)
        self.panel_inferior(frame=frame_inferior)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Superior
    # └────────────────────────────────────────────────────────────┘

    def panel_superior(self, frame: Frame):
        """Este panel sera para navegar y buscar en la base de datos los diferentes libros"""

        # Button Menu
        btn_menu = Button(frame, text="☰")
        btn_menu.pack(side=LEFT, fill=X, padx=1, pady=1)

        # Entry Buscar
        ent_buscar = Entry(frame, textvariable=self.var_buscar)
        ent_buscar.pack(side=LEFT, fill=X, expand=True, padx=1, pady=1)

        # Combobox Campos
        self.cbx_campos = Combobox(frame, values=self.campos, state=READONLY)
        self.cbx_campos.current(0)
        self.cbx_campos.pack(side=LEFT, fill=X, padx=1, pady=1)

        # CheckButton Activo
        chc_activo = Checkbutton(frame, variable=self.var_activo, text="Activo")
        chc_activo.pack(side=LEFT, fill=X, padx=1, pady=1)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Central
    # └────────────────────────────────────────────────────────────┘

    def panel_central(self, frame: Frame):
        pass

    def panel_izquierdo(self, frame: Frame):
        """Para mostrar el menu de asociasiones de los archivos"""
        pass

    def panel_derecho(self, frame: Frame):
        """para mostrar la tabla de busqueda"""
        pass

    # ┌────────────────────────────────────────────────────────────┐
    # │ Panel Inferior
    # └────────────────────────────────────────────────────────────┘

    def panel_inferior(self, frame: Frame):
        """para trabajar con los archivos, seleccionados en la tabla"""
        pass
