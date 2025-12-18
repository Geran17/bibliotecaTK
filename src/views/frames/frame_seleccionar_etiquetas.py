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
)
from ttkbootstrap.scrolled import ScrolledFrame
from models.entities.consulta import Consulta
from models.entities.etiqueta import Etiqueta
from models.entities.documento import Documento
from models.entities.documento_etiqueta import DocumentoEtiqueta
from ttkbootstrap.constants import *
from typing import List, Dict, Any


class FrameSeleccionarEtiquetas(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # variables
        self.var_buscar_documentos = StringVar()
        self.var_buscar_etiquetas = StringVar()
        # Variable ÚNICA para todos los radiobuttons
        self.var_radio_documento = IntVar(value=0)
        self.documentos_seleccionados: List[Documento] = []
        self.var_check_etiquetas: Dict[str, Any] = {}
        # Flag para controlar cuando estamos cargando
        self.cargando_asociaciones = False
        # Almacenar todas las etiquetas
        self.etiquetas: List[Etiqueta] = []

        # cargamos los widgets
        self.crear_widgets()
        # cargamos las etiquetas
        self._cargar_etiquetas()

        # Agregar traces para búsqueda
        self.var_buscar_documentos.trace_add('write', lambda *args: self._filtrar_documentos())
        self.var_buscar_etiquetas.trace_add('write', lambda *args: self._filtrar_etiquetas())

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘

    def crear_widgets(self):
        frame_superior = Frame(self, padding=(1, 1))
        self.panel_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=1, pady=1)

        frame_central = Frame(self, padding=(1, 1))
        self.panel_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)

        frame_inferior = Frame(self, padding=(1, 1))
        self.panel_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=1, pady=1)

    def panel_superior(self, frame: Frame):
        pass

    def panel_central(self, frame: Frame):

        paned_window = PanedWindow(frame, orient="vertical")
        paned_window.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)

        # --- Panel de Documentos ---
        container_documentos = LabelFrame(paned_window, text="Documentos", padding=5)
        paned_window.add(container_documentos)

        ent_buscar_documentos = Entry(container_documentos, textvariable=self.var_buscar_documentos)
        ent_buscar_documentos.pack(fill=X, padx=2, pady=(0, 5))

        self.frame_documentos = ScrolledFrame(container_documentos, padding=(1, 1))
        self.frame_documentos.pack(fill=BOTH, expand=True, padx=2, pady=2)

        # --- Panel de Etiquetas ---
        container_etiquetas = LabelFrame(paned_window, text="Etiquetas", padding=5)
        paned_window.add(container_etiquetas)

        ent_etiquetas = Entry(container_etiquetas, textvariable=self.var_buscar_etiquetas)
        ent_etiquetas.pack(fill=X, padx=2, pady=(0, 5))

        self.frame_etiquetas = ScrolledFrame(container_etiquetas, padding=(1, 1))
        self.frame_etiquetas.pack(fill=BOTH, expand=True, padx=2, pady=2)

    def panel_inferior(self, frame: Frame):
        pass

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos de la clase
    # └────────────────────────────────────────────────────────────┘

    def obtener_documentos_seleccionados(self, documetos_seleccionados: List[Documento]):
        if documetos_seleccionados:
            self.documentos_seleccionados = documetos_seleccionados
            self._cargar_documentos_seleccionados()

    def procesar_etiquetas_seleccionadas(self, id_documento):
        """Retorna una lista con los nombres de las etiquetas seleccionadas"""
        for id_etiqueta, var in self.var_check_etiquetas.items():
            documento_etiqueta = DocumentoEtiqueta(
                id_documento=id_documento, id_etiqueta=id_etiqueta
            )

            if not documento_etiqueta.existe():
                if var.get():
                    documento_etiqueta.asociar()

            if documento_etiqueta.existe():
                if not var.get():
                    documento_etiqueta.desasociar()

    def cargar_asociaciones(self, id_documento: int):
        """
        Esta funcion se encargara de establecer las etiquetas
        que estan asociadas al documento
        """
        if id_documento != 0:
            self.cargando_asociaciones = True

            for id_etiqueta, var in self.var_check_etiquetas.items():
                documento_etiqueta = DocumentoEtiqueta(
                    id_documento=id_documento, id_etiqueta=id_etiqueta
                )
                var.set(value=documento_etiqueta.existe())

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

    def _cargar_etiquetas(self):
        for widget in self.frame_etiquetas.winfo_children():
            widget.destroy()

        self.var_check_etiquetas.clear()

        consulta = Consulta()
        if isinstance(consulta, Consulta):
            etiquetas = consulta.get_etiquetas()
            self.etiquetas = etiquetas
            self._mostrar_etiquetas(etiquetas)

    def _mostrar_etiquetas(self, etiquetas: List[Etiqueta]):
        for widget in self.frame_etiquetas.winfo_children():
            widget.destroy()

        num_columnas = 4

        for i, etiqueta in enumerate(etiquetas):
            fila = i // num_columnas
            columna = i % num_columnas

            if etiqueta.id not in self.var_check_etiquetas:
                var = BooleanVar(value=False)
                var.trace_add('write', lambda *args: self.on_etiqueta_seleccionado())
                self.var_check_etiquetas[etiqueta.id] = var
            else:
                var = self.var_check_etiquetas[etiqueta.id]

            check = Checkbutton(
                self.frame_etiquetas,
                text=etiqueta.nombre,
                variable=var,
            )
            check.grid(column=columna, row=fila, sticky=W, padx=5, pady=2)

    def _filtrar_etiquetas(self):
        texto_busqueda = self.var_buscar_etiquetas.get().lower().strip()

        if not texto_busqueda:
            etiquetas_filtradas = self.etiquetas
        else:
            etiquetas_filtradas = [
                et for et in self.etiquetas if texto_busqueda in et.nombre.lower()
            ]

        self.cargando_asociaciones = True
        self._mostrar_etiquetas(etiquetas_filtradas)
        self.cargando_asociaciones = False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_documento_seleccionado(self):
        seleccionado = self.var_radio_documento.get()
        if seleccionado:
            self.cargar_asociaciones(id_documento=seleccionado)

    def on_etiqueta_seleccionado(self):
        if self.cargando_asociaciones:
            return

        id_documento = self.var_radio_documento.get()
        if id_documento != 0:
            self.procesar_etiquetas_seleccionadas(id_documento=id_documento)
        else:
            showinfo(
                parent=self, title="Seleccione", message="Seleccione un documento", icon='info'
            )
