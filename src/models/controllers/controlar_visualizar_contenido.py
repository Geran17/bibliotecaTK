from os.path import exists
from tkinter.messagebox import showerror, showwarning, askyesno
from tkinter.filedialog import asksaveasfilename
from typing import Dict, Any, List
from tkinter import Menu

from ttkbootstrap import Button, Entry, Treeview

from models.controllers.configuracion_controller import ConfiguracionController
from models.entities.consulta import Consulta
from models.entities.documento import Documento
from utilities.auxiliar import (
    abrir_documento_desde_biblioteca,
    generar_ruta_documento,
    copiar_archivo,
)


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

        self._crear_menu_contextual()
        self._vincular_eventos()

    def _crear_menu_contextual(self):
        """Crea el menú contextual para el Treeview."""
        self.menu_contextual = Menu(self.master, tearoff=0)
        self.menu_contextual.add_command(
            label="📋 Copiar documento", command=self._on_copiar_documento
        )
        self.menu_contextual.add_command(
            label="🗑️ Eliminar documento", command=self._on_eliminar_documento
        )
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="🔄 Cambiar estado", command=self._on_cambiar_estado)

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

    def _poblar_treeview(self, lista_resultados: List[Dict[str, Any]]):
        """Limpia y puebla el Treeview con una lista de resultados jerarquizados."""
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        self.map_resultados.clear()

        if not lista_resultados:
            return

        # Agrupar resultados por documento
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

        # Poblar el Treeview
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

    def on_doble_clic_tree(self, event=None):
        """Abre el documento correspondiente al hacer doble clic en un resultado."""
        iid_seleccionado = self.tree_view.focus()
        if not iid_seleccionado or iid_seleccionado.startswith("doc_"):
            return  # Ignorar clics en los nodos de documento

        resultado = self.map_resultados.get(iid_seleccionado)
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

    def _on_copiar_documento(self):
        """Copia el documento seleccionado a una ubicación externa."""
        iid_seleccionado = self.tree_view.focus()
        if not iid_seleccionado or iid_seleccionado.startswith("doc_"):
            return

        resultado = self.map_resultados.get(iid_seleccionado)
        if not resultado:
            return

        nombre_archivo = f"{resultado['nombre_documento']}.{resultado['extension_doc']}"
        ruta_destino = asksaveasfilename(
            defaultextension=f".{resultado['extension_doc']}",
            initialfile=nombre_archivo,
            title="Copiar documento a...",
        )
        if not ruta_destino:
            return

        config = ConfiguracionController()
        ruta_biblioteca = config.obtener_ubicacion_biblioteca()
        ruta_origen = generar_ruta_documento(
            ruta_biblioteca, resultado["id_documento"], nombre_archivo
        )

        if not exists(ruta_origen):
            showerror("Archivo no encontrado", f"El archivo no se encontró:\n{ruta_origen}")
            return

        try:
            copiar_archivo(ruta_origen, ruta_destino)
            showwarning("Copia exitosa", f"Documento copiado a:\n{ruta_destino}")
        except Exception as e:
            showerror("Error al copiar", f"No se pudo copiar el documento: {e}")

    def _on_eliminar_documento(self):
        """Elimina el documento seleccionado de la biblioteca y base de datos."""
        iid_seleccionado = self.tree_view.focus()
        if not iid_seleccionado or iid_seleccionado.startswith("doc_"):
            return

        resultado = self.map_resultados.get(iid_seleccionado)
        if not resultado:
            return

        respuesta = askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el documento '{resultado['nombre_documento']}'?\nEsta acción no se puede deshacer.",
        )
        if not respuesta:
            return

        doc = Documento(id=resultado["id_documento"], nombre="", extension="", hash="", tamano=0)
        if doc.instanciar() and doc.eliminar():
            # Actualizar el treeview eliminando el documento
            self.tree_view.delete(f"doc_{resultado['id_documento']}")
            showwarning("Eliminación exitosa", "Documento eliminado de la biblioteca.")
        else:
            showerror("Error", "No se pudo eliminar el documento.")

    def _on_cambiar_estado(self):
        """Cambia el estado activo/inactivo del documento."""
        iid_seleccionado = self.tree_view.focus()
        if not iid_seleccionado or iid_seleccionado.startswith("doc_"):
            return

        resultado = self.map_resultados.get(iid_seleccionado)
        if not resultado:
            return

        doc = Documento(id=resultado["id_documento"], nombre="", extension="", hash="", tamano=0)
        if doc.instanciar():
            nuevo_estado = not doc.esta_activo
            doc.esta_activo = nuevo_estado
            if doc.actualizar():
                estado_texto = "activado" if nuevo_estado else "desactivado"
                showwarning("Estado cambiado", f"Documento {estado_texto}.")
            else:
                showerror("Error", "No se pudo cambiar el estado del documento.")
        else:
            showerror("Error", "No se pudo cargar el documento.")
