from os.path import exists, join
from pathlib import Path
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno, showerror, showinfo, showwarning
from typing import Callable, Dict, Any, Optional

from models.controllers.configuracion_controller import ConfiguracionController
from models.controllers.controlar_comentarios import ControlarComentarios
from models.entities.bibliografia import Bibliografia
from models.entities.documento import Documento
from utilities.auxiliar import (
    abrir_archivo,
    abrir_documento_desde_biblioteca,
    copiar_archivo,
    eliminar_archivo,
    generar_ruta_documento,
    mover_archivo,
    papelera_archivo,
    renombrar_archivo,
)
from views.components.resizable_input_dialog import ask_resizable_string
from views.components.resizable_text_dialog import ask_resizable_text
from views.dialogs.dialog_visualizar_metadatos import DialogVisualizarMetadatos


class ControlarMenuContextualDocumento:
    """
    Servicio reutilizable para aplicar operaciones contextuales sobre un
    documento seleccionado.
    """

    def __init__(
        self,
        master,
        get_documento_data: Callable[[], Optional[Dict[str, Any]]],
        on_refresh: Optional[Callable[[], None]] = None,
    ):
        self.master = master
        self.get_documento_data = get_documento_data
        self.on_refresh = on_refresh
        self.comentarios = ControlarComentarios()

    def _normalizar_documento_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not data:
            return None

        id_documento = data.get("id_documento", data.get("id"))
        nombre_documento = data.get("nombre_documento", data.get("nombre", data.get("nombre_doc")))
        extension_doc = data.get("extension_doc", data.get("extension"))

        if id_documento is None or not nombre_documento or not extension_doc:
            return None

        return {
            "id_documento": int(id_documento),
            "nombre_documento": str(nombre_documento),
            "extension_doc": str(extension_doc),
        }

    def _get_documento_instanciado(self) -> Optional[Documento]:
        data = self.get_documento_data()
        normalizado = self._normalizar_documento_data(data) if data else None
        if not normalizado:
            return None

        documento = Documento(
            id=normalizado["id_documento"],
            nombre=normalizado["nombre_documento"],
            extension=normalizado["extension_doc"],
            hash="",
            tamano=0,
        )
        if not documento.instanciar():
            showerror("Error", "No se pudo cargar el documento desde la base de datos.", parent=self.master)
            return None
        return documento

    def _get_ruta_documento(self, documento: Documento) -> Optional[str]:
        ruta_biblioteca = ConfiguracionController().obtener_ubicacion_biblioteca()
        if not ruta_biblioteca:
            return None
        return generar_ruta_documento(
            ruta_biblioteca=ruta_biblioteca,
            id_documento=documento.id,
            nombre_documento=f"{documento.nombre}.{documento.extension}",
        )

    def _formatear_tamano(self, bytes_value: int) -> str:
        if not bytes_value:
            return "0 B"
        unidades = ["B", "KB", "MB", "GB", "TB"]
        valor = float(bytes_value)
        indice = 0
        while valor >= 1024 and indice < len(unidades) - 1:
            valor /= 1024
            indice += 1
        if indice == 0:
            return f"{int(valor)} {unidades[indice]}"
        return f"{valor:.2f} {unidades[indice]}"

    def _post_mutacion(self):
        if self.on_refresh:
            self.on_refresh()

    def on_abrir_documento(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        ok, error = abrir_documento_desde_biblioteca(
            id_documento=documento.id,
            nombre_documento=documento.nombre,
            extension_documento=documento.extension,
        )
        if not ok:
            showerror("Error al abrir", error, parent=self.master)

    def on_abrir_carpeta(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        ruta_documento = self._get_ruta_documento(documento)
        if not ruta_documento or not exists(ruta_documento):
            showerror("Error", "El documento no existe en la biblioteca.", parent=self.master)
            return
        abrir_archivo(str(Path(ruta_documento).parent))

    def on_propiedades(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        ruta_documento = self._get_ruta_documento(documento)
        existe_archivo = bool(ruta_documento and exists(ruta_documento))
        estado = "Activo" if documento.esta_activo else "Inactivo"
        propiedades = [
            f"ID: {documento.id}",
            f"Nombre: {documento.nombre}",
            f"Extensión: {documento.extension}",
            f"Tamaño: {self._formatear_tamano(documento.tamano)}",
            f"Estado: {estado}",
            f"Hash: {documento.hash}",
            f"Creado en: {documento.creado_en or '-'}",
            f"Actualizado en: {documento.actualizado_en or '-'}",
            f"Ruta: {ruta_documento or '-'}",
            f"Existe en disco: {'Sí' if existe_archivo else 'No'}",
        ]
        showinfo("Propiedades del documento", "\n".join(propiedades), parent=self.master)

    def on_ver_metadatos(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        dialog = DialogVisualizarMetadatos(title="Metadatos del Documento")
        dialog.set_documento(documento)
        dialog.grab_set()

    def on_comentario(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return

        comentario_actual = self.comentarios.obtener_comentario(documento.id)
        texto = ask_resizable_text(
            master=self.master,
            title="Comentario del documento",
            prompt=f"Comentario para: {documento.nombre}",
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

        if self.comentarios.guardar_comentario(documento.id, texto):
            if texto:
                showinfo("Comentario", "Comentario guardado.", parent=self.master)
            else:
                showinfo("Comentario", "Comentario eliminado.", parent=self.master)
        else:
            showerror("Error", "No se pudo guardar el comentario.", parent=self.master)

    def on_renombrar_documento(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        nombre_nuevo = ask_resizable_string(
            master=self.master,
            title="Renombrar documento",
            prompt="Nuevo nombre del documento:",
            initialvalue=documento.nombre,
        )
        if nombre_nuevo is None:
            return
        nombre_nuevo = nombre_nuevo.strip()
        if not nombre_nuevo:
            showwarning("Nombre vacío", "El nombre del documento no puede estar vacío.", parent=self.master)
            return
        if nombre_nuevo == documento.nombre:
            return
        caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in nombre_nuevo for char in caracteres_invalidos):
            showwarning("Nombre inválido", f"El nombre no puede contener: {' '.join(caracteres_invalidos)}", parent=self.master)
            return

        ruta_origen = self._get_ruta_documento(documento)
        if not ruta_origen or not exists(ruta_origen):
            showerror("Error", "El documento no existe en la biblioteca.", parent=self.master)
            return
        ruta_destino = join(str(Path(ruta_origen).parent), f"{documento.id}_{nombre_nuevo}.{documento.extension}")
        if exists(ruta_destino):
            showerror("Archivo existente", "Ya existe un archivo con ese nombre.", parent=self.master)
            return

        nombre_anterior = documento.nombre
        documento.nombre = nombre_nuevo
        if not documento.actualizar():
            documento.nombre = nombre_anterior
            showerror("Error", "No se pudo actualizar el documento en la base de datos.", parent=self.master)
            return
        if not renombrar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino):
            documento.nombre = nombre_anterior
            documento.actualizar()
            showerror("Error", "No se pudo renombrar el archivo.", parent=self.master)
            return
        self._post_mutacion()
        showinfo("Documento renombrado", "El documento fue renombrado correctamente.", parent=self.master)

    def _generar_nombre_bibliografico(self, bibliografia: Bibliografia, estilo: str) -> str:
        autores = bibliografia.autores.split(',')[0] if bibliografia.autores else "Anonimo"
        ano = bibliografia.ano_publicacion or "s.f."
        titulo = bibliografia.titulo or "Sin Titulo"
        autores = (autores[:25] + '...') if len(autores) > 25 else autores
        titulo = (titulo[:50] + '...') if len(titulo) > 50 else titulo
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
            nuevo_nombre = f"{autores} - {titulo}"
        for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
            nuevo_nombre = nuevo_nombre.replace(char, '')
        return ' '.join(nuevo_nombre.split())

    def on_renombrar_bibliografico(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        bibliografia = Bibliografia(id_documento=documento.id, titulo="")
        if not bibliografia.instanciar():
            showwarning("Sin datos bibliográficos", "El documento no tiene información bibliográfica para renombrarlo.", parent=self.master)
            return
        nombre_nuevo = self._generar_nombre_bibliografico(
            bibliografia=bibliografia,
            estilo=ConfiguracionController().obtener_estilo_citacion() or "APA",
        )
        if not nombre_nuevo or nombre_nuevo == documento.nombre:
            return

        ruta_origen = self._get_ruta_documento(documento)
        if not ruta_origen or not exists(ruta_origen):
            showerror("Error", "El documento no existe en la biblioteca.", parent=self.master)
            return
        ruta_destino = join(str(Path(ruta_origen).parent), f"{documento.id}_{nombre_nuevo}.{documento.extension}")
        if exists(ruta_destino):
            showerror("Archivo existente", "Ya existe un archivo con ese nombre.", parent=self.master)
            return

        nombre_anterior = documento.nombre
        documento.nombre = nombre_nuevo
        if not documento.actualizar():
            documento.nombre = nombre_anterior
            showerror("Error", "No se pudo actualizar el documento en la base de datos.", parent=self.master)
            return
        if not renombrar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino):
            documento.nombre = nombre_anterior
            documento.actualizar()
            showerror("Error", "No se pudo renombrar el archivo.", parent=self.master)
            return

        self._post_mutacion()
        showinfo("Documento renombrado", "El documento fue renombrado bibliográficamente.", parent=self.master)

    def on_copiar_documento(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        ruta_origen = self._get_ruta_documento(documento)
        if not ruta_origen or not exists(ruta_origen):
            showerror("Archivo no encontrado", "El archivo no se encontró en la biblioteca.", parent=self.master)
            return
        ruta_destino_carpeta = askdirectory(title="Seleccione la carpeta de destino para copiar", parent=self.master)
        if not ruta_destino_carpeta:
            return
        ruta_destino = join(ruta_destino_carpeta, f"{documento.nombre}.{documento.extension}")
        if exists(ruta_destino):
            if not askyesno("Archivo existente", "Ya existe un archivo con el mismo nombre. ¿Desea sobreescribirlo?", parent=self.master):
                return
        if not copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino):
            showerror("Error al copiar", "No se pudo copiar el documento.", parent=self.master)
            return
        showinfo("Copia exitosa", f"Documento copiado a:\n{ruta_destino}", parent=self.master)

    def on_mover_documento(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        ruta_origen = self._get_ruta_documento(documento)
        if not ruta_origen or not exists(ruta_origen):
            showerror("Error", "El documento no existe en la biblioteca.", parent=self.master)
            return
        ruta_destino_carpeta = askdirectory(title="Seleccione la carpeta de destino (fuera de la biblioteca)", parent=self.master)
        if not ruta_destino_carpeta:
            return
        ruta_biblioteca = ConfiguracionController().obtener_ubicacion_biblioteca() or ""
        if ruta_biblioteca and Path(ruta_destino_carpeta).as_posix().startswith(Path(ruta_biblioteca).as_posix()):
            showwarning("Destino inválido", "La carpeta de destino debe estar fuera de la biblioteca.", parent=self.master)
            return
        ruta_destino = join(ruta_destino_carpeta, f"{documento.nombre}.{documento.extension}")
        if exists(ruta_destino):
            showwarning("Archivo existente", "Ya existe un archivo con ese nombre en destino.", parent=self.master)
            return
        if not askyesno("Confirmar movimiento", f"Se moverá '{documento.nombre}.{documento.extension}' y se eliminará su registro de BD. ¿Continuar?", parent=self.master):
            return
        if not mover_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino):
            showerror("Error al mover", "No se pudo mover el documento.", parent=self.master)
            return
        if not documento.eliminar():
            showwarning("Advertencia", "El archivo se movió, pero no se pudo eliminar el registro en la base de datos.", parent=self.master)
            return
        self._post_mutacion()
        showinfo("Movimiento completado", "Documento movido y eliminado de la biblioteca.", parent=self.master)

    def on_enviar_papelera(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        ruta_documento = self._get_ruta_documento(documento)
        if not ruta_documento or not exists(ruta_documento):
            showerror("Error", "El documento no existe en la biblioteca.", parent=self.master)
            return
        if not askyesno("Confirmar envío a papelera", f"¿Desea enviar '{documento.nombre}.{documento.extension}' a la papelera?", parent=self.master):
            return
        if not papelera_archivo(ruta_origen=ruta_documento):
            showerror("Error", "No se pudo enviar el documento a la papelera.", parent=self.master)
            return
        documento.esta_activo = False
        if not documento.actualizar():
            showwarning("Advertencia", "Se envió a papelera, pero no se pudo actualizar el estado en BD.", parent=self.master)
        self._post_mutacion()
        showinfo("Operación completada", "Documento enviado a la papelera.", parent=self.master)

    def on_eliminar_documento(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        if not askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el documento '{documento.nombre}'?\nEsta acción no se puede deshacer.", parent=self.master):
            return
        ruta_documento = self._get_ruta_documento(documento)
        if ruta_documento and exists(ruta_documento):
            if not eliminar_archivo(ruta_destino=ruta_documento):
                showerror("Error", "No se pudo eliminar el archivo del sistema.", parent=self.master)
                return
        if not documento.eliminar():
            showerror("Error", "No se pudo eliminar el documento de la base de datos.", parent=self.master)
            return
        self._post_mutacion()
        showinfo("Eliminación exitosa", "Documento eliminado de la biblioteca.", parent=self.master)

    def on_cambiar_estado(self):
        documento = self._get_documento_instanciado()
        if not documento:
            return
        documento.esta_activo = not documento.esta_activo
        if not documento.actualizar():
            showerror("Error", "No se pudo cambiar el estado del documento.", parent=self.master)
            return
        estado_texto = "activado" if documento.esta_activo else "desactivado"
        self._post_mutacion()
        showinfo("Estado cambiado", f"Documento {estado_texto}.", parent=self.master)
