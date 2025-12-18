from os.path import join, exists
from tkinter.messagebox import showerror, showwarning
from typing import Dict, Any, List

from ttkbootstrap import Button, Entry, Treeview

from models.controllers.configuracion_controller import ConfiguracionController
from models.entities.consulta import Consulta
from utilities.auxiliar import (
    generar_ruta_documento,
    copiar_archivo,
    abrir_archivo,
)
from utilities.configuracion import DIRECTORIO_TEMPORAL


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

        self._vincular_eventos()

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a sus manejadores."""
        self.btn_buscar.config(command=self.on_buscar)
        self.ent_buscar.bind("<Return>", lambda event: self.on_buscar())
        self.tree_view.bind("<Double-1>", self.on_doble_clic_tree)

    def on_buscar(self):
        """Busca en el contenido y puebla el Treeview con los resultados."""
        termino = self.ent_buscar.get().strip()

        if not termino:
            showwarning("Búsqueda vacía", "Por favor, ingrese un término para buscar.")
            return

        resultados = Consulta().buscar_en_contenido(termino=termino)
        self._poblar_treeview(resultados)

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

        config = ConfiguracionController()
        ruta_biblioteca = config.obtener_ubicacion_biblioteca()
        nombre_archivo = f"{resultado['nombre_documento']}.{resultado['extension_doc']}"
        ruta_origen = generar_ruta_documento(
            ruta_biblioteca, resultado["id_documento"], nombre_archivo
        )

        if not exists(ruta_origen):
            showerror("Archivo no encontrado", f"El archivo no se encontró:\n{ruta_origen}")
            return

        ruta_destino_temporal = join(DIRECTORIO_TEMPORAL, nombre_archivo)
        try:
            copiar_archivo(ruta_origen, ruta_destino_temporal)
            abrir_archivo(ruta_destino_temporal, pagina=resultado.get("pagina"))
        except Exception as e:
            showerror("Error al abrir", f"No se pudo abrir el documento: {e}")
