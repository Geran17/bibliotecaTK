from os.path import exists
from tkinter.messagebox import showerror, showwarning
from tkinter import Menu
from typing import Dict, Any, List

from ttkbootstrap import Button, Entry, Combobox
from ttkbootstrap.tableview import Tableview

from models.controllers.configuracion_controller import ConfiguracionController
from models.controllers.controlar_menu_contextual_documento import (
    ControlarMenuContextualDocumento,
)
from models.entities.consulta import Consulta
from utilities.auxiliar import (
    abrir_documento_desde_biblioteca,
)


class ControlarVisualizarBiblioteca:
    """
    Controlador para la lógica de la vista de búsqueda bibliográfica.
    """

    def __init__(
        self,
        table_view: Tableview,
        ent_buscar: Entry,
        cbx_campos: Combobox,
        btn_buscar: Button,
        master,
    ):
        self.table_view = table_view
        self.ent_buscar = ent_buscar
        self.cbx_campos = cbx_campos
        self.btn_buscar = btn_buscar
        self.master = master

        self.map_documentos: Dict[int, Dict[str, Any]] = {}
        self.icon_libro = "📕"

        self.menu_ops = ControlarMenuContextualDocumento(
            master=self.master,
            get_documento_data=self._get_documento_contextual,
            on_refresh=self.recargar_resultados,
        )
        self._vincular_eventos()
        self._crear_menu_contextual()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a sus manejadores."""
        self.btn_buscar.config(command=self.on_buscar)
        self.ent_buscar.bind("<Return>", lambda event: self.on_buscar())
        self.table_view.view.bind("<Double-1>", self.on_doble_clic_tabla)
        self.table_view.view.bind("<Button-3>", self._mostrar_menu_contextual)

    def _crear_menu_contextual(self):
        self.menu_contextual = Menu(self.master, tearoff=0)
        self.menu_contextual.add_command(label="📖 Abrir documento", command=self.menu_ops.on_abrir_documento)
        self.menu_contextual.add_command(label="📂 Abrir carpeta", command=self.menu_ops.on_abrir_carpeta)
        self.menu_contextual.add_command(label="ℹ️ Propiedades", command=self.menu_ops.on_propiedades)
        self.menu_contextual.add_command(label="🧾 Ver metadatos", command=self.menu_ops.on_ver_metadatos)
        self.menu_contextual.add_command(label="📝 Comentario", command=self.menu_ops.on_comentario)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="✏️ Renombrar documento", command=self.menu_ops.on_renombrar_documento)
        self.menu_contextual.add_command(label="🧬 Renombrar bibliográficamente", command=self.menu_ops.on_renombrar_bibliografico)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="📋 Copiar documento", command=self.menu_ops.on_copiar_documento)
        self.menu_contextual.add_command(label="✂️ Mover documento", command=self.menu_ops.on_mover_documento)
        self.menu_contextual.add_command(label="🗑️ Enviar a papelera", command=self.menu_ops.on_enviar_papelera)
        self.menu_contextual.add_command(label="🗑️ Eliminar documento", command=self.menu_ops.on_eliminar_documento)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="🔄 Cambiar estado", command=self.menu_ops.on_cambiar_estado)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="🔎 Buscar", command=self.on_buscar)
        self.menu_contextual.add_command(label="🔄 Refrescar", command=self.recargar_resultados)

    def _mostrar_menu_contextual(self, event):
        item_id = self.table_view.view.identify_row(event.y)
        if item_id:
            self.table_view.view.selection_set(item_id)
            self.table_view.view.focus(item_id)
        self.menu_contextual.tk_popup(event.x_root, event.y_root)

    def _get_documento_contextual(self):
        selected_row = self.table_view.get_rows(selected=True)
        if not selected_row or not selected_row[0].values:
            return None
        id_documento = selected_row[0].values[0]
        return self.map_documentos.get(id_documento)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_buscar(self):
        """
        Manejador del evento de búsqueda. Obtiene el término y el campo de búsqueda,
        consulta la base de datos y puebla la tabla con los resultados.
        """
        campo_display = self.cbx_campos.get()
        termino = self.ent_buscar.get().strip()

        if not termino:
            showwarning("Búsqueda vacía", "Por favor, ingrese un término para buscar.")
            return

        # Mapeo del valor del combobox al nombre real de la columna en la BD
        mapa_campos = {
            "Título": "titulo",
            "Autores": "autores",
            "Editorial": "editorial",
            "ISBN": "isbn",
        }
        campo = mapa_campos.get(campo_display)

        resultados = Consulta().buscar_en_bibliografia(campo=campo, termino=termino)

        # Guardamos los datos para poder abrir el documento después
        self.map_documentos = {res["id_documento"]: res for res in resultados}

        self._poblar_tabla(resultados)

    def recargar_resultados(self):
        """
        Refresca la vista sin forzar advertencias de búsqueda vacía.
        Si hay término de búsqueda activo, vuelve a ejecutar la consulta.
        """
        termino = self.ent_buscar.get().strip()
        if termino:
            self.on_buscar()
        else:
            self.map_documentos.clear()
            self.table_view.delete_rows()

    def on_doble_clic_tabla(self, event=None):
        """
        Manejador del evento de doble clic en la tabla.
        Abre el documento correspondiente a la fila seleccionada.
        """
        self._abrir_documento_seleccionado()

    def _poblar_tabla(self, lista_resultados: List[Dict[str, Any]]) -> None:
        """Limpia y puebla la tabla con una lista de resultados bibliográficos.

        Args:
            lista_resultados (List[Dict[str, Any]]): La lista de diccionarios
                con los datos a mostrar.
        """
        self.table_view.delete_rows()
        if not lista_resultados:
            return

        # Insertar las filas una por una
        for res in lista_resultados:
            self.table_view.insert_row(values=self._formatear_fila(res))

        self.table_view.autoalign_columns()
        self.table_view.autofit_columns()

    def _abrir_documento_seleccionado(self) -> None:
        """
        Obtiene el documento de la fila seleccionada, construye su ruta y lo abre
        en el directorio temporal. Muestra errores si algo falla.
        """
        selected_row = self.table_view.get_rows(selected=True)
        if not selected_row:
            return

        id_documento = selected_row[0].values[0]
        documento_data = self.map_documentos.get(id_documento)

        if not documento_data:
            showerror(
                title="Error",
                message="No se encontró la información del documento.",
                parent=self.master,
            )
            return

        config = ConfiguracionController()
        ruta_biblioteca = config.obtener_ubicacion_biblioteca()
        if not ruta_biblioteca or not exists(ruta_biblioteca):
            showerror(
                title="Error",
                message="La ubicación de la biblioteca no está configurada o no existe.",
                parent=self.master,
            )
            return

        ok, error = abrir_documento_desde_biblioteca(
            id_documento=id_documento,
            nombre_documento=documento_data["nombre_doc"],
            extension_documento=documento_data["extension_doc"],
            ruta_biblioteca=ruta_biblioteca,
        )
        if not ok:
            showerror(title="Error al abrir", message=error, parent=self.master)

    def _formatear_fila(self, res: Dict[str, Any]) -> list:
        """Formatea un diccionario de resultado a una lista para la tabla.

        Args:
            res (Dict[str, Any]): Diccionario con los datos de un resultado de búsqueda.

        Returns:
            list: Una lista con los valores formateados para una fila de la tabla.
        """
        return [
            res.get("id_documento", "-"),
            self.icon_libro,
            res.get("titulo", "N/A"),
            res.get("autores", "N/A"),
            res.get("ano_publicacion", "-"),
            res.get("editorial", "N/A"),
            res.get("isbn", "N/A"),
            res.get("nombre_doc", ""),
            res.get("extension_doc", ""),
        ]
