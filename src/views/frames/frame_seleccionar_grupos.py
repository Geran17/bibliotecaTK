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
from models.entities.grupo import Grupo
from models.entities.documento import Documento
from models.entities.documento_grupo import DocumentoGrupo
from views.dialogs.dialog_administrar_grupo import DialogAdministrarGrupos
from ttkbootstrap.constants import *
from views.components.ui_tokens import PADDING_COMPACT, PADDING_OUTER, PADDING_PANEL
from typing import List, Dict, Any


class FrameSeleccionarGrupos(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # variables
        self.var_buscar_documentos = StringVar()
        self.var_buscar_grupos = StringVar()
        # Variable ÚNICA para todos los radiobuttons
        self.var_radio_documento = IntVar(value=0)
        self.documentos_seleccionados: List[Documento] = []
        self.var_check_grupos: Dict[str, Any] = {}
        # Flag para controlar cuando estamos cargando
        self.cargando_asociaciones = False
        # Almacenar todos los grupos
        self.grupos: List[Grupo] = []

        # cargamos los widgets
        self.crear_widgets()
        # cargamos los grupos
        self._cargar_grupos()

        # Agregar traces para búsqueda
        self.var_buscar_documentos.trace_add('write', lambda *args: self._filtrar_documentos())
        self.var_buscar_grupos.trace_add('write', lambda *args: self._filtrar_grupos())

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
        label_titulo = Label(
            frame, text="Asociar grupos a los documentos", font=("Helvetica", 12, "bold")
        )
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

        # --- Panel de Grupos ---
        container_grupos = LabelFrame(paned_window, text="Grupos", padding=PADDING_PANEL)
        paned_window.add(container_grupos)

        ent_grupos = Entry(container_grupos, textvariable=self.var_buscar_grupos)
        ent_grupos.pack(fill=X, padx=PADDING_PANEL, pady=(0, PADDING_OUTER))

        self.frame_grupos = ScrolledFrame(container_grupos, padding=(PADDING_COMPACT, PADDING_COMPACT))
        self.frame_grupos.pack(fill=BOTH, expand=True, padx=PADDING_PANEL, pady=PADDING_PANEL)

    def panel_inferior(self, frame: Frame):
        btn_administrar = Button(
            frame,
            text="Administrar Grupos",
            command=self.on_administrar_grupos,
            style="primary.Outline.TButton",
        )
        btn_administrar.pack(side=RIGHT, padx=PADDING_OUTER * 2, pady=PADDING_OUTER)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos de la clase
    # └────────────────────────────────────────────────────────────┘

    def obtener_documentos_seleccionados(self, documetos_seleccionados: List[Documento]):
        if documetos_seleccionados:
            self.documentos_seleccionados = documetos_seleccionados
            self._cargar_documentos_seleccionados()

    def procesar_grupos_seleccionados(self, id_documento):
        """Retorna una lista con los nombres de los grupos seleccionados"""
        for id_grupo, var in self.var_check_grupos.items():
            documento_grupo = DocumentoGrupo(id_documento=id_documento, id_grupo=id_grupo)

            # caso: en que no exista
            if not documento_grupo.existe():
                """Si no existe la relaccion y se seleccionado la asociamos"""
                if var.get():
                    documento_grupo.asociar()

            # caso: en existe
            if documento_grupo.existe():
                """Si existe la relaccion y se saco la seleccion lo desasociamos"""
                if not var.get():
                    documento_grupo.desasociar()

    def cargar_asociaciones(self, id_documento: int):
        """
        Esta funcion se encargara de establecer los grupos
        que estan asociadas al documento
        """
        if id_documento != 0:
            # Activar flag para evitar que el trace procese cambios
            self.cargando_asociaciones = True

            # Cargar las asociaciones correctamente para TODOS los grupos
            # No solo los visibles, sino todos los que existen
            for id_grupo, var in self.var_check_grupos.items():
                documento_grupo = DocumentoGrupo(id_documento=id_documento, id_grupo=id_grupo)
                # Establecer el valor según exista o no la asociación
                var.set(value=documento_grupo.existe())

            # Desactivar flag después de cargar
            self.cargando_asociaciones = False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos privados
    # └────────────────────────────────────────────────────────────┘

    def _cargar_documentos_seleccionados(self):
        # Limpiar radiobuttons anteriores si existen
        for widget in self.frame_documentos.winfo_children():
            widget.destroy()

        # Agregar trace para detectar cambios (solo una vez)
        if not hasattr(self, '_trace_documento_agregado'):
            self.var_radio_documento.trace_add(
                "write", lambda *args: self.on_documento_seleccionado()
            )
            self._trace_documento_agregado = True

        # Aplicar filtro si hay texto en búsqueda
        self._mostrar_documentos(self.documentos_seleccionados)

    def _mostrar_documentos(self, documentos: List[Documento]):
        """Muestra los documentos en la lista"""
        # Limpiar widgets existentes
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
        """Filtra los documentos según el texto de búsqueda"""
        texto_busqueda = self.var_buscar_documentos.get().lower().strip()

        if not texto_busqueda:
            # Si no hay texto, mostrar todos
            documentos_filtrados = self.documentos_seleccionados
        else:
            # Filtrar documentos que contengan el texto
            documentos_filtrados = [
                doc for doc in self.documentos_seleccionados if texto_busqueda in doc.nombre.lower()
            ]

        self._mostrar_documentos(documentos_filtrados)

    def _cargar_grupos(self):
        # Para ScrolledFrame, usa .winfo_children() en el frame interno
        for widget in self.frame_grupos.winfo_children():
            widget.destroy()

        # Limpiar el diccionario
        self.var_check_grupos.clear()

        # Hacemos una consulta para obtener el total de los grupos
        consulta = Consulta()
        if isinstance(consulta, Consulta):
            grupos = consulta.get_grupos()

            # Guardar referencia a los grupos
            self.grupos = grupos

            # Aplicar filtro si hay texto en búsqueda
            self._mostrar_grupos(grupos)

    def _mostrar_grupos(self, grupos: List[Grupo]):
        """Muestra los grupos en el grid"""
        # Limpiar widgets existentes
        for widget in self.frame_grupos.winfo_children():
            widget.destroy()

        # Configurar grid en 4 columnas
        num_columnas = 4

        for i, grupo in enumerate(grupos):
            # Calcular fila y columna
            fila = i // num_columnas
            columna = i % num_columnas

            # Crear o reutilizar variable si ya existe
            if grupo.id not in self.var_check_grupos:
                var = BooleanVar(value=False)
                var.trace_add('write', lambda *args: self.on_grupo_seleccionado())
                self.var_check_grupos[grupo.id] = var
            else:
                var = self.var_check_grupos[grupo.id]

            # Cargamos los check
            check = Checkbutton(
                self.frame_grupos,
                text=grupo.nombre,
                variable=var,
            )
            check.grid(column=columna, row=fila, sticky=W, padx=5, pady=2)

    def _filtrar_grupos(self):
        """Filtra los grupos según el texto de búsqueda"""
        texto_busqueda = self.var_buscar_grupos.get().lower().strip()

        if not texto_busqueda:
            # Si no hay texto, mostrar todos
            grupos_filtrados = self.grupos
        else:
            # Filtrar grupos que contengan el texto
            grupos_filtrados = [g for g in self.grupos if texto_busqueda in g.nombre.lower()]

        # Activar flag para evitar procesamiento durante redibujado
        self.cargando_asociaciones = True
        self._mostrar_grupos(grupos_filtrados)
        self.cargando_asociaciones = False

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_documento_seleccionado(self):
        """Detecta cualquier cambio en la selección"""
        seleccionado = self.var_radio_documento.get()
        if seleccionado:
            self.cargar_asociaciones(id_documento=seleccionado)

    def on_grupo_seleccionado(self):
        """Detecta cambios en los grupos seleccionados"""
        # Ignorar si estamos cargando asociaciones
        if self.cargando_asociaciones:
            return

        # verificamos que se halla seleccionado un libro o documento
        id_documento = self.var_radio_documento.get()
        if id_documento != 0:
            self.procesar_grupos_seleccionados(id_documento=id_documento)
        else:
            showinfo(
                parent=self, title="Seleccione", message="Seleccione un documentos", icon='info'
            )

    def on_administrar_grupos(self):
        dialog = DialogAdministrarGrupos(master=self.master)
        self.master.wait_window(dialog)
