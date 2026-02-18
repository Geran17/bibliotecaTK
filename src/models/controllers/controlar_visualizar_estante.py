import os
import math
import threading
from typing import Dict, Any, List, Optional, Callable
from ttkbootstrap import Frame, StringVar, Entry, Combobox, Button, Label, Separator
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
from tkinter import Menu
from ttkbootstrap.tooltip import ToolTip
from PIL import Image, ImageTk

from models.entities.consulta import Consulta
from models.entities.favorito import Favorito
from models.entities.documento import Documento
from models.controllers.configuracion_controller import ConfiguracionController
from models.controllers.controlar_comentarios import ControlarComentarios
from models.controllers.controlar_menu_contextual_documento import (
    ControlarMenuContextualDocumento,
)
from utilities.auxiliar import (
    crear_directorio_id_documento,
    abrir_archivo,
    generar_ruta_documento,
    copiar_archivo,
)
from utilities.configuracion import DIRECTORIO_TEMPORAL
from views.components.resizable_input_dialog import ask_resizable_string
from views.components.resizable_text_dialog import ask_resizable_text
from views.dialogs.dialog_visualizar_metadatos import DialogVisualizarMetadatos
from ttkbootstrap.constants import *

ANCHO_PORTADA = 100
ANCHO_PORTADA_LISTA = 56
ALTO_PORTADA_LISTA = 84
PORTADAS_POR_REPISA = 8
DOCUMENTOS_POR_PAGINA = 40  # Número de documentos por página


