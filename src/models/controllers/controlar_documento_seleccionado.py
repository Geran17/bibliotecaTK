from ttkbootstrap.tableview import Tableview
from ttkbootstrap import Button, IntVar, StringVar
from typing import Dict, Any, Optional
from tkinter.messagebox import showerror, showwarning
from models.entities.documento import Documento
from models.entities.bibliografia import Bibliografia
from os.path import join, exists
from pathlib import Path
from utilities.configuracion import DIRECTORIO_TEMPORAL
from models.controllers.configuracion_controller import ConfiguracionController
from utilities.auxiliar import (
    generar_ruta_documento,
    abrir_archivo,
    copiar_archivo,
    renombrar_archivo,
    mover_archivo,
    papelera_archivo,
    eliminar_archivo,
)
from views.dialogs.dialog_visualizar_metadatos import DialogVisualizarMetadatos


class ControlarDocumentoSeleccionado:
    def __init__(
        self,
        table_view: Tableview,
        map_vars: Dict[str, Any] = {},
        map_widgets: Dict[str, Any] = {},
        master=None,
    ):
        self.table_view: Tableview = table_view
        self.map_vars = map_vars
        self.map_widgets = map_widgets
        self.master = master

        # variables
        self.documento: Documento = None
        self.selected_item = ()
        self.ruta_biblioteca: str = None
        self.ruta_documento: str = None

        # Maps
        # map_widgets
        self.btn_abrir: Button = self.map_widgets['btn_abrir']
        self.btn_abrir_carpeta: Button = self.map_widgets['btn_abrir_carpeta']
        self.btn_renombrar: Button = self.map_widgets['btn_renombrar']
        self.btn_copiar: Button = self.map_widgets['btn_copiar']
        self.btn_mover: Button = self.map_widgets['btn_mover']
        self.btn_eliminar: Button = self.map_widgets['btn_eliminar']
        self.btn_papelera: Button = self.map_widgets['btn_papelera']
        self.btn_propiedades: Button = self.map_widgets['btn_propiedades']
        self.btn_metadatos: Button = self.map_widgets['btn_metadatos']
        self.btn_renombrar_bibliografico: Button = self.map_widgets['btn_renombrar_bibliografico']

        # map_vars
        self.var_id_documento: IntVar = self.map_vars['id_documento']
        self.var_nombre_documento: StringVar = self.map_vars['nombre_documento']

        conf = ConfiguracionController()
        self.ruta_biblioteca = conf.obtener_ubicacion_biblioteca()

        # Vincular evento de doble clic
        self.table_view.view.bind("<Double-Button-1>", self.on_double_click_table_view)
        self.btn_abrir.config(command=self.on_abrir_documento)
        self.btn_abrir_carpeta.config(command=self.on_abrir_carpeta)
        self.btn_renombrar.config(command=self.on_renombrar)
        self.btn_mover.config(command=self.on_mover)
        self.btn_eliminar.config(command=self.on_eliminar)
        self.btn_papelera.config(command=self.on_papelera)
        self.btn_metadatos.config(command=self.on_visualizar_metadatos)
        self.btn_renombrar_bibliografico.config(command=self.on_renombrar_bibliografico)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘

    def _set_documento(self):
        self.selected_item = self.table_view.view.selection()
        if self.selected_item:
            # Obtener el ID del item seleccionado
            item_id = self.selected_item[0]

            # Opción 1: Obtener valores directamente del treeview (RECOMENDADO)
            values = self.table_view.view.item(item_id)['values']

            # O Opción 2: Convertir el ID a índice numérico
            # all_items = self.table_view.view.get_children()
            # row_index = all_items.index(item_id)
            # values = self.table_view.get_row(row_index).values

            if values:
                self.documento = Documento(
                    id=values[0],
                    nombre=values[3],
                    hash=values[9],
                    extension=values[4],
                    creado_en="",
                    actualizado_en="",
                    tamano=0,
                    esta_activo=True,
                )
                if self.documento.instanciar():
                    self.var_id_documento.set(value=self.documento.id)
                    self.var_nombre_documento.set(value=self.documento.nombre)
                    self.ruta_documento = generar_ruta_documento(
                        ruta_biblioteca=self.ruta_biblioteca,
                        nombre_documento=f"{self.documento.nombre}.{self.documento.extension}",
                        id_documento=self.documento.id,
                    )

    def _actualizar_fila_tabla(self):
        """
        Actualiza solo la fila seleccionada en la tabla con los nuevos valores
        del documento, manteniendo la selección actual.
        """
        if not self.selected_item:
            return

        item_id = self.selected_item[0]

        # Obtener los valores actuales de la fila
        values = list(self.table_view.view.item(item_id)['values'])

        # Actualizar solo el valor del nombre (índice 3 según _set_documento)
        values[3] = self.documento.nombre

        # Actualizar la fila en el treeview
        self.table_view.view.item(item_id, values=values)

        # Mantener la selección
        self.table_view.view.selection_set(item_id)
        self.table_view.view.focus(item_id)

    def _generar_nombre_bibliografico(
        self, bibliografia: Bibliografia, estilo: str
    ) -> Optional[str]:
        """Genera un nombre de archivo basado en el estilo de citación."""
        autores = bibliografia.autores.split(',')[0] if bibliografia.autores else "Anonimo"
        ano = bibliografia.ano_publicacion or "s.f."  # s.f. = sin fecha
        titulo = bibliografia.titulo or "Sin Titulo"

        # Truncar partes largas para evitar nombres de archivo excesivos
        autores = (autores[:25] + '...') if len(autores) > 25 else autores
        titulo = (titulo[:50] + '...') if len(titulo) > 50 else titulo

        nuevo_nombre = ""
        if estilo == "APA":
            nuevo_nombre = f"{autores} ({ano}) {titulo}"
        elif estilo == "MLA":
            nuevo_nombre = f"{autores} - {titulo}"
        elif estilo == "Chicago":
            nuevo_nombre = f"{autores} - {titulo} ({ano})"
        elif estilo == "Harvard":
            nuevo_nombre = f"{autores} ({ano}) {titulo}"
        elif estilo == "Vancouver":
            nuevo_nombre = f"{autores} - {titulo}"
        else:
            # Estilo por defecto o desconocido
            nuevo_nombre = f"{autores} - {titulo}"

        # Limpiar caracteres inválidos para nombres de archivo
        caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in caracteres_invalidos:
            nuevo_nombre = nuevo_nombre.replace(char, '')

        # Reemplazar múltiples espacios con uno solo
        nuevo_nombre = ' '.join(nuevo_nombre.split())

        return nuevo_nombre

    def _actualizar_y_renombrar(self, nuevo_nombre: str):
        """Función auxiliar para encapsular la lógica de renombrado."""
        self.var_nombre_documento.set(nuevo_nombre)
        # Llama a la lógica de renombrado existente con el nuevo nombre
        self.on_renombrar()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘
    def on_abrir_carpeta(self):
        pass

    def on_double_click_table_view(self, event):
        self._set_documento()

    def on_abrir_documento(self):
        """
        Placeholder para la lógica de abrir el documento seleccionado.
        Los documentos e abriran en la carpeta temporal del sistema.
        """
        if self.documento:
            doc = self.documento
            ruta_destino = join(DIRECTORIO_TEMPORAL, f"{doc.nombre}.{doc.extension}")
            if not exists(self.ruta_documento):
                showerror(
                    title="Error",
                    message=f"El documento no existe en la biblioteca: {self.ruta_documento}",
                )
                return
            # copiamos el documento en la carpeta temporal
            try:
                copiar_archivo(ruta_origen=self.ruta_documento, ruta_destino=ruta_destino)
            except Exception as e:
                print(f"Error al copiar el documento: {e}")
                return
            # abrimos el documento en la carpeta temporal
            abrir_archivo(ruta_origen=ruta_destino)
        else:
            showwarning(
                title="Seleccione el documento",
                message="Error: No hay documento seleccionado para abrir. Doble click para seleccionar",
                icon="warning",
                parent=self.master,
            )

    def on_abrir_carpeta(self):
        if self.documento:
            path_parent = Path(self.ruta_documento).parent
            if exists(path_parent):
                abrir_archivo(ruta_origen=path_parent)
        else:
            showwarning(
                title="Seleccione el documento",
                message="Error: No hay documento seleccionado para abrir. Doble click para seleccionar",
                icon="warning",
            )

    def on_visualizar_metadatos(self):
        """Abre el dialog para visualizar los metadatos del documento seleccionado."""
        if self.documento:
            dialog = DialogVisualizarMetadatos(title="Metadatos del Documento")
            dialog.set_documento(self.documento)
            dialog.grab_set()
        else:
            showwarning(
                title="Seleccione el documento",
                message="Error: No hay documento seleccionado para visualizar metadatos. Doble click para seleccionar",
                icon="warning",
                parent=self.master,
            )

    def on_renombrar_bibliografico(self):
        """
        Renombra el documento seleccionado utilizando sus datos bibliográficos
        y el estilo de citación configurado.
        """
        if not self.documento:
            showwarning(
                title="Seleccione Documento",
                message="Por favor, seleccione un documento para renombrar.",
                parent=self.master,
            )
            return

        # 1. Verificar si existen datos bibliográficos
        bibliografia = Bibliografia(id_documento=self.documento.id, titulo="")
        if not bibliografia.instanciar():
            showerror(
                title="Sin Datos Bibliográficos",
                message="El documento no tiene información bibliográfica para poder renombrarlo.",
                parent=self.master,
            )
            return

        # 2. Obtener el estilo de citación
        config = ConfiguracionController()
        estilo = config.obtener_estilo_citacion() or "APA"  # APA por defecto

        # 3. Generar el nuevo nombre
        nuevo_nombre = self._generar_nombre_bibliografico(bibliografia, estilo)

        if nuevo_nombre:
            # 4. Ejecutar el renombrado
            self._actualizar_y_renombrar(nuevo_nombre)

    def on_renombrar(self):
        if not self.documento:
            showwarning(
                title="Seleccione el documento",
                message="Error: No hay documento seleccionado para renombrar. Doble click para seleccionar",
                icon="warning",
                parent=self.master,
            )
            return

        # Validar que el archivo existe
        if not exists(self.ruta_documento):
            showerror(
                title="Error",
                message=f"El documento no existe en la biblioteca: {self.ruta_documento}",
                parent=self.master,
            )
            return

        # Obtener datos de los campos
        var_nombre = self.var_nombre_documento.get().strip()
        var_id = self.var_id_documento.get()

        # Validar nombre no vacío
        if not var_nombre:
            showwarning(
                title="Nombre vacío",
                message="El nombre del documento no puede estar vacío",
                parent=self.master,
            )
            return

        # Validar caracteres inválidos en el nombre
        caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in var_nombre for char in caracteres_invalidos):
            showwarning(
                title="Nombre inválido",
                message=f"El nombre no puede contener los siguientes caracteres: {' '.join(caracteres_invalidos)}",
                parent=self.master,
            )
            return

        # Guardar datos anteriores
        ruta_origen = self.ruta_documento
        ruta_padre = Path(self.ruta_documento).parent
        nombre_anterior = self.documento.nombre

        # Si el nombre no cambió, no hacer nada
        if var_nombre == nombre_anterior:
            return

        # Actualizar el nombre en el objeto
        self.documento.nombre = var_nombre

        # Intentar actualizar en la base de datos
        if not self.documento.actualizar():
            showerror(
                title="Error de base de datos",
                message="No se pudo actualizar el documento en la base de datos",
                parent=self.master,
            )
            self.documento.nombre = nombre_anterior  # Revertir cambio
            return

        # Construir rutas
        nuevo_nombre = f"{var_id}_{var_nombre}.{self.documento.extension}"
        ruta_destino = join(ruta_padre, nuevo_nombre)

        # Validar que no exista ya un archivo con ese nombre
        if exists(ruta_destino):
            showerror(
                title="Archivo existente",
                message=f"Ya existe un archivo con el nombre: {nuevo_nombre}",
                parent=self.master,
            )
            # Revertir cambio en BD
            self.documento.nombre = nombre_anterior
            self.documento.actualizar()
            return

        # Intentar renombrar el archivo
        try:
            renombrar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino)
            # Actualizar la ruta del documento en memoria
            self.ruta_documento = ruta_destino

            # Refrescar la fila en la tabla sin perder la selección
            self._actualizar_fila_tabla()

        except Exception as e:
            # Revertir cambios si falla el renombrado
            self.documento.nombre = nombre_anterior
            self.documento.actualizar()
            showerror(
                title="Error al renombrar",
                message=f"No se pudo renombrar el archivo: {str(e)}",
                parent=self.master,
            )

    def on_mover(self):
        """
        Mueve el documento seleccionado fuera de la biblioteca.
        El archivo se mueve sin el ID en el nombre y se elimina de la base de datos.
        """
        if not self.documento:
            showwarning(
                title="Seleccione el documento",
                message="Error: No hay documento seleccionado para mover. Doble click para seleccionar",
                icon="warning",
                parent=self.master,
            )
            return

        # Validar que el archivo existe
        if not exists(self.ruta_documento):
            showerror(
                title="Error",
                message=f"El documento no existe en la biblioteca: {self.ruta_documento}",
                parent=self.master,
            )
            return

        # Seleccionar carpeta de destino fuera de la biblioteca
        from tkinter.filedialog import askdirectory

        ruta_destino_carpeta = askdirectory(
            title="Seleccione la carpeta de destino (fuera de la biblioteca)",
            parent=self.master,
        )

        if not ruta_destino_carpeta:
            # Usuario canceló la selección
            return

        # Validar que la carpeta de destino NO esté dentro de la biblioteca
        if ruta_destino_carpeta.startswith(self.ruta_biblioteca):
            showerror(
                title="Carpeta inválida",
                message="La carpeta de destino debe estar fuera de la biblioteca",
                parent=self.master,
            )
            return

        # Construir la ruta completa del archivo de destino SIN el ID
        nombre_archivo = f"{self.documento.nombre}.{self.documento.extension}"
        ruta_destino = join(ruta_destino_carpeta, nombre_archivo)

        # Validar que no exista ya un archivo en el destino
        if exists(ruta_destino):
            showerror(
                title="Archivo existente",
                message=f"Ya existe un archivo en la ubicación de destino: {nombre_archivo}",
                parent=self.master,
            )
            return

        # Confirmar movimiento
        from tkinter.messagebox import askyesno

        confirmacion = askyesno(
            title="Confirmar movimiento",
            message=f"¿Desea mover '{nombre_archivo}' fuera de la biblioteca?\n\nEl documento se eliminará de la base de datos.",
            parent=self.master,
        )

        if not confirmacion:
            return

        # Intentar mover el archivo
        try:
            mover_archivo(ruta_origen=self.ruta_documento, ruta_destino=ruta_destino)

            # Si el movimiento fue exitoso, eliminar de la base de datos
            try:
                if not self.documento.eliminar():
                    showwarning(
                        title="Advertencia",
                        message="El archivo se movió correctamente, pero no se pudo eliminar de la base de datos",
                        parent=self.master,
                    )
                    return

                # Remover el item de la tabla
                if self.selected_item:
                    item_id = self.selected_item[0]
                    self.table_view.view.delete(item_id)

                # Limpiar selección
                self.documento = None
                self.selected_item = ()
                self.ruta_documento = None
                self.var_id_documento.set(0)
                self.var_nombre_documento.set("")

            except Exception as e:
                showerror(
                    title="Error al eliminar de la base de datos",
                    message=f"El archivo se movió, pero ocurrió un error al eliminar de la BD: {str(e)}",
                    parent=self.master,
                )

        except Exception as e:
            showerror(
                title="Error al mover",
                message=f"No se pudo mover el archivo: {str(e)}",
                parent=self.master,
            )

    def on_eliminar(self):
        """
        Elimina permanentemente el documento seleccionado del sistema de archivos
        y de la base de datos. Esta acción no se puede deshacer.
        """
        if not self.documento:
            showwarning(
                title="Seleccione el documento",
                message="Error: No hay documento seleccionado para eliminar. Doble click para seleccionar",
                icon="warning",
                parent=self.master,
            )
            return

        # Validar que el archivo existe
        if not exists(self.ruta_documento):
            showwarning(
                title="Advertencia",
                message=f"El documento no existe en el sistema de archivos: {self.ruta_documento}",
                parent=self.master,
            )
            # Continuar para eliminar de la BD de todos modos

        # Confirmar eliminación
        from tkinter.messagebox import askyesno

        confirmacion = askyesno(
            title="Confirmar eliminación",
            message=f"¿Está seguro de que desea eliminar permanentemente '{self.documento.nombre}.{self.documento.extension}'?\n\nEsta acción no se puede deshacer.",
            icon="warning",
            parent=self.master,
        )

        if not confirmacion:
            return

        # Guardar datos por si necesitamos revertir
        documento_id = self.documento.id

        # Intentar eliminar el archivo físico
        archivo_eliminado = False
        if exists(self.ruta_documento):
            try:
                eliminar_archivo(ruta_destino=self.ruta_documento)
                archivo_eliminado = True
            except Exception as e:
                showerror(
                    title="Error al eliminar archivo",
                    message=f"No se pudo eliminar el archivo: {str(e)}",
                    parent=self.master,
                )
                return

        # Intentar eliminar de la base de datos
        try:
            if not self.documento.eliminar():
                # Si falla la eliminación de BD, intentar restaurar el archivo
                # (esto sería complejo, mejor prevenir)
                showerror(
                    title="Error de base de datos",
                    message="No se pudo eliminar el documento de la base de datos",
                    parent=self.master,
                )
                return

            # Remover el item de la tabla
            if self.selected_item:
                item_id = self.selected_item[0]
                self.table_view.view.delete(item_id)

            # Limpiar selección
            self.documento = None
            self.selected_item = ()
            self.ruta_documento = None
            self.var_id_documento.set(0)
            self.var_nombre_documento.set("")

        except Exception as e:
            showerror(
                title="Error al eliminar",
                message=f"Error inesperado: {str(e)}",
                parent=self.master,
            )

    def on_papelera(self):
        """
        Mueve el documento seleccionado a la papelera de reciclaje del sistema.
        El archivo puede ser recuperado desde la papelera.
        """
        if not self.documento:
            showwarning(
                title="Seleccione el documento",
                message="Error: No hay documento seleccionado para enviar a la papelera. Doble click para seleccionar",
                icon="warning",
                parent=self.master,
            )
            return

        # Validar que el archivo existe
        if not exists(self.ruta_documento):
            showerror(
                title="Error",
                message=f"El documento no existe en la biblioteca: {self.ruta_documento}",
                parent=self.master,
            )
            return

        # Confirmar envío a papelera
        from tkinter.messagebox import askyesno

        confirmacion = askyesno(
            title="Confirmar envío a papelera",
            message=f"¿Desea enviar '{self.documento.nombre}.{self.documento.extension}' a la papelera de reciclaje?",
            parent=self.master,
        )

        if not confirmacion:
            return

        # Intentar enviar a la papelera
        try:
            papelera_archivo(ruta_origen=self.ruta_documento)

            # Marcar como inactivo en la base de datos en lugar de eliminar
            # (o eliminar, según tu lógica de negocio)
            self.documento.esta_activo = False
            if not self.documento.actualizar():
                showwarning(
                    title="Advertencia",
                    message="El archivo se movió a la papelera, pero no se pudo actualizar el estado en la base de datos",
                    parent=self.master,
                )

            # Remover el item de la tabla
            if self.selected_item:
                item_id = self.selected_item[0]
                self.table_view.view.delete(item_id)

            # Limpiar selección
            self.documento = None
            self.selected_item = ()
            self.ruta_documento = None
            self.var_id_documento.set(0)
            self.var_nombre_documento.set("")

        except Exception as e:
            showerror(
                title="Error al enviar a papelera",
                message=f"No se pudo enviar el archivo a la papelera: {str(e)}",
                parent=self.master,
            )
