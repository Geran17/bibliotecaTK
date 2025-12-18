from os.path import join, exists
from tkinter.messagebox import showerror
from tkinter.ttk import Treeview
from typing import Dict, Any, List

from ttkbootstrap.tableview import Tableview

from models.controllers.configuracion_controller import ConfiguracionController
from models.entities.consulta import Consulta
from utilities.auxiliar import generar_ruta_documento, copiar_archivo, abrir_archivo
from utilities.configuracion import DIRECTORIO_TEMPORAL


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

        self._vincular_eventos()
        self._poblar_treeview()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Privados
    # └────────────────────────────────────────────────────────────┘

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a sus manejadores."""
        self.tree_view.bind("<<TreeviewSelect>>", self.on_seleccionar_clave)
        self.table_view.view.bind("<Double-1>", self.on_doble_clic_tabla)

    def _poblar_treeview(self):
        """
        Obtiene las claves de metadatos y las organiza jerárquicamente en el Treeview.
        """
        consulta = Consulta()
        metadatos_agrupados = consulta.get_metadatos_agrupados_con_conteo()

        grupos = {}
        claves = {}
        for item in metadatos_agrupados:
            if ":" in item["clave"]:
                grupo, nombre_clave = item["clave"].split(":", 1)
                clave_completa = item["clave"]

                # Insertar grupo si no existe
                if grupo not in grupos:
                    grupos[grupo] = self.tree_view.insert("", "end", text=grupo, open=False)

                # Insertar clave si no existe
                if clave_completa not in claves:
                    claves[clave_completa] = self.tree_view.insert(
                        grupos[grupo], "end", text=nombre_clave, open=False
                    )

                # Insertar valor como hijo de la clave
                texto_valor = f"{item['valor']} ({item['total']})"
                self.tree_view.insert(
                    claves[clave_completa],
                    "end",
                    text=texto_valor,
                    values=(clave_completa, item["valor"]),
                )
            else:
                # Lógica para claves sin grupo (si es necesario)
                pass

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

    def _abrir_documento_seleccionado(self):
        """
        Obtiene el documento de la fila seleccionada, construye su ruta y lo abre.
        """
        selected_row = self.table_view.get_rows(selected=True)
        if not selected_row:
            return

        id_documento = selected_row[0].values[0]
        documento_data = self.map_documentos.get(id_documento)

        if not documento_data:
            showerror("Error", "No se encontró la información del documento.", parent=self.master)
            return

        config = ConfiguracionController()
        ruta_biblioteca = config.obtener_ubicacion_biblioteca()
        if not ruta_biblioteca or not exists(ruta_biblioteca):
            showerror(
                "Error", "La ubicación de la biblioteca no está configurada.", parent=self.master
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
                "Archivo no encontrado",
                f"El archivo no se encontró en:\n{ruta_origen}",
                parent=self.master,
            )
            return

        ruta_destino_temporal = join(DIRECTORIO_TEMPORAL, nombre_archivo)
        try:
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino_temporal)
            abrir_archivo(ruta_origen=ruta_destino_temporal)
        except Exception as e:
            showerror("Error al abrir", f"No se pudo abrir el documento: {e}", parent=self.master)

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

        # Si es un grupo (sin padre) o una clave (su padre no tiene padre), no hacer nada.
        if self.tree_view.parent(selected_item) == "" or parent_de_parent == "":
            self.table_view.delete_rows()
            return

        # Es un nodo de valor, obtenemos clave y valor
        values = self.tree_view.item(selected_item, "values")
        clave_completa, valor = values[0], values[1]

        documentos = Consulta().get_documentos_por_clave_metadato(clave=clave_completa, valor=valor)
        self._poblar_tabla(documentos)

    def on_doble_clic_tabla(self, event=None):
        """Manejador del evento de doble clic en la tabla de documentos."""
        self._abrir_documento_seleccionado()