class ControlarVisualizarEstante:
    """
    Controlador para la lógica de visualización y búsqueda en el estante.
    """

    MAPA_CAMPO_UI_A_DB = {
        "Título": "titulo",
        "Autores": "autores",
        "Editorial": "editorial",
        "ISBN": "isbn",
        "Colección": "coleccion",
        "Grupo": "grupo",
        "Nombre": "nombre",
        "Todo": "todo",
    }
    MAPA_CAMPO_DB_A_UI = {valor: clave for clave, valor in MAPA_CAMPO_UI_A_DB.items()}
    MAPA_MODO_UI_A_INTERNO = {
        "Cuadrícula": "cuadricula",
        "Lista": "lista",
    }
    MAPA_MODO_INTERNO_A_UI = {valor: clave for clave, valor in MAPA_MODO_UI_A_INTERNO.items()}
    MAPA_TIPO_ORG_UI_A_KEY = {
        "Colecciones": "coleccion",
        "Grupos": "grupo",
        "Categorías": "categoria",
        "Etiquetas": "etiqueta",
        "Palabras Clave": "palabra_clave",
    }
    MAPA_TIPO_ORG_KEY_A_UI = {valor: clave for clave, valor in MAPA_TIPO_ORG_UI_A_KEY.items()}

    def __init__(
        self,
        master: Frame,
        map_widgets: Dict[str, Any],
        map_vars: Dict[str, Any],
        map_documentos: Dict[str, Any],
        scroll_frame: ScrolledFrame,
    ):
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars
        self.map_documentos = map_documentos
        self.scroll_frame = scroll_frame
        self.config = ConfiguracionController()
        self.consulta = Consulta()

        # Acceso a los widgets
        self.ent_buscar: Entry = self.map_widgets["ent_buscar"]
        self.cbx_campos: Combobox = self.map_widgets["cbx_campos"]
        self.cbx_modo_visualizacion: Combobox = self.map_widgets.get("cbx_modo_visualizacion")
        self.btn_buscar: Button = self.map_widgets["btn_buscar"]
        self.btn_anterior: Button = self.map_widgets.get("btn_anterior")
        self.btn_siguiente: Button = self.map_widgets.get("btn_siguiente")
        self.lbl_pagina: Label = self.map_widgets.get("lbl_pagina")
        self.cbx_tipo_organizacion: Optional[Combobox] = self.map_widgets.get(
            "cbx_tipo_organizacion"
        )
        self.cbx_organizacion: Optional[Combobox] = self.map_widgets.get("cbx_organizacion")

        # Acceso a las variables
        self.var_buscar: StringVar = self.map_vars["var_buscar"]
        self.var_modo_visualizacion: StringVar = self.map_vars.get("var_modo_visualizacion")
        self.var_tipo_organizacion: Optional[StringVar] = self.map_vars.get("var_tipo_organizacion")
        self.var_organizacion: Optional[StringVar] = self.map_vars.get("var_organizacion")
        if self.var_modo_visualizacion is None:
            self.var_modo_visualizacion = StringVar(value="Cuadrícula")

        # Variables de paginación
        self.pagina_actual = 1
        self.total_documentos = 0
        self.campo_busqueda_actual = ""
        self.termino_busqueda_actual = ""
        self.modo_visualizacion_actual = "cuadricula"
        self.tipo_organizacion_actual: Optional[str] = None
        self.id_organizacion_actual: Optional[int] = None
        self.nombre_organizacion_actual: str = ""
        self.documentos_organizacion: List[Dict[str, Any]] = []
        self.documentos_filtrados_organizacion: List[Dict[str, Any]] = []
        self.tipo_organizacion_seleccionado: Optional[str] = None
        self.map_organizaciones: Dict[str, int] = {}
        self._map_organizacion_getters: Dict[str, Callable[[], List[Any]]] = {
            "coleccion": self.consulta.get_colecciones,
            "grupo": self.consulta.get_grupos,
            "categoria": self.consulta.get_categorias,
            "etiqueta": self.consulta.get_etiquetas,
            "palabra_clave": self.consulta.get_palabras_clave,
        }
        self._map_documentos_getters: Dict[str, Callable[[int], List[Dict[str, Any]]]] = {
            "coleccion": self.consulta.get_documentos_por_coleccion,
            "grupo": self.consulta.get_documentos_por_grupo,
            "categoria": self.consulta.get_documentos_por_categoria,
            "etiqueta": self.consulta.get_documentos_por_etiqueta,
            "palabra_clave": self.consulta.get_documentos_por_palabra_clave,
        }

        # Almacenamiento de referencias de imágenes para evitar que el recolector de basura las elimine
        self._referencias_imagenes = []
        self.documento_seleccionado_contextual = None
        self.progresos_lectura = self.config.obtener_progresos_lectura()
        self._depurar_progresos_lectura_huerfanos()
        self.comentarios = ControlarComentarios()
        self._comentarios_ids = set()
        self.menu_ops = ControlarMenuContextualDocumento(
            master=self.master,
            get_documento_data=self._get_documento_contextual,
            on_refresh=self.recargar_estante,
        )

        self._crear_menu_contextual()
        self._vincular_eventos()
        self._inicializar_estado_estante()

    def _crear_menu_contextual(self):
        """Crea el menú contextual para las portadas."""
        self.menu_contextual = Menu(self.master, tearoff=0)
        self.menu_contextual.add_command(
            label="📖 Abrir documento", command=self._on_abrir_documento_contextual
        )
        self.menu_contextual.add_command(
            label="📂 Abrir carpeta", command=self.menu_ops.on_abrir_carpeta
        )
        self.menu_contextual.add_command(
            label="ℹ️ Propiedades", command=self.menu_ops.on_propiedades
        )
        self.menu_contextual.add_command(
            label="🧾 Ver metadatos", command=self.menu_ops.on_ver_metadatos
        )
        self.menu_contextual.add_command(
            label="📝 Comentario", command=self._on_comentario_contextual
        )
        self.menu_index_comentario = self.menu_contextual.index("end")
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(
            label="✏️ Renombrar documento", command=self.menu_ops.on_renombrar_documento
        )
        self.menu_contextual.add_command(
            label="🧬 Renombrar bibliográficamente", command=self.menu_ops.on_renombrar_bibliografico
        )
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(
            label="📋 Copiar documento", command=self.menu_ops.on_copiar_documento
        )
        self.menu_contextual.add_command(
            label="✂️ Mover documento", command=self.menu_ops.on_mover_documento
        )
        self.menu_contextual.add_command(
            label="🗑️ Enviar a papelera", command=self.menu_ops.on_enviar_papelera
        )
        self.menu_contextual.add_command(
            label="🗑️ Eliminar documento", command=self.menu_ops.on_eliminar_documento
        )
        self.menu_contextual.add_command(
            label="🔄 Cambiar estado", command=self.menu_ops.on_cambiar_estado
        )
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(
            label="ℹ️ Ver detalles", command=self._on_ver_detalles_contextual
        )
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(
            label="📘 Registrar progreso de lectura",
            command=self._on_registrar_progreso_lectura_contextual,
        )
        self.menu_index_progreso = self.menu_contextual.index("end")
        self.menu_contextual.add_command(
            label="🧹 Quitar progreso de lectura",
            command=self._on_quitar_progreso_lectura_contextual,
        )
        self.menu_index_quitar_progreso = self.menu_contextual.index("end")
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(
            label="⭐ Marcar como favorito",  # El texto se actualizará dinámicamente
            command=self._on_marcar_favorito_contextual,
        )
        self.menu_index_favorito = self.menu_contextual.index("end")

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a los métodos del controlador."""
        self.btn_buscar.config(command=self.on_buscar)
        self.ent_buscar.bind("<Return>", self.on_buscar)
        if self.cbx_modo_visualizacion:
            self.cbx_modo_visualizacion.bind(
                "<<ComboboxSelected>>", self.on_cambiar_modo_visualizacion
            )
        if self.cbx_tipo_organizacion:
            self.cbx_tipo_organizacion.bind(
                "<<ComboboxSelected>>", self.on_cambiar_tipo_organizacion
            )
        if self.cbx_organizacion:
            self.cbx_organizacion.bind("<<ComboboxSelected>>", self.on_seleccionar_organizacion)
        if self.btn_anterior:
            self.btn_anterior.config(command=self.on_pagina_anterior)
        if self.btn_siguiente:
            self.btn_siguiente.config(command=self.on_pagina_siguiente)

    def _cargar_estante(self):
        """Inicializa el estante mostrando el catálogo completo paginado."""
        self._limpiar_filtro_organizacion(limpiar_ui=True)
        self.campo_busqueda_actual = "todo"
        self.termino_busqueda_actual = ""
        self.pagina_actual = 1
        self._guardar_estado_busqueda_estante(campo_db="todo", termino_busqueda="")
        self.total_documentos = self.consulta.contar_resultados_busqueda(campo="todo", termino="")
        self._mostrar_pagina_actual()

    def on_buscar(self, event=None):
        """Maneja el evento de búsqueda."""
        termino_busqueda = self.var_buscar.get().strip()
        campo_seleccionado = self.cbx_campos.get()
        campo_db = self.MAPA_CAMPO_UI_A_DB.get(campo_seleccionado, "todo")

        if not termino_busqueda:
            self.termino_busqueda_actual = ""
            self.campo_busqueda_actual = campo_db
            if self._tiene_filtro_organizacion():
                self._recargar_filtro_organizacion()
                return
            self._cargar_estante()
            return

        self._aplicar_busqueda(campo_db=campo_db, termino_busqueda=termino_busqueda)

    def _aplicar_busqueda(self, campo_db: str, termino_busqueda: str):
        """Aplica búsqueda, actualiza paginación y persiste el estado."""
        self.campo_busqueda_actual = campo_db
        self.termino_busqueda_actual = termino_busqueda
        self.pagina_actual = 1
        if self._tiene_filtro_organizacion():
            self._actualizar_documentos_filtrados_organizacion()
            self._guardar_estado_busqueda_estante(
                campo_db=campo_db,
                termino_busqueda=termino_busqueda,
            )
            self._mostrar_pagina_actual()
            return

        self.total_documentos = self.consulta.contar_resultados_busqueda(
            campo=campo_db, termino=termino_busqueda
        )
        self._guardar_estado_busqueda_estante(
            campo_db=campo_db,
            termino_busqueda=termino_busqueda,
        )
        self._mostrar_pagina_actual()

    def _guardar_estado_busqueda_estante(self, campo_db: str, termino_busqueda: str):
        modo_visualizacion = self._normalizar_modo_visualizacion(self.modo_visualizacion_actual)
        estado = {
            "campo": (campo_db or "todo").strip().lower(),
            "termino": (termino_busqueda or "").strip(),
            "modo_visualizacion": modo_visualizacion,
            "tipo_organizacion": self.tipo_organizacion_actual,
            "id_organizacion": self.id_organizacion_actual,
            "nombre_organizacion": (self.nombre_organizacion_actual or "").strip(),
        }
        self.config.guardar_estado_vista_estante(estado=estado)

    def _inicializar_estado_estante(self):
        """Restaura la última búsqueda guardada y carga el estante automáticamente."""
        estado = self.config.obtener_estado_vista_estante()
        if not isinstance(estado, dict):
            self._cargar_estante()
            return

        tipo_org = (estado.get("tipo_organizacion") or "").strip()
        id_org = estado.get("id_organizacion")
        nombre_org = (estado.get("nombre_organizacion") or "").strip()

        campo_db = (estado.get("campo") or "todo").strip().lower()
        termino_busqueda = (estado.get("termino") or "").strip()
        self.modo_visualizacion_actual = self._normalizar_modo_visualizacion(
            estado.get("modo_visualizacion")
        )
        modo_ui = self.MAPA_MODO_INTERNO_A_UI[self.modo_visualizacion_actual]
        self.var_modo_visualizacion.set(modo_ui)
        if self.cbx_modo_visualizacion:
            self.cbx_modo_visualizacion.set(modo_ui)

        if campo_db not in self.MAPA_CAMPO_DB_A_UI:
            campo_db = "todo"

        campo_ui = self.MAPA_CAMPO_DB_A_UI.get(campo_db, "Todo")
        self.cbx_campos.set(campo_ui)
        self.var_buscar.set(termino_busqueda)
        self.campo_busqueda_actual = campo_db
        self.termino_busqueda_actual = termino_busqueda

        if tipo_org and id_org is not None:
            try:
                id_org = int(id_org)
            except (TypeError, ValueError):
                id_org = None

        if tipo_org and id_org is not None:
            self._restaurar_filtro_organizacion(
                tipo_key=tipo_org,
                id_org=id_org,
                nombre_ui=nombre_org,
            )
            if self._tiene_filtro_organizacion():
                return

        if not termino_busqueda:
            self._cargar_estante()
            return

        self._aplicar_busqueda(campo_db=campo_db, termino_busqueda=termino_busqueda)

    def _normalizar_modo_visualizacion(self, modo_visualizacion: str) -> str:
        modo = (modo_visualizacion or "").strip().lower()
        if modo in self.MAPA_MODO_INTERNO_A_UI:
            return modo
        return "cuadricula"

    def on_cambiar_modo_visualizacion(self, event=None):
        modo_ui = self.var_modo_visualizacion.get()
        modo_nuevo = self.MAPA_MODO_UI_A_INTERNO.get(modo_ui, "cuadricula")
        modo_nuevo = self._normalizar_modo_visualizacion(modo_nuevo)

        if modo_nuevo == self.modo_visualizacion_actual:
            return

        self.modo_visualizacion_actual = modo_nuevo
        self._guardar_estado_busqueda_estante(
            campo_db=self.campo_busqueda_actual or "todo",
            termino_busqueda=self.termino_busqueda_actual,
        )

        if self.campo_busqueda_actual:
            self._mostrar_pagina_actual()
        else:
            self._cargar_estante()

    def _mostrar_documentos_en_estante(self, lista_documentos):
        """
        Renderiza los documentos en el ScrolledFrame según el modo de visualización.
        """
        self._limpiar_estante_visual()
        self._comentarios_ids = set(self.comentarios.obtener_comentarios().keys())

        if not lista_documentos:
            Label(self.scroll_frame, text="No se encontraron documentos.", bootstyle="secondary").pack(
                pady=20
            )
            return

        if self.modo_visualizacion_actual == "lista":
            self._mostrar_documentos_lista(lista_documentos)
        else:
            self._mostrar_documentos_cuadricula(lista_documentos)

    def _limpiar_estante_visual(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self._referencias_imagenes.clear()

    def _mostrar_documentos_cuadricula(self, lista_documentos):
        ruta_portadas = self.config.obtener_ubicacion_portadas()

        # Contenedor principal dentro del ScrolledFrame
        main_container = Frame(self.scroll_frame)
        main_container.pack(fill=X, padx=10, pady=10)

        repisa_actual = None
        tareas_carga = []

        for i, doc in enumerate(lista_documentos):
            # Crear una nueva repisa cada N portadas
            if i % PORTADAS_POR_REPISA == 0:
                repisa_actual = Frame(main_container)
                repisa_actual.pack(fill=X, pady=10)
                Separator(main_container, bootstyle="secondary").pack(fill=X, padx=20)

            id_documento = doc["id"]
            nombre_documento = doc["nombre"]
            if str(id_documento) in self._comentarios_ids:
                nombre_documento = f"📝 {nombre_documento}"

            # Crear un frame para cada portada y su etiqueta
            frame_portada = Frame(repisa_actual)
            frame_portada.pack(side=LEFT, anchor=N, padx=10, pady=10)

            # --- Tooltip ---
            nombre = doc.get("nombre", "N/A")
            titulo = doc.get("titulo")  # Será None si no existe
            paginas = doc.get("numero_paginas")
            tamano_bytes = doc.get("tamano", 0)
            tamano_str = self._formatear_tamano(tamano_bytes)
            progreso_texto = self._construir_texto_progreso_documento(doc)
            tooltip_text = self._construir_tooltip_documento(
                nombre=nombre,
                titulo=titulo,
                paginas=paginas,
                tamano_str=tamano_str,
                progreso_texto=progreso_texto,
            )
            ToolTip(frame_portada, text=tooltip_text, bootstyle=(INFO, INVERSE))

            ruta_portada_miniatura = os.path.join(
                crear_directorio_id_documento(ruta_portadas, id_documento),
                f"{id_documento}_miniatura.png",
            )

            # Placeholder inicial mientras carga
            lbl_imagen = Label(frame_portada, text="⌛", font=("Helvetica", 16))

            # Añadir a la lista de tareas para el hilo
            tareas_carga.append(
                (ruta_portada_miniatura, lbl_imagen, ANCHO_PORTADA, int(ANCHO_PORTADA * 1.5))
            )

            lbl_imagen.pack(pady=(0, 5))

            lbl_nombre = Label(
                frame_portada,
                text=nombre_documento,
                bootstyle="secondary",
                wraplength=ANCHO_PORTADA,  # Ajustar texto al ancho de la portada
                justify=CENTER,
            )
            lbl_nombre.pack()

            texto_progreso_corto = self._construir_texto_progreso_resumido(doc)
            lbl_progreso = None
            if texto_progreso_corto:
                lbl_progreso = Label(
                    frame_portada,
                    text=texto_progreso_corto,
                    bootstyle="success",
                    font=("TkFixedFont", 7),
                    wraplength=0,
                    justify=CENTER,
                )
                lbl_progreso.pack(pady=(3, 0))

            # --- Vinculación de eventos ---
            # Usamos una función lambda para pasar el documento específico al manejador
            handler_contextual = lambda event, d=doc: self._mostrar_menu_contextual(event, d)
            frame_portada.bind("<Button-3>", handler_contextual)
            lbl_imagen.bind("<Button-3>", handler_contextual)
            lbl_nombre.bind("<Button-3>", handler_contextual)
            if lbl_progreso:
                lbl_progreso.bind("<Button-3>", handler_contextual)

            # Doble clic para abrir el documento
            handler_abrir = lambda event, d=doc: self._abrir_documento(d)
            frame_portada.bind("<Double-1>", handler_abrir)
            lbl_imagen.bind("<Double-1>", handler_abrir)
            lbl_nombre.bind("<Double-1>", handler_abrir)
            if lbl_progreso:
                lbl_progreso.bind("<Double-1>", handler_abrir)

        # Iniciar hilo de carga
        threading.Thread(
            target=self._procesar_carga_imagenes, args=(tareas_carga,), daemon=True
        ).start()

    def _mostrar_documentos_lista(self, lista_documentos):
        ruta_portadas = self.config.obtener_ubicacion_portadas()

        main_container = Frame(self.scroll_frame)
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tareas_carga = []

        for doc in lista_documentos:
            id_documento = doc["id"]
            nombre_documento = doc["nombre"]
            if str(id_documento) in self._comentarios_ids:
                nombre_documento = f"📝 {nombre_documento}"

            fila = Frame(main_container, padding=(8, 8))
            fila.pack(fill=X, padx=4, pady=(0, 4))

            lbl_imagen = Label(fila, text="⌛", font=("Helvetica", 14), width=6)
            lbl_imagen.pack(side=LEFT, padx=(0, 10))

            frame_info = Frame(fila)
            frame_info.pack(side=LEFT, fill=X, expand=True)

            lbl_nombre = Label(
                frame_info,
                text=nombre_documento,
                bootstyle="secondary",
                anchor=W,
                justify=LEFT,
            )
            lbl_nombre.pack(fill=X)

            lbl_detalle = Label(
                frame_info,
                text=self._construir_detalle_lista_documento(doc),
                bootstyle="secondary",
                anchor=W,
                justify=LEFT,
                wraplength=900,
            )
            lbl_detalle.pack(fill=X, pady=(4, 0))
            texto_progreso = self._construir_texto_progreso_resumido(doc)
            if texto_progreso:
                lbl_progreso = Label(
                    frame_info,
                    text=texto_progreso,
                    bootstyle="success",
                    anchor=W,
                    justify=LEFT,
                    font=("TkFixedFont", 8),
                )
                lbl_progreso.pack(fill=X, pady=(2, 0))

            nombre = doc.get("nombre", "N/A")
            titulo = doc.get("titulo")
            paginas = doc.get("numero_paginas")
            tamano_str = self._formatear_tamano(doc.get("tamano", 0))
            progreso_texto = self._construir_texto_progreso_documento(doc)
            tooltip_text = self._construir_tooltip_documento(
                nombre=nombre,
                titulo=titulo,
                paginas=paginas,
                tamano_str=tamano_str,
                progreso_texto=progreso_texto,
            )
            ToolTip(fila, text=tooltip_text, bootstyle=(INFO, INVERSE))

            ruta_portada_miniatura = os.path.join(
                crear_directorio_id_documento(ruta_portadas, id_documento),
                f"{id_documento}_miniatura.png",
            )
            tareas_carga.append(
                (
                    ruta_portada_miniatura,
                    lbl_imagen,
                    ANCHO_PORTADA_LISTA,
                    ALTO_PORTADA_LISTA,
                )
            )

            handler_contextual = lambda event, d=doc: self._mostrar_menu_contextual(event, d)
            handler_abrir = lambda event, d=doc: self._abrir_documento(d)
            widgets_evento = [fila, lbl_imagen, frame_info, lbl_nombre, lbl_detalle]
            if texto_progreso:
                widgets_evento.append(lbl_progreso)
            for widget in widgets_evento:
                widget.bind("<Button-3>", handler_contextual)
                widget.bind("<Double-1>", handler_abrir)

            Separator(main_container, bootstyle="secondary").pack(fill=X, padx=6, pady=(2, 8))

        threading.Thread(
            target=self._procesar_carga_imagenes, args=(tareas_carga,), daemon=True
        ).start()

    def _mostrar_pagina_actual(self):
        """Muestra la página actual de documentos."""
        if self._tiene_filtro_organizacion():
            offset = (self.pagina_actual - 1) * DOCUMENTOS_POR_PAGINA
            documentos_pagina = self.documentos_filtrados_organizacion[
                offset : offset + DOCUMENTOS_POR_PAGINA
            ]
            self._mostrar_documentos_en_estante(documentos_pagina)
            self._actualizar_controles_paginacion()
            return

        if not self.campo_busqueda_actual:
            self._cargar_estante()
            return
        offset = (self.pagina_actual - 1) * DOCUMENTOS_POR_PAGINA
        documentos_pagina = self.consulta.buscar_en_estante(
            campo=self.campo_busqueda_actual,
            termino=self.termino_busqueda_actual,
            limit=DOCUMENTOS_POR_PAGINA,
            offset=offset,
        )
        self._mostrar_documentos_en_estante(documentos_pagina)
        self._actualizar_controles_paginacion()

    def _actualizar_controles_paginacion(self):
        """Actualiza los controles de paginación."""
        total_paginas = (self.total_documentos + DOCUMENTOS_POR_PAGINA - 1) // DOCUMENTOS_POR_PAGINA
        total_paginas = max(1, total_paginas)
        if self.lbl_pagina:
            self.lbl_pagina.config(text=f"Página {self.pagina_actual} de {total_paginas}")
        if self.btn_anterior:
            self.btn_anterior.config(state=NORMAL if self.pagina_actual > 1 else DISABLED)
        if self.btn_siguiente:
            self.btn_siguiente.config(
                state=NORMAL if self.pagina_actual < total_paginas else DISABLED
            )

    def on_pagina_anterior(self):
        """Navega a la página anterior."""
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self._mostrar_pagina_actual()

    def on_pagina_siguiente(self):
        """Navega a la página siguiente."""
        total_paginas = (self.total_documentos + DOCUMENTOS_POR_PAGINA - 1) // DOCUMENTOS_POR_PAGINA
        if self.pagina_actual < total_paginas:
            self.pagina_actual += 1
            self._mostrar_pagina_actual()

    def recargar_estante(self):
        """
        Refresca el estado visual del estante.
        Si hay una búsqueda activa, recarga la página actual.
        """
        self.progresos_lectura = self.config.obtener_progresos_lectura()
        if self._tiene_filtro_organizacion():
            self._recargar_filtro_organizacion()
            return
        if self.termino_busqueda_actual:
            self._mostrar_pagina_actual()
            return

        self.pagina_actual = 1
        self.total_documentos = 0
        self._cargar_estante()
        self._actualizar_controles_paginacion()

    def _tiene_filtro_organizacion(self) -> bool:
        return bool(self.tipo_organizacion_actual and self.id_organizacion_actual is not None)

    def _limpiar_filtro_organizacion(self, limpiar_ui: bool = False):
        self.tipo_organizacion_actual = None
        self.id_organizacion_actual = None
        self.nombre_organizacion_actual = ""
        self.documentos_organizacion = []
        self.documentos_filtrados_organizacion = []
        if limpiar_ui:
            self.tipo_organizacion_seleccionado = None
            self.map_organizaciones = {}
            if self.var_tipo_organizacion:
                self.var_tipo_organizacion.set("")
            if self.var_organizacion:
                self.var_organizacion.set("")
            if self.cbx_tipo_organizacion:
                self.cbx_tipo_organizacion.set("")
            if self.cbx_organizacion:
                self.cbx_organizacion.set("")
                self.cbx_organizacion.config(values=[], state=DISABLED)

    def on_cambiar_tipo_organizacion(self, event=None):
        if not self.cbx_tipo_organizacion:
            return
        tipo_ui = (
            self.var_tipo_organizacion.get().strip()
            if self.var_tipo_organizacion
            else self.cbx_tipo_organizacion.get().strip()
        )
        tipo_key = self.MAPA_TIPO_ORG_UI_A_KEY.get(tipo_ui)
        self.tipo_organizacion_seleccionado = tipo_key
        self._limpiar_filtro_organizacion(limpiar_ui=False)
        self._cargar_organizaciones_en_combo(tipo_key=tipo_key)

    def _cargar_organizaciones_en_combo(self, tipo_key: Optional[str]):
        if not self.cbx_organizacion:
            return
        if not tipo_key or tipo_key not in self._map_organizacion_getters:
            self.cbx_organizacion.config(values=[], state=DISABLED)
            if self.var_organizacion:
                self.var_organizacion.set("")
            self.cbx_organizacion.set("")
            return

        organizaciones = self._map_organizacion_getters[tipo_key]()
        valores = self._construir_valores_organizacion(organizaciones)
        if valores:
            self.cbx_organizacion.config(values=valores, state=READONLY)
        else:
            self.cbx_organizacion.config(values=[], state=DISABLED)
        if self.var_organizacion:
            self.var_organizacion.set("")
        self.cbx_organizacion.set("")

    def _construir_valores_organizacion(self, organizaciones: List[Any]) -> List[str]:
        nombres: List[str] = []
        items: List[Dict[str, Any]] = []
        for org in organizaciones:
            nombre = self._obtener_nombre_organizacion(org)
            if not nombre:
                continue
            try:
                id_org = int(getattr(org, "id", None))
            except (TypeError, ValueError):
                continue
            nombres.append(nombre)
            items.append({"nombre": nombre, "id": id_org})

        if not items:
            self.map_organizaciones = {}
            return []

        conteos: Dict[str, int] = {}
        for nombre in nombres:
            conteos[nombre] = conteos.get(nombre, 0) + 1

        items.sort(key=lambda x: x["nombre"].lower())
        valores: List[str] = []
        self.map_organizaciones = {}
        for item in items:
            nombre = item["nombre"]
            id_org = item["id"]
            if conteos.get(nombre, 0) > 1:
                display = f"{nombre} (ID {id_org})"
            else:
                display = nombre
            self.map_organizaciones[display] = id_org
            valores.append(display)
        return valores

    def _obtener_nombre_organizacion(self, org: Any) -> str:
        if hasattr(org, "nombre"):
            return (getattr(org, "nombre") or "").strip()
        if hasattr(org, "palabra"):
            return (getattr(org, "palabra") or "").strip()
        return ""

    def on_seleccionar_organizacion(self, event=None):
        if not self.cbx_organizacion:
            return
        if not self.tipo_organizacion_seleccionado:
            return
        seleccion = (
            self.var_organizacion.get().strip()
            if self.var_organizacion
            else self.cbx_organizacion.get().strip()
        )
        if not seleccion:
            return

        id_org = self.map_organizaciones.get(seleccion)
        if id_org is None:
            return

        self._aplicar_filtro_organizacion(
            tipo_key=self.tipo_organizacion_seleccionado,
            id_org=id_org,
            nombre_ui=seleccion,
        )

    def _limpiar_busqueda(self):
        self.var_buscar.set("")
        self.cbx_campos.set("Todo")
        self.campo_busqueda_actual = "todo"
        self.termino_busqueda_actual = ""

    def _aplicar_filtro_organizacion(self, tipo_key: str, id_org: int, nombre_ui: str = ""):
        if tipo_key not in self._map_documentos_getters:
            return
        self.progresos_lectura = self.config.obtener_progresos_lectura()
        documentos = self._map_documentos_getters[tipo_key](id_org)
        self.documentos_organizacion = documentos or []
        self.pagina_actual = 1
        self.tipo_organizacion_actual = tipo_key
        self.id_organizacion_actual = id_org
        self.nombre_organizacion_actual = nombre_ui or ""
        self._actualizar_documentos_filtrados_organizacion()
        self._guardar_estado_busqueda_estante(
            campo_db=self.campo_busqueda_actual or "todo",
            termino_busqueda=self.termino_busqueda_actual,
        )
        self._mostrar_pagina_actual()

    def _recargar_filtro_organizacion(self):
        if not self._tiene_filtro_organizacion():
            return
        self._aplicar_filtro_organizacion(
            tipo_key=self.tipo_organizacion_actual,
            id_org=self.id_organizacion_actual,
            nombre_ui=self.nombre_organizacion_actual,
        )

    def _restaurar_filtro_organizacion(self, tipo_key: str, id_org: int, nombre_ui: str):
        if not self.cbx_tipo_organizacion or not self.cbx_organizacion:
            return
        tipo_ui = self.MAPA_TIPO_ORG_KEY_A_UI.get(tipo_key)
        if not tipo_ui:
            return
        if self.var_tipo_organizacion:
            self.var_tipo_organizacion.set(tipo_ui)
        self.cbx_tipo_organizacion.set(tipo_ui)
        self.tipo_organizacion_seleccionado = tipo_key
        self._cargar_organizaciones_en_combo(tipo_key=tipo_key)
        display = self._resolver_display_por_id(id_org, nombre_ui)
        if not display:
            return
        if self.var_organizacion:
            self.var_organizacion.set(display)
        self.cbx_organizacion.set(display)
        self._aplicar_filtro_organizacion(tipo_key=tipo_key, id_org=id_org, nombre_ui=display)

    def _resolver_display_por_id(self, id_org: int, nombre_ui: str) -> str:
        for display, item_id in self.map_organizaciones.items():
            if item_id == id_org:
                return display
        if nombre_ui and nombre_ui in self.map_organizaciones:
            return nombre_ui
        return ""

    def _actualizar_documentos_filtrados_organizacion(self):
        if not self._tiene_filtro_organizacion():
            self.documentos_filtrados_organizacion = []
            self.total_documentos = 0
            return

        ids_organizacion = {
            doc.get("id")
            for doc in self.documentos_organizacion
            if doc.get("id") is not None
        }
        if not ids_organizacion:
            self.documentos_filtrados_organizacion = []
            self.total_documentos = 0
            return

        if self.termino_busqueda_actual:
            campo_db = self.campo_busqueda_actual or "todo"
            termino = self.termino_busqueda_actual
        else:
            campo_db = "todo"
            termino = ""

        resultados = self.consulta.buscar_en_estante(
            campo=campo_db,
            termino=termino,
            limit=None,
            offset=0,
        )
        self.documentos_filtrados_organizacion = [
            doc for doc in resultados if doc.get("id") in ids_organizacion
        ]
        self.total_documentos = len(self.documentos_filtrados_organizacion)

    def _procesar_carga_imagenes(self, tareas):
        """Procesa la carga de imágenes en un hilo separado."""
        for ruta, label, ancho, alto in tareas:
            if os.path.exists(ruta):
                try:
                    img = Image.open(ruta)
                    img.thumbnail((ancho, alto))
                    img.load()  # Forzar carga en memoria
                    self.master.after(0, self._actualizar_imagen_label, label, img)
                except Exception as e:
                    print(f"Error al cargar la imagen {ruta}: {e}")
                    self.master.after(0, self._configurar_label_error, label)
            else:
                self.master.after(0, self._configurar_label_sin_portada, label)

    def _actualizar_imagen_label(self, label, pil_image):
        """Actualiza el label con la imagen cargada (en el hilo principal)."""
        try:
            if label.winfo_exists():
                photo = ImageTk.PhotoImage(pil_image)
                label.config(text="", image=photo)
                self._referencias_imagenes.append(photo)
        except Exception:
            pass

    def _configurar_label_sin_portada(self, label):
        """Configura el label cuando no hay portada (en el hilo principal)."""
        try:
            if label.winfo_exists():
                label.config(text="🖼️\nSin portada", font=("Helvetica", 10), bootstyle="secondary")
        except Exception:
            pass

    def _configurar_label_error(self, label):
        """Configura el label cuando hay error (en el hilo principal)."""
        try:
            if label.winfo_exists():
                label.config(text="🖼️\nError", font=("Helvetica", 10))
        except Exception:
            pass

    def _construir_tooltip_documento(
        self,
        nombre: str,
        titulo: str,
        paginas: Any,
        tamano_str: str,
        progreso_texto: str = "",
    ) -> str:
        tooltip_text = f"Nombre: {nombre}"
        if titulo:
            tooltip_text += f"\nTítulo: {titulo}"
        if paginas:
            tooltip_text += f"\nPáginas: {paginas}"
        tooltip_text += f"\nTamaño: {tamano_str}"
        if progreso_texto:
            tooltip_text += f"\n{progreso_texto}"
        return tooltip_text

    def _construir_detalle_lista_documento(self, doc: Dict[str, Any]) -> str:
        partes_linea_1 = []
        if doc.get("titulo"):
            partes_linea_1.append(f"Título: {doc['titulo']}")
        if doc.get("autores"):
            partes_linea_1.append(f"Autores: {doc['autores']}")
        if doc.get("editorial"):
            partes_linea_1.append(f"Editorial: {doc['editorial']}")

        if not partes_linea_1:
            partes_linea_1.append("Sin metadatos bibliográficos")

        partes_linea_2 = []
        if doc.get("isbn"):
            partes_linea_2.append(f"ISBN: {doc['isbn']}")
        if doc.get("coleccion"):
            partes_linea_2.append(f"Colección: {doc['coleccion']}")
        if doc.get("grupo"):
            partes_linea_2.append(f"Grupo: {doc['grupo']}")
        if doc.get("numero_paginas"):
            partes_linea_2.append(f"Páginas: {doc['numero_paginas']}")

        extension = doc.get("extension", "").upper() or "N/A"
        tamano = self._formatear_tamano(doc.get("tamano", 0))
        partes_linea_2.append(f"Archivo: {extension}")
        partes_linea_2.append(f"Tamaño: {tamano}")

        detalle = f"{' | '.join(partes_linea_1)}\n{' | '.join(partes_linea_2)}"

        return detalle

    def _obtener_progreso_documento(self, id_documento: Any) -> Dict[str, Any]:
        try:
            id_normalizado = str(int(id_documento))
        except (TypeError, ValueError):
            return {}
        progreso = self.progresos_lectura.get(id_normalizado, {})
        return progreso if isinstance(progreso, dict) else {}

    def _obtener_total_paginas_documento(self, doc: Dict[str, Any]) -> int:
        total_paginas = doc.get("numero_paginas")
        try:
            return max(0, int(total_paginas))
        except (TypeError, ValueError):
            return 0

    def _normalizar_pagina_actual(self, pagina_actual: Any) -> int:
        try:
            return max(0, int(pagina_actual))
        except (TypeError, ValueError):
            return 0

    def _resolver_estado_lectura(self, pagina_actual: int, total_paginas: int) -> str:
        if pagina_actual <= 0:
            return "Pendiente"
        if total_paginas > 0 and pagina_actual >= total_paginas:
            return "Completado"
        return "En lectura"

    def _calcular_info_progreso_documento(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        progreso = self._obtener_progreso_documento(doc.get("id"))
        if not progreso:
            return {}

        pagina_actual = self._normalizar_pagina_actual(progreso.get("pagina_actual", 0))
        total_paginas = self._obtener_total_paginas_documento(doc)
        pagina_mostrada = pagina_actual
        porcentaje = None

        if total_paginas > 0:
            pagina_mostrada = min(pagina_actual, total_paginas)
            porcentaje = int(round((pagina_mostrada / total_paginas) * 100))

        return {
            "pagina_actual": pagina_actual,
            "pagina_mostrada": pagina_mostrada,
            "total_paginas": total_paginas,
            "porcentaje": porcentaje,
            "estado": self._resolver_estado_lectura(
                pagina_actual=pagina_mostrada,
                total_paginas=total_paginas,
            ),
        }

    def _construir_texto_progreso_documento(self, doc: Dict[str, Any]) -> str:
        info = self._calcular_info_progreso_documento(doc)
        if not info:
            return ""

        if info["total_paginas"] > 0:
            return (
                f"Lectura: {info['porcentaje']}% "
                f"({info['pagina_mostrada']}/{info['total_paginas']}) · {info['estado']}"
            )
        return f"Lectura: página {info['pagina_actual']} · {info['estado']}"

    def _construir_texto_progreso_resumido(self, doc: Dict[str, Any]) -> str:
        info = self._calcular_info_progreso_documento(doc)
        if not info:
            return ""
        if info["total_paginas"] > 0:
            porcentaje = max(0, min(100, int(info["porcentaje"])))
            bloques_totales = 10
            bloques_llenos = int(round((porcentaje / 100) * bloques_totales))
            bloques_llenos = max(0, min(bloques_totales, bloques_llenos))
            barra = ("█" * bloques_llenos) + ("░" * (bloques_totales - bloques_llenos))
            return f"{porcentaje}% {barra} ({info['pagina_mostrada']}/{info['total_paginas']})"
        return f"Pág. {info['pagina_actual']}"

    def _depurar_progresos_lectura_huerfanos(self):
        if not self.progresos_lectura:
            return

        try:
            ids_validos = {
                str(doc["id"])
                for doc in Consulta().get_todos_documentos()
                if doc.get("id") is not None
            }
        except Exception:
            return

        progreso_filtrado = {
            id_documento: datos
            for id_documento, datos in self.progresos_lectura.items()
            if id_documento in ids_validos
        }
        if len(progreso_filtrado) != len(self.progresos_lectura):
            if self.config.guardar_progresos_lectura(progresos=progreso_filtrado):
                self.progresos_lectura = progreso_filtrado

    # --- Métodos para el menú contextual ---

    def _mostrar_menu_contextual(self, event, documento):
        """Guarda el documento seleccionado y muestra el menú en la posición del cursor."""
        self.documento_seleccionado_contextual = documento

        # Actualizar etiquetas dinámicas del menú contextual.
        es_favorito = documento.get("es_favorito", 0)
        label_favorito = "🌟 Quitar de favoritos" if es_favorito else "⭐ Marcar como favorito"
        self.menu_contextual.entryconfig(self.menu_index_favorito, label=label_favorito)

        comentario = self.comentarios.obtener_comentario(documento.get("id"))
        label_comentario = (
            "📝 Ver/Editar comentario" if comentario.strip() else "📝 Agregar comentario"
        )
        self.menu_contextual.entryconfig(self.menu_index_comentario, label=label_comentario)

        progreso = self._obtener_progreso_documento(documento.get("id"))
        if progreso:
            self.menu_contextual.entryconfig(
                self.menu_index_progreso,
                label="✏️ Actualizar progreso de lectura",
            )
            self.menu_contextual.entryconfig(self.menu_index_quitar_progreso, state=NORMAL)
        else:
            self.menu_contextual.entryconfig(
                self.menu_index_progreso,
                label="📘 Registrar progreso de lectura",
            )
            self.menu_contextual.entryconfig(self.menu_index_quitar_progreso, state=DISABLED)

        self.menu_contextual.post(event.x_root, event.y_root)

    def _on_abrir_documento_contextual(self):
        """Manejador para la opción 'Abrir' del menú."""
        if self.documento_seleccionado_contextual:
            self._abrir_documento(self.documento_seleccionado_contextual)

    def _get_documento_contextual(self):
        return self.documento_seleccionado_contextual

    def _on_comentario_contextual(self):
        if not self.documento_seleccionado_contextual:
            return

        doc_id = self.documento_seleccionado_contextual.get("id")
        nombre_doc = self.documento_seleccionado_contextual.get("nombre", "Documento")
        comentario_actual = self.comentarios.obtener_comentario(doc_id)

        texto = ask_resizable_text(
            master=self.master,
            title="Comentario del documento",
            prompt=f"Comentario para: {nombre_doc}",
            initialvalue=comentario_actual,
        )
        if texto is None:
            return

        texto = texto.strip()
        if not texto and comentario_actual:
            if not askyesno(
                "Eliminar comentario",
                "El comentario está vacío. ¿Desea eliminarlo?",
                parent=self.master,
            ):
                return

        if self.comentarios.guardar_comentario(doc_id, texto):
            if texto:
                showinfo("Comentario", "Comentario guardado.", parent=self.master)
            else:
                showinfo("Comentario", "Comentario eliminado.", parent=self.master)
            self._mostrar_pagina_actual()
        else:
            showerror("Error", "No se pudo guardar el comentario.", parent=self.master)

    def _on_ver_detalles_contextual(self):
        """Manejador para la opción 'Ver detalles' del menú. Abre el diálogo de metadatos."""
        if not self.documento_seleccionado_contextual:
            return

        doc_id = self.documento_seleccionado_contextual["id"]
        # Creamos una instancia de Documento para pasarla al diálogo
        doc_obj = Documento(id=doc_id, nombre="", extension="", hash="", tamano=0)

        if doc_obj.instanciar():
            dialog = DialogVisualizarMetadatos(title="Metadatos del Documento", master=self.master)
            dialog.set_documento(doc_obj)
            dialog.grab_set()
        else:
            showerror(
                "Error",
                "No se pudo cargar la información completa del documento.",
                parent=self.master,
            )

    def _on_marcar_favorito_contextual(self):
        """Manejador para la opción 'Marcar/Quitar favorito' del menú."""
        if not self.documento_seleccionado_contextual:
            return

        doc_id = self.documento_seleccionado_contextual["id"]

        es_favorito_actual = self.documento_seleccionado_contextual.get("es_favorito", 0)
        favorito = Favorito(id_documento=doc_id)

        if es_favorito_actual:
            if favorito.desmarcar():
                showinfo("Favorito", "Documento quitado de favoritos.", parent=self.master)
                self.documento_seleccionado_contextual["es_favorito"] = 0
            else:
                showerror("Error", "No se pudo quitar de favoritos.", parent=self.master)
        else:
            if favorito.marcar():
                showinfo("Favorito", "Documento añadido a favoritos.", parent=self.master)
                self.documento_seleccionado_contextual["es_favorito"] = 1
            else:
                showerror("Error", "No se pudo añadir a favoritos.", parent=self.master)

    def _on_registrar_progreso_lectura_contextual(self):
        if not self.documento_seleccionado_contextual:
            return

        doc = self.documento_seleccionado_contextual
        doc_id = doc.get("id")
        try:
            id_documento = int(doc_id)
        except (TypeError, ValueError):
            showerror("Error", "No se pudo identificar el documento.", parent=self.master)
            return

        total_paginas = self._obtener_total_paginas_documento(doc)
        progreso_actual = self._obtener_progreso_documento(id_documento)
        pagina_inicial = str(self._normalizar_pagina_actual(progreso_actual.get("pagina_actual", 0)))
        texto_limite = f" (0 a {total_paginas})" if total_paginas > 0 else ""
        pagina_ingresada = ask_resizable_string(
            master=self.master,
            title="Progreso de lectura",
            prompt=f"Ingresa la página en la que vas:{texto_limite}",
            initialvalue=pagina_inicial,
        )
        if pagina_ingresada is None:
            return

        pagina_ingresada = pagina_ingresada.strip()
        if not pagina_ingresada:
            showwarning("Valor requerido", "Debes ingresar un número de página.", parent=self.master)
            return

        try:
            pagina_actual = int(pagina_ingresada)
        except ValueError:
            showwarning("Valor inválido", "La página debe ser un número entero.", parent=self.master)
            return

        if pagina_actual < 0:
            showwarning("Valor inválido", "La página no puede ser negativa.", parent=self.master)
            return

        if total_paginas > 0 and pagina_actual > total_paginas:
            showwarning(
                "Valor fuera de rango",
                f"La página no puede ser mayor al total ({total_paginas}).",
                parent=self.master,
            )
            return

        if not self.config.guardar_progreso_lectura(
            id_documento=id_documento,
            pagina_actual=pagina_actual,
        ):
            showerror("Error", "No se pudo guardar el progreso de lectura.", parent=self.master)
            return

        self.progresos_lectura = self.config.obtener_progresos_lectura()
        self.recargar_estante()

        if total_paginas > 0:
            porcentaje = int(round((pagina_actual / total_paginas) * 100))
            estado = self._resolver_estado_lectura(
                pagina_actual=pagina_actual,
                total_paginas=total_paginas,
            )
            showinfo(
                "Progreso guardado",
                f"Lectura actualizada: {porcentaje}% ({pagina_actual}/{total_paginas}) · {estado}.",
                parent=self.master,
            )
        else:
            showinfo(
                "Progreso guardado",
                f"Lectura actualizada en la página {pagina_actual}.",
                parent=self.master,
            )

    def _on_quitar_progreso_lectura_contextual(self):
        if not self.documento_seleccionado_contextual:
            return

        doc_id = self.documento_seleccionado_contextual.get("id")
        try:
            id_documento = int(doc_id)
        except (TypeError, ValueError):
            showerror("Error", "No se pudo identificar el documento.", parent=self.master)
            return

        if not self._obtener_progreso_documento(id_documento):
            showinfo(
                "Progreso de lectura",
                "El documento no tiene progreso de lectura registrado.",
                parent=self.master,
            )
            return

        if not self.config.eliminar_progreso_lectura(id_documento=id_documento):
            showerror("Error", "No se pudo eliminar el progreso de lectura.", parent=self.master)
            return

        self.progresos_lectura.pop(str(id_documento), None)
        self.recargar_estante()
        showinfo("Progreso de lectura", "Se eliminó el progreso de lectura.", parent=self.master)

    def _abrir_documento(self, doc_data: Dict[str, Any]):
        """Abre un documento copiándolo a la carpeta temporal."""
        ruta_biblioteca = self.config.obtener_ubicacion_biblioteca()
        if not ruta_biblioteca or not os.path.exists(ruta_biblioteca):
            showerror(
                "Error de Configuración",
                "La ubicación de la biblioteca no está configurada o no existe.",
                parent=self.master,
            )
            return

        nombre_archivo = f"{doc_data['nombre']}.{doc_data['extension']}"
        ruta_origen = generar_ruta_documento(
            ruta_biblioteca=ruta_biblioteca,
            id_documento=doc_data["id"],
            nombre_documento=nombre_archivo,
        )

        if not os.path.exists(ruta_origen):
            showerror(
                "Archivo no encontrado",
                f"El archivo no se encontró en la biblioteca:\n{ruta_origen}",
                parent=self.master,
            )
            return

        ruta_destino_temporal = os.path.join(DIRECTORIO_TEMPORAL, nombre_archivo)
        try:
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino_temporal)
            abrir_archivo(ruta_origen=ruta_destino_temporal)
        except Exception as e:
            showerror("Error al abrir", f"No se pudo abrir el documento: {e}", parent=self.master)

    def _formatear_tamano(self, bytes_size: int) -> str:
        """
        Formatea el tamaño de un archivo de bytes a una unidad legible.
        """
        if not isinstance(bytes_size, (int, float)) or bytes_size < 0:
            return "0 B"

        if bytes_size == 0:
            return "0 B"

        unidades = ["B", "KB", "MB", "GB", "TB", "PB"]
        # Calcular el índice de la unidad apropiada
        try:
            indice = min(int(math.log(bytes_size, 1024)), len(unidades) - 1)
        except (ValueError, TypeError):
            return "0 B"

        # Calcular el valor en la unidad correspondiente
        valor = bytes_size / (1024**indice)

        # Formatear según la unidad
        if indice == 0:  # Bytes
            return f"{int(valor)} B"
        else:
            return f"{valor:.2f} {unidades[indice]}"
