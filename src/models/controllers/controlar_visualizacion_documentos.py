from ttkbootstrap.tableview import Tableview
from ttkbootstrap import Treeview, Button, Entry, Combobox, StringVar
from typing import Dict, Any, List
from os.path import join, exists
from tkinter.messagebox import showerror, showwarning
import math
from models.entities.consulta import Consulta
from models.entities.coleccion import Coleccion
from models.entities.categoria import Categoria
from models.entities.etiqueta import Etiqueta
from models.entities.palabra_clave import PalabraClave
from models.entities.grupo import Grupo
from models.controllers.configuracion_controller import ConfiguracionController
from utilities.configuracion import DIRECTORIO_TEMPORAL
from utilities.auxiliar import (
    generar_ruta_documento,
    abrir_archivo,
    copiar_archivo,
)


class ControlarVisualizacionDocumentos:
    """
    Controlador para la lógica de la vista principal de documentos.

    Gestiona la carga de datos en los Treeviews de organización y la
    interacción entre estos y la tabla de documentos.
    """

    def __init__(self, master, map_widgets: Dict[str, Any], map_vars: Dict[str, Any]):
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars
        self.consulta = Consulta()

        # --- Widgets ---
        self.map_treeviews: Dict[str, Treeview] = self.map_widgets["treeviews"]
        self.table_view: Tableview = self.map_widgets["table_view"]
        self.ent_buscar: Entry = self.map_widgets["ent_buscar"]
        self.btn_buscar: Button = self.map_widgets["btn_buscar"]
        self.cbx_campos: Combobox = self.map_widgets["cbx_campos"]
        self.btn_refrescar: Button = self.map_widgets["btn_refrescar"]

        # --- Iconos ---
        self.icon_libro = "📕"
        self.icon_coleccion = "📚"
        self.icon_grupo = "🗂️"
        self.icon_categoria = "🗃️"
        self.icon_etiqueta = "🏷️"
        self.icon_palabra_clave = "🔑"

        # --- Variables ---
        self.colecciones: List[Coleccion] = []
        self.map_colecciones: Dict[int, Coleccion] = {}
        self.map_documentos_por_coleccion: Dict[int, List[Dict[str, Any]]] = {}
        self.grupos: List[Grupo] = []
        self.map_grupos: Dict[int, Grupo] = {}
        self.map_documentos_por_grupo: Dict[int, List[Dict[str, Any]]] = {}
        self.categorias: List[Categoria] = []
        self.map_categorias: Dict[int, Categoria] = {}
        self.map_documentos_por_categoria: Dict[int, List[Dict[str, Any]]] = {}
        self.etiquetas: List[Etiqueta] = []
        self.map_etiquetas: Dict[int, Etiqueta] = {}
        self.map_documentos_por_etiqueta: Dict[int, List[Dict[str, Any]]] = {}
        self.palabras_clave: List[PalabraClave] = []
        self.map_palabras_clave: Dict[int, PalabraClave] = {}
        self.map_documentos_por_palabra_clave: Dict[int, List[Dict[str, Any]]] = {}
        self.map_documentos: Dict[int, Dict[str, Any]] = {}

        # --- Inicialización ---
        self._vincular_eventos()
        self._cargar_datos_iniciales()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Inicialización
    # └────────────────────────────────────────────────────────────┘

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a sus manejadores."""
        # Vincular evento de selección en el Treeview de Colecciones
        tree_colecciones = self.map_treeviews.get("Colecciones")
        if tree_colecciones:
            tree_colecciones.bind("<Double-1>", self.on_doble_clic_tree_coleccion)

        # Vincular evento de selección en el Treeview de Grupos
        tree_grupos = self.map_treeviews.get("Grupos")
        if tree_grupos:
            tree_grupos.bind("<Double-1>", self.on_doble_clic_tree_grupo)

        # Vincular evento de selección en el Treeview de Categorías
        tree_categorias = self.map_treeviews.get("Categorías")
        if tree_categorias:
            tree_categorias.bind("<Double-1>", self.on_doble_clic_tree_categoria)

        # Vincular evento de selección en el Treeview de Etiquetas
        tree_etiquetas = self.map_treeviews.get("Etiquetas")
        if tree_etiquetas:
            tree_etiquetas.bind("<Double-1>", self.on_doble_clic_tree_etiqueta)

        # Vincular evento de selección en el Treeview de Palabras Clave
        tree_palabras_clave = self.map_treeviews.get("Palabras Clave")
        if tree_palabras_clave:
            tree_palabras_clave.bind("<Double-1>", self.on_doble_clic_tree_palabra_clave)

        # Vincular evento de doble clic en la tabla de documentos
        self.table_view.view.bind("<Double-1>", self.on_doble_clic_tabla_documentos)

        # Vincular botón de búsqueda
        self.btn_buscar.config(command=self.on_buscar_documentos)
        self.ent_buscar.bind("<Return>", lambda event: self.on_buscar_documentos())

        # Vincular botón de refrescar
        self.btn_refrescar.config(command=self.recargar_datos)

    def _cargar_datos_iniciales(self):
        """Carga los datos necesarios al iniciar el controlador."""
        self._cargar_colecciones()
        self._cargar_grupos()
        self._cargar_categorias()
        self._cargar_etiquetas()
        self._cargar_palabras_clave()

    def recargar_datos(self):
        """Vuelve a cargar todos los datos de los treeviews."""
        self._cargar_datos_iniciales()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Lógica de Carga de Datos (Pestaña Colecciones)
    # └────────────────────────────────────────────────────────────┘

    def _cargar_colecciones(self):
        """Carga las colecciones desde la BD y las muestra en el Treeview."""
        tree_colecciones = self.map_treeviews.get("Colecciones")
        if not tree_colecciones:
            return

        # Limpiar Treeview
        for item in tree_colecciones.get_children():
            tree_colecciones.delete(item)

        # Obtener datos
        self.colecciones = self.consulta.get_colecciones()
        self.map_colecciones = {col.id: col for col in self.colecciones}

        # Poblar Treeview con colecciones y sus documentos
        if self.colecciones:
            for coleccion in self.colecciones:
                # Obtener documentos para esta colección
                documentos = self.consulta.get_documentos_por_coleccion(coleccion.id)
                self.map_documentos_por_coleccion[coleccion.id] = documentos

                # Insertar la colección como nodo padre
                iid_coleccion = f"col_{coleccion.id}"
                tree_colecciones.insert(
                    "",
                    "end",
                    iid=iid_coleccion,
                    text=f" {self.icon_coleccion} {coleccion.nombre} ({len(documentos)})",
                )

                # Insertar los documentos como hijos
                for doc in documentos:
                    # El iid debe ser único en todo el Treeview
                    iid_documento = f"{iid_coleccion}_doc_{doc['id']}"
                    tree_colecciones.insert(
                        iid_coleccion, "end", iid=iid_documento, text=f"  📄 {doc['nombre']}"
                    )
                    # Guardar el documento en el mapa global para acceso rápido
                    self.map_documentos[doc['id']] = doc

    # ┌────────────────────────────────────────────────────────────┐
    # │ Lógica de Carga de Datos (Pestaña Grupos)
    # └────────────────────────────────────────────────────────────┘

    def _cargar_grupos(self):
        """Carga los grupos desde la BD y las muestra en el Treeview."""
        tree_grupos = self.map_treeviews.get("Grupos")
        if not tree_grupos:
            return

        # Limpiar Treeview
        for item in tree_grupos.get_children():
            tree_grupos.delete(item)

        # Obtener datos
        self.grupos = self.consulta.get_grupos()
        self.map_grupos = {g.id: g for g in self.grupos}

        # Poblar Treeview con grupos y sus documentos
        if self.grupos:
            for grupo in self.grupos:
                # Obtener documentos para este grupo
                documentos = self.consulta.get_documentos_por_grupo(grupo.id)
                self.map_documentos_por_grupo[grupo.id] = documentos

                # Insertar el grupo como nodo padre
                iid_grupo = f"gpo_{grupo.id}"
                tree_grupos.insert(
                    "",
                    "end",
                    iid=iid_grupo,
                    text=f" {self.icon_grupo} {grupo.nombre} ({len(documentos)})",
                )

                # Insertar los documentos como hijos
                for doc in documentos:
                    iid_documento = f"{iid_grupo}_doc_{doc['id']}"
                    tree_grupos.insert(
                        iid_grupo, "end", iid=iid_documento, text=f"  📄 {doc['nombre']}"
                    )
                    self.map_documentos[doc['id']] = doc

    # ┌────────────────────────────────────────────────────────────┐
    # │ Lógica de Carga de Datos (Pestaña Categorías)
    # └────────────────────────────────────────────────────────────┘

    def _cargar_categorias(self):
        """Carga las categorías y sus documentos de forma jerárquica."""
        tree_categorias = self.map_treeviews.get("Categorías")
        if not tree_categorias:
            return

        for item in tree_categorias.get_children():
            tree_categorias.delete(item)

        self.categorias = self.consulta.get_categorias()
        self.map_categorias = {cat.id: cat for cat in self.categorias}

        # Organizar categorías en un diccionario de hijos por padre
        nodos_hijos = {}
        for cat in self.categorias:
            parent_id = cat.id_padre if cat.id_padre is not None else 0
            if parent_id not in nodos_hijos:
                nodos_hijos[parent_id] = []
            nodos_hijos[parent_id].append(cat)

        # Función recursiva para añadir nodos al Treeview
        def anadir_nodos(parent_id, parent_iid):
            if parent_id in nodos_hijos:
                for cat in sorted(nodos_hijos[parent_id], key=lambda x: x.nombre):
                    documentos = self.consulta.get_documentos_por_categoria(cat.id)
                    self.map_documentos_por_categoria[cat.id] = documentos

                    iid_categoria = f"cat_{cat.id}"
                    tree_categorias.insert(
                        parent_iid,
                        "end",
                        iid=iid_categoria,
                        text=f" {self.icon_categoria} {cat.nombre} ({len(documentos)})",
                        open=False,  # Iniciar cerradas
                    )

                    # Insertar documentos como hijos de la categoría
                    for doc in documentos:
                        iid_documento = f"{iid_categoria}_doc_{doc['id']}"
                        tree_categorias.insert(
                            iid_categoria,
                            "end",
                            iid=iid_documento,
                            text=f"  📄 {doc['nombre']}",
                        )
                        self.map_documentos[doc['id']] = doc

                    # Llamada recursiva para las subcategorías
                    anadir_nodos(cat.id, iid_categoria)

        # Iniciar la carga desde las categorías raíz (id_padre es 0 o None)
        anadir_nodos(0, "")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Lógica de Carga de Datos (Pestaña Etiquetas)
    # └────────────────────────────────────────────────────────────┘

    def _cargar_etiquetas(self):
        """Carga las etiquetas desde la BD y las muestra en el Treeview."""
        tree_etiquetas = self.map_treeviews.get("Etiquetas")
        if not tree_etiquetas:
            return

        # Limpiar Treeview
        for item in tree_etiquetas.get_children():
            tree_etiquetas.delete(item)

        # Obtener datos
        self.etiquetas = self.consulta.get_etiquetas()
        self.map_etiquetas = {e.id: e for e in self.etiquetas}

        # Poblar Treeview con etiquetas y sus documentos
        if self.etiquetas:
            for etiqueta in self.etiquetas:
                # Obtener documentos para esta etiqueta
                documentos = self.consulta.get_documentos_por_etiqueta(etiqueta.id)
                self.map_documentos_por_etiqueta[etiqueta.id] = documentos

                # Insertar la etiqueta como nodo padre
                iid_etiqueta = f"eti_{etiqueta.id}"
                tree_etiquetas.insert(
                    "",
                    "end",
                    iid=iid_etiqueta,
                    text=f" {self.icon_etiqueta} {etiqueta.nombre} ({len(documentos)})",
                )

                # Insertar los documentos como hijos
                for doc in documentos:
                    iid_documento = f"{iid_etiqueta}_doc_{doc['id']}"
                    tree_etiquetas.insert(
                        iid_etiqueta, "end", iid=iid_documento, text=f"  📄 {doc['nombre']}"
                    )
                    self.map_documentos[doc['id']] = doc

    # ┌────────────────────────────────────────────────────────────┐
    # │ Lógica de Carga de Datos (Pestaña Palabras Clave)
    # └────────────────────────────────────────────────────────────┘

    def _cargar_palabras_clave(self):
        """Carga las palabras clave desde la BD y las muestra en el Treeview."""
        tree_palabras_clave = self.map_treeviews.get("Palabras Clave")
        if not tree_palabras_clave:
            return

        # Limpiar Treeview
        for item in tree_palabras_clave.get_children():
            tree_palabras_clave.delete(item)

        # Obtener datos
        self.palabras_clave = self.consulta.get_palabras_clave()
        self.map_palabras_clave = {pc.id: pc for pc in self.palabras_clave}

        # Poblar Treeview con palabras clave y sus documentos
        if self.palabras_clave:
            for pc in self.palabras_clave:
                # Obtener documentos para esta palabra clave
                documentos = self.consulta.get_documentos_por_palabra_clave(pc.id)
                self.map_documentos_por_palabra_clave[pc.id] = documentos

                # Insertar la palabra clave como nodo padre
                iid_pc = f"pc_{pc.id}"
                tree_palabras_clave.insert(
                    "",
                    "end",
                    iid=iid_pc,
                    text=f" {self.icon_palabra_clave} {pc.palabra} ({len(documentos)})",
                )

                # Insertar los documentos como hijos
                for doc in documentos:
                    iid_documento = f"{iid_pc}_doc_{doc['id']}"
                    tree_palabras_clave.insert(
                        iid_pc, "end", iid=iid_documento, text=f"  📄 {doc['nombre']}"
                    )
                    self.map_documentos[doc['id']] = doc

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Auxiliares
    # └────────────────────────────────────────────────────────────┘

    def _poblar_tabla(self, lista_documentos: List[Dict[str, Any]]):
        """Limpia y puebla la tabla con una lista de documentos."""
        self.table_view.delete_rows()
        if not lista_documentos:
            return

        coldata = self.master.coldata  # Acceder a coldata desde la instancia de la vista
        row_data = []
        for doc in lista_documentos:
            row_data.append(self._formatear_fila_documento(doc))

        self.table_view.build_table_data(coldata, row_data)
        self.table_view.autofit_columns()
        self.table_view.autoalign_columns()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Manejadores de Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_buscar_documentos(self):
        """
        Se ejecuta al presionar el botón de búsqueda. Filtra los documentos
        según el criterio y término de búsqueda y los muestra en la tabla.
        """
        campo = self.cbx_campos.get()
        termino = self.ent_buscar.get().strip()

        if not termino:
            showwarning(
                title="Búsqueda vacía", message="Por favor, ingrese un término para buscar."
            )
            return

        # Llamar al método de búsqueda del DAO
        resultados = self.consulta.buscar_documentos_por_nombre(campo=campo, buscar=termino)

        # Actualizar el mapa de documentos con los resultados de la búsqueda
        for doc in resultados:
            self.map_documentos[doc['id']] = doc

        self._poblar_tabla(resultados)

    def on_doble_clic_tree_coleccion(self, event=None):
        """
        Se ejecuta al seleccionar una colección en el Treeview.
        Busca los documentos asociados y los muestra en la tabla.
        """
        tree_colecciones = self.map_treeviews.get("Colecciones")
        if not tree_colecciones:
            return

        iid_seleccionado = tree_colecciones.focus()
        if not iid_seleccionado:
            return

        # El iid puede ser "col_1" o "col_1_doc_9"
        partes_iid = iid_seleccionado.split("_")
        tipo = partes_iid[0]
        id_item = partes_iid[1]  # Siempre será el ID de la colección o del documento

        id_item = int(id_item)

        if tipo == "col":
            # Se hizo doble clic en una colección
            documentos = self.map_documentos_por_coleccion.get(id_item, [])
            self._poblar_tabla(documentos)
        elif tipo == "doc":
            # El ID del documento es la última parte del iid
            id_documento = int(partes_iid[-1])
            documento = self.map_documentos.get(id_item)
            if documento:
                self._poblar_tabla([documento])

    def on_doble_clic_tree_grupo(self, event=None):
        """
        Se ejecuta al seleccionar un grupo en el Treeview.
        Busca los documentos asociados y los muestra en la tabla.
        """
        tree_grupos = self.map_treeviews.get("Grupos")
        if not tree_grupos:
            return

        iid_seleccionado = tree_grupos.focus()
        if not iid_seleccionado:
            return

        partes_iid = iid_seleccionado.split("_")
        tipo = partes_iid[0]
        id_item = int(partes_iid[1])

        if tipo == "gpo":
            # Se hizo doble clic en un grupo
            documentos = self.map_documentos_por_grupo.get(id_item, [])
            self._poblar_tabla(documentos)
        elif tipo == "doc":
            # Se hizo doble clic en un documento
            id_documento = int(partes_iid[-1])
            documento = self.map_documentos.get(id_documento)
            if documento:
                self._poblar_tabla([documento])

    def on_doble_clic_tree_categoria(self, event=None):
        """
        Se ejecuta al seleccionar una categoría en el Treeview.
        Busca los documentos asociados y los muestra en la tabla.
        """
        tree_categorias = self.map_treeviews.get("Categorías")
        if not tree_categorias:
            return

        iid_seleccionado = tree_categorias.focus()
        if not iid_seleccionado:
            return

        partes_iid = iid_seleccionado.split("_")
        tipo = partes_iid[0]
        id_item = int(partes_iid[1])

        if tipo == "cat":
            # Se hizo doble clic en una categoría
            documentos = self.map_documentos_por_categoria.get(id_item, [])
            self._poblar_tabla(documentos)
        elif tipo == "doc":
            # Se hizo doble clic en un documento
            id_documento = int(partes_iid[-1])
            documento = self.map_documentos.get(id_documento)
            if documento:
                self._poblar_tabla([documento])

    def on_doble_clic_tree_etiqueta(self, event=None):
        """
        Se ejecuta al seleccionar una etiqueta en el Treeview.
        Busca los documentos asociados y los muestra en la tabla.
        """
        tree_etiquetas = self.map_treeviews.get("Etiquetas")
        if not tree_etiquetas:
            return

        iid_seleccionado = tree_etiquetas.focus()
        if not iid_seleccionado:
            return

        partes_iid = iid_seleccionado.split("_")
        tipo = partes_iid[0]
        id_item = int(partes_iid[1])

        if tipo == "eti":
            # Se hizo doble clic en una etiqueta
            documentos = self.map_documentos_por_etiqueta.get(id_item, [])
            self._poblar_tabla(documentos)
        elif tipo == "doc":
            # Se hizo doble clic en un documento
            id_documento = int(partes_iid[-1])
            documento = self.map_documentos.get(id_documento)
            if documento:
                self._poblar_tabla([documento])

    def on_doble_clic_tree_palabra_clave(self, event=None):
        """
        Se ejecuta al seleccionar una palabra clave en el Treeview.
        Busca los documentos asociados y los muestra en la tabla.
        """
        tree_palabras_clave = self.map_treeviews.get("Palabras Clave")
        if not tree_palabras_clave:
            return

        iid_seleccionado = tree_palabras_clave.focus()
        if not iid_seleccionado:
            return

        partes_iid = iid_seleccionado.split("_")
        tipo = partes_iid[0]
        id_item = int(partes_iid[1])

        if tipo == "pc":
            # Se hizo doble clic en una palabra clave
            documentos = self.map_documentos_por_palabra_clave.get(id_item, [])
            self._poblar_tabla(documentos)
        elif tipo == "doc":
            # Se hizo doble clic en un documento
            id_documento = int(partes_iid[-1])
            documento = self.map_documentos.get(id_documento)
            if documento:
                self._poblar_tabla([documento])

    def on_doble_clic_tabla_documentos(self, event=None):
        """
        Se ejecuta al hacer doble clic en una fila de la tabla de documentos.
        Abre el archivo correspondiente.
        """
        selected_row = self.table_view.get_rows(selected=True)
        if not selected_row:
            return

        # Obtenemos el ID del documento de la primera columna
        id_documento = selected_row[0].values[0]
        documento_data = self.map_documentos.get(id_documento)

        if not documento_data:
            showerror(
                title="Error",
                message="No se encontró la información del documento.",
                parent=self.master,
            )
            return

        # Lógica para abrir el archivo
        config = ConfiguracionController()
        ruta_biblioteca = config.obtener_ubicacion_biblioteca()
        if not ruta_biblioteca or not exists(ruta_biblioteca):
            showerror(
                title="Error",
                message="La ubicación de la biblioteca no está configurada o no existe.",
            )
            return

        nombre_archivo = f"{documento_data['nombre']}.{documento_data['extension']}"
        ruta_origen = generar_ruta_documento(
            ruta_biblioteca=ruta_biblioteca,
            id_documento=id_documento,
            nombre_documento=nombre_archivo,
        )

        if not exists(ruta_origen):
            showerror(
                title="Archivo no encontrado",
                message=f"El archivo no se encontró en la biblioteca:\n{ruta_origen}",
            )
            return

        # Copiar a temporal y abrir
        ruta_destino_temporal = join(DIRECTORIO_TEMPORAL, nombre_archivo)
        try:
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino_temporal)
            abrir_archivo(ruta_origen=ruta_destino_temporal)
        except Exception as e:
            showerror(title="Error al abrir", message=f"No se pudo abrir el documento: {e}")

    def _formatear_fila_documento(self, doc: Dict[str, Any]) -> list:
        """Formatea un diccionario de documento a una lista para la tabla."""
        return [
            doc.get('id', '-'),
            self.icon_libro,
            doc.get('nombre', 'N/A'),
            doc.get('extension', ''),
            self._formatear_tamano(doc.get('tamano', 0)),
            doc.get('creado_en', '-'),
            doc.get('actualizado_en', '-'),
        ]

    def _formatear_tamano(self, bytes_size: int) -> str:
        """
        Formatea el tamaño de un archivo de bytes a una unidad legible.
        """
        if not isinstance(bytes_size, (int, float)) or bytes_size < 0:
            return "0 B"

        if bytes_size == 0:
            return "0 B"

        unidades = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
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
