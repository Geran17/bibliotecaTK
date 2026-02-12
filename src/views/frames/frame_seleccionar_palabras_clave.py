from tkinter.messagebox import showinfo
from ttkbootstrap import (
    Frame,
    Entry,
    StringVar,
    Checkbutton,
    Radiobutton,
    BooleanVar,
    IntVar,
    PanedWindow,
    Label,
    LabelFrame,
    Button,
)
from ttkbootstrap.scrolled import ScrolledFrame
from models.entities.consulta import Consulta
from models.entities.palabra_clave import PalabraClave
from models.entities.documento import Documento
from models.entities.documento_palabra_clave import DocumentoPalabraClave
from views.dialogs.dialog_administrar_palabras_clave import DialogAdministrarPalabrasClave
from ttkbootstrap.constants import *
from views.components.ui_tokens import FONT_SECTION, PADDING_COMPACT, PADDING_OUTER, PADDING_PANEL
from typing import List, Dict, Any


class FrameSeleccionarPalabrasClave(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # variables
        self.var_buscar_documentos = StringVar()
        self.var_buscar_palabras_clave = StringVar()
        # Variable ÚNICA para todos los radiobuttons
        self.var_radio_documento = IntVar(value=0)
        self.documentos_seleccionados: List[Documento] = []
        self.var_check_palabras_clave: Dict[str, Any] = {}
        # Flag para controlar cuando estamos cargando
        self.cargando_asociaciones = False
        # Almacenar todas las palabras clave
        self.palabras_clave: List[PalabraClave] = []

        # cargamos los widgets
        self.crear_widgets()
        # cargamos las palabras clave
        self._cargar_palabras_clave()

        # Agregar traces para búsqueda
        self.var_buscar_documentos.trace_add('write', lambda *args: self._filtrar_documentos())
        self.var_buscar_palabras_clave.trace_add(
            'write', lambda *args: self._filtrar_palabras_clave()
        )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        frame_superior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        frame_central = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        frame_inferior = Frame(self, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.panel_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

    def panel_superior(self, frame: Frame):
        label_titulo = Label(frame, text="Asociar palabras clave a los documentos", font=FONT_SECTION)
        label_titulo.pack(side=LEFT, padx=PADDING_OUTER * 2, pady=PADDING_OUTER)

    def panel_central(self, frame: Frame):

        paned_window = PanedWindow(frame, orient="vertical")
        paned_window.pack(side=TOP, fill=BOTH, expand=True, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        # --- Panel de Documentos ---
        container_documentos = LabelFrame(paned_window, text="Documentos", padding=PADDING_PANEL)
        paned_window.add(container_documentos)

        ent_buscar_documentos = Entry(container_documentos, textvariable=self.var_buscar_documentos)
        ent_buscar_documentos.pack(fill=X, padx=PADDING_PANEL, pady=(0, PADDING_OUTER))

        self.frame_documentos = ScrolledFrame(container_documentos, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_documentos.pack(fill=BOTH, expand=True, padx=PADDING_PANEL, pady=PADDING_PANEL)

        # --- Panel de Palabras Clave ---
        container_palabras_clave = LabelFrame(paned_window, text="Palabras Clave", padding=PADDING_PANEL)
        paned_window.add(container_palabras_clave)

        ent_palabras_clave = Entry(
            container_palabras_clave, textvariable=self.var_buscar_palabras_clave
        )
        ent_palabras_clave.pack(fill=X, padx=PADDING_PANEL, pady=(0, PADDING_OUTER))

        self.frame_palabras_clave = ScrolledFrame(container_palabras_clave, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_palabras_clave.pack(fill=BOTH, expand=True, padx=PADDING_PANEL, pady=PADDING_PANEL)

    def panel_inferior(self, frame: Frame):
        btn_administrar = Button(
            frame,
            text="Administrar Palabras Clave",
            command=self.on_administrar_palabras_clave,
            style="primary.Outline.TButton",
        )
        btn_administrar.pack(side=RIGHT, padx=PADDING_OUTER * 2, pady=PADDING_OUTER)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos de la clase
    # └────────────────────────────────────────────────────────────┘

    def obtener_documentos_seleccionados(self, documentos_seleccionados: List[Documento]):
        if documentos_seleccionados:
            self.documentos_seleccionados = documentos_seleccionados
            self._cargar_documentos_seleccionados()

    def procesar_palabras_clave_seleccionadas(self, id_documento):
        """Retorna una lista con los nombres de las palabras clave seleccionadas"""
        for id_palabra_clave, var in self.var_check_palabras_clave.items():
            documento_palabra_clave = DocumentoPalabraClave(
                id_documento=id_documento, id_palabra_clave=id_palabra_clave
            )

            if not documento_palabra_clave.existe():
                if var.get():
                    documento_palabra_clave.asociar()

            if documento_palabra_clave.existe():
                if not var.get():
                    documento_palabra_clave.desasociar()

    def cargar_asociaciones(self, id_documento: int):
        """
        Esta funcion se encargara de establecer las palabras clave
        que estan asociadas al documento
        """
        if id_documento != 0:
            self.cargando_asociaciones = True

            for id_palabra_clave, var in self.var_check_palabras_clave.items():
                documento_palabra_clave = DocumentoPalabraClave(
                    id_documento=id_documento, id_palabra_clave=id_palabra_clave
                )
                var.set(value=documento_palabra_clave.existe())

            self.cargando_asociaciones = False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos privados
    # └────────────────────────────────────────────────────────────┘

    def _cargar_documentos_seleccionados(self):
        for widget in self.frame_documentos.winfo_children():
            widget.destroy()

        if not hasattr(self, '_trace_documento_agregado'):
            self.var_radio_documento.trace_add(
                "write", lambda *args: self.on_documento_seleccionado()
            )
            self._trace_documento_agregado = True

        self._mostrar_documentos(self.documentos_seleccionados)

    def _mostrar_documentos(self, documentos: List[Documento]):
        for widget in self.frame_documentos.winfo_children():
            widget.destroy()

        if documentos:
            for documento in documentos:
                radio = Radiobutton(
                    self.frame_documentos,
                    text=documento.nombre,
                    variable=self.var_radio_documento,
                    value=documento.id,
                )
                radio.pack(anchor=W, padx=5, pady=2)

    def _filtrar_documentos(self):
        texto_busqueda = self.var_buscar_documentos.get().lower().strip()

        if not texto_busqueda:
            documentos_filtrados = self.documentos_seleccionados
        else:
            documentos_filtrados = [
                doc for doc in self.documentos_seleccionados if texto_busqueda in doc.nombre.lower()
            ]

        self._mostrar_documentos(documentos_filtrados)

    def _cargar_palabras_clave(self):
        for widget in self.frame_palabras_clave.winfo_children():
            widget.destroy()

        self.var_check_palabras_clave.clear()

        consulta = Consulta()
        if isinstance(consulta, Consulta):
            palabras_clave = consulta.get_palabras_clave()
            self.palabras_clave = palabras_clave
            self._mostrar_palabras_clave(palabras_clave)

    def _mostrar_palabras_clave(self, palabras_clave: List[PalabraClave]):
        for widget in self.frame_palabras_clave.winfo_children():
            widget.destroy()

        num_columnas = 4

        for i, palabra_clave in enumerate(palabras_clave):
            fila = i // num_columnas
            columna = i % num_columnas

            if palabra_clave.id not in self.var_check_palabras_clave:
                var = BooleanVar(value=False)
                var.trace_add('write', lambda *args: self.on_palabra_clave_seleccionado())
                self.var_check_palabras_clave[palabra_clave.id] = var
            else:
                var = self.var_check_palabras_clave[palabra_clave.id]

            check = Checkbutton(
                self.frame_palabras_clave,
                text=palabra_clave.palabra,
                variable=var,
            )
            check.grid(column=columna, row=fila, sticky=W, padx=5, pady=2)

    def _filtrar_palabras_clave(self):
        texto_busqueda = self.var_buscar_palabras_clave.get().lower().strip()

        if not texto_busqueda:
            palabras_clave_filtradas = self.palabras_clave
        else:
            palabras_clave_filtradas = [
                pc for pc in self.palabras_clave if texto_busqueda in pc.palabra.lower()
            ]

        self.cargando_asociaciones = True
        self._mostrar_palabras_clave(palabras_clave_filtradas)
        self.cargando_asociaciones = False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_documento_seleccionado(self):
        seleccionado = self.var_radio_documento.get()
        if seleccionado:
            self.cargar_asociaciones(id_documento=seleccionado)

    def on_palabra_clave_seleccionado(self):
        if self.cargando_asociaciones:
            return

        id_documento = self.var_radio_documento.get()
        if id_documento != 0:
            self.procesar_palabras_clave_seleccionadas(id_documento=id_documento)
        else:
            showinfo(
                parent=self, title="Seleccione", message="Seleccione un documento", icon='info'
            )

    def on_administrar_palabras_clave(self):
        dialog = DialogAdministrarPalabrasClave(master=self.master)
        self.master.wait_window(dialog)
