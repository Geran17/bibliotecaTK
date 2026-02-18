from tkinter import Menu
from tkinter.messagebox import showerror, showwarning
from typing import Dict, Any, List, Optional

from ttkbootstrap import Button, Entry, Treeview

from models.controllers.controlar_menu_contextual_documento import (
    ControlarMenuContextualDocumento,
)
from models.entities.consulta import Consulta
from utilities.auxiliar import abrir_documento_desde_biblioteca


class ControlarVisualizarContenido:
    """
    Controlador para la lógica de la vista de búsqueda en contenido.
    """

    def __init__(self, tree_view: Treeview, ent_buscar: Entry, btn_buscar: Button, master):
        self.tree_view = tree_view
        self.ent_buscar = ent_buscar
        self.btn_buscar = btn_buscar
        self.master = master

        self.map_resultados: Dict[str, Dict[str, Any]] = {}
        self.map_documentos: Dict[int, Dict[str, str]] = {}

        self.menu_ops = ControlarMenuContextualDocumento(
            master=self.master,
            get_documento_data=self._obtener_datos_documento_seleccionado,
            on_refresh=self.recargar_resultados,
        )

        self._crear_menu_contextual()
        self._vincular_eventos()

    def _crear_menu_contextual(self):
        """Crea el menú contextual para el Treeview."""
        self.menu_contextual = Menu(self.master, tearoff=0)
        self.menu_contextual.add_command(label="📖 Abrir documento", command=self.on_doble_clic_tree)
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
        self.btn_buscar.config(command=self.on_buscar)
        self.ent_buscar.bind("<Return>", lambda event: self.on_buscar())
        self.tree_view.bind("<Double-1>", self.on_doble_clic_tree)
        self.tree_view.bind("<Button-3>", self._mostrar_menu_contextual)

    def _mostrar_menu_contextual(self, event):
        """Muestra el menú contextual en la posición del cursor."""
        iid = self.tree_view.identify_row(event.y)
        if iid:
            self.tree_view.selection_set(iid)
            self.tree_view.focus(iid)
            self.menu_contextual.post(event.x_root, event.y_root)

    def on_buscar(self):
        """Busca en el contenido y puebla el Treeview con los resultados."""
        termino = self.ent_buscar.get().strip()

        if not termino:
            showwarning("Búsqueda vacía", "Por favor, ingrese un término para buscar.")
            return

        resultados = Consulta().buscar_en_contenido(termino=termino)
        self._poblar_treeview(resultados)

    def recargar_resultados(self):
        """Recarga sin advertencias; limpia si no hay término activo."""
        termino = self.ent_buscar.get().strip()
        if termino:
            resultados = Consulta().buscar_en_contenido(termino=termino)
            self._poblar_treeview(resultados)
            return

        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        self.map_resultados.clear()
        self.map_documentos.clear()

    def _poblar_treeview(self, lista_resultados: List[Dict[str, Any]]):
        """Limpia y puebla el Treeview con una lista de resultados jerarquizados."""
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        self.map_resultados.clear()
        self.map_documentos.clear()

        if not lista_resultados:
            return

        documentos = {}
        for res in lista_resultados:
            id_doc = res["id_documento"]
            if id_doc not in documentos:
                documentos[id_doc] = {
                    "nombre": res["nombre_documento"],
                    "extension": res["extension_doc"],
                    "items": [],
                }
            documentos[id_doc]["items"].append(res)

        for id_doc, data in documentos.items():
            iid_doc = f"doc_{id_doc}"
            self.tree_view.insert("", "end", iid=iid_doc, text=f"📄 {data['nombre']}", open=True)

            for item in data["items"]:
                iid_item = f"{iid_doc}_{item['tipo'].lower()}_{item['id_item']}"
                self.tree_view.insert(
                    iid_doc,
                    "end",
                    iid=iid_item,
                    values=(item["tipo"], item["titulo_item"], item.get("pagina") or "-"),
                )
                self.map_resultados[iid_item] = item

            self.map_documentos[id_doc] = {
                "nombre_documento": data["nombre"],
                "extension_doc": data["extension"],
            }

    def _obtener_datos_documento_seleccionado(self) -> Optional[Dict[str, Any]]:
        iid_seleccionado = self.tree_view.focus()
        if not iid_seleccionado:
            return None

        if iid_seleccionado.startswith("doc_"):
            try:
                id_documento = int(iid_seleccionado.split("_", maxsplit=1)[1])
            except (ValueError, IndexError):
                return None

            data_doc = self.map_documentos.get(id_documento)
            if not data_doc:
                return None

            return {
                "id_documento": id_documento,
                "nombre_documento": data_doc["nombre_documento"],
                "extension_doc": data_doc["extension_doc"],
                "pagina": None,
            }

        return self.map_resultados.get(iid_seleccionado)

    def on_doble_clic_tree(self, event=None):
        """Abre el documento correspondiente al hacer doble clic en un resultado."""
        resultado = self._obtener_datos_documento_seleccionado()
        if not resultado:
            return

        ok, error = abrir_documento_desde_biblioteca(
            id_documento=resultado["id_documento"],
            nombre_documento=resultado["nombre_documento"],
            extension_documento=resultado["extension_doc"],
            pagina=resultado.get("pagina"),
        )
        if not ok:
            showerror("Error al abrir", error)
