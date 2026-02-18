from tkinter import Menu
from tkinter.ttk import Treeview
from typing import Dict, Any, List, Optional

from ttkbootstrap.tableview import Tableview

from models.controllers.controlar_menu_contextual_documento import (
    ControlarMenuContextualDocumento,
)
from models.entities.consulta import Consulta


class ControlarVisorMetadatos:
    """
    Controlador para la lógica de la vista de exploración de metadatos.
    """

    def __init__(self, tree_view: Treeview, table_view: Tableview, master):
        self.tree_view = tree_view
        self.table_view = table_view
        self.master = master

        self.map_documentos: Dict[int, Dict[str, Any]] = {}
        self.icon_doc = "📄"

        self.menu_ops = ControlarMenuContextualDocumento(
            master=self.master,
            get_documento_data=self._get_documento_contextual,
            on_refresh=self._refrescar_tabla_actual,
        )

        self._crear_menu_contextual()
        self._vincular_eventos()
        self._poblar_treeview()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Privados
    # └────────────────────────────────────────────────────────────┘

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

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a sus manejadores."""
        self.tree_view.bind("<<TreeviewSelect>>", self.on_seleccionar_clave)
        self.table_view.view.bind("<Double-1>", self.on_doble_clic_tabla)
        self.table_view.view.bind("<Button-3>", self._mostrar_menu_contextual_tabla)

    def _mostrar_menu_contextual_tabla(self, event):
        item_id = self.table_view.view.identify_row(event.y)
        if not item_id:
            return
        self.table_view.view.selection_set(item_id)
        self.table_view.view.focus(item_id)
        self.menu_contextual.post(event.x_root, event.y_root)

    def _poblar_treeview(self):
        """
        Obtiene las claves de metadatos y las organiza jerárquicamente en el Treeview.
        """
        metadatos_agrupados = Consulta().get_metadatos_agrupados_con_conteo()

        grupos = {}
        claves = {}
        for item in metadatos_agrupados:
            if ":" not in item["clave"]:
                continue

            grupo, nombre_clave = item["clave"].split(":", 1)
            clave_completa = item["clave"]

            if grupo not in grupos:
                grupos[grupo] = self.tree_view.insert("", "end", text=grupo, open=False)

            if clave_completa not in claves:
                claves[clave_completa] = self.tree_view.insert(
                    grupos[grupo], "end", text=nombre_clave, open=False
                )

            texto_valor = f"{item['valor']} ({item['total']})"
            self.tree_view.insert(
                claves[clave_completa],
                "end",
                text=texto_valor,
                values=(clave_completa, item["valor"]),
            )

    def _poblar_tabla(self, lista_documentos: List[Dict[str, Any]]):
        """Limpia y puebla la tabla con una lista de documentos."""
        self.table_view.delete_rows()
        self.map_documentos.clear()

        if not lista_documentos:
            return

        self.map_documentos = {doc["id"]: doc for doc in lista_documentos}

        for doc in lista_documentos:
            fila = [
                doc.get("id", "-"),
                self.icon_doc,
                doc.get("nombre", "N/A"),
                doc.get("extension", "N/A"),
                doc.get("tamano", 0),
            ]
            self.table_view.insert_row(values=fila)

        self.table_view.autofit_columns()

    def _get_documento_contextual(self) -> Optional[Dict[str, Any]]:
        selected_row = self.table_view.get_rows(selected=True)
        if not selected_row or not selected_row[0].values:
            return None
        id_documento = selected_row[0].values[0]
        return self.map_documentos.get(id_documento)

    def _refrescar_tabla_actual(self):
        self.on_seleccionar_clave()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_seleccionar_clave(self, event=None):
        """
        Manejador del evento de selección en el Treeview. Si se selecciona una
        clave hija, busca y muestra los documentos asociados.
        """
        selected_item = self.tree_view.focus()
        if not selected_item:
            return

        parent_de_parent = self.tree_view.parent(self.tree_view.parent(selected_item))

        if self.tree_view.parent(selected_item) == "" or parent_de_parent == "":
            self.table_view.delete_rows()
            return

        values = self.tree_view.item(selected_item, "values")
        clave_completa, valor = values[0], values[1]

        documentos = Consulta().get_documentos_por_clave_metadato(clave=clave_completa, valor=valor)
        self._poblar_tabla(documentos)

    def on_doble_clic_tabla(self, event=None):
        """Manejador del evento de doble clic en la tabla de documentos."""
        self.menu_ops.on_abrir_documento()
