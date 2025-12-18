from tkinter.messagebox import showwarning, showerror, showinfo, askyesno
from typing import Dict, Any
from ttkbootstrap import IntVar, Button, StringVar
from models.entities.documento import Documento
from models.entities.bibliografia import Bibliografia
from utilities.auxiliar import obtener_datos_libros


class ControlarAdministrarBiblioteca:
    def __init__(self, master, map_vars: Dict[str, Any] = {}, map_buttons: Dict[str, Button] = {}):
        # maps
        self.map_vars = map_vars
        self.map_buttons = map_buttons
        self.master = master

        # Vars
        self.var_radio_documento: IntVar = self.map_vars['radio_documento']
        self.var_titulo: StringVar = self.map_vars['titulo']
        self.var_autores: StringVar = self.map_vars['autores']
        self.var_lugar_publicacion: StringVar = self.map_vars['lugar_publicacion']
        self.var_editorial: StringVar = self.map_vars['editorial']
        self.var_ano_publicacion: IntVar = self.map_vars['ano_publicacion']
        self.var_numero_edicion: StringVar = self.map_vars['numero_edicion']
        self.var_idioma: StringVar = self.map_vars['idioma']
        self.var_volumen_tomo: StringVar = self.map_vars['volumne_tomo']
        self.var_numero_paginas: StringVar = self.map_vars['numero_paginas']
        self.var_isbn: StringVar = self.map_vars['isbn']
        self.var_id_bibliografia: StringVar = self.map_vars['id_bibliografia']

        # Buttons
        self.btn_abrir: Button = self.map_buttons['abrir']
        self.btn_guardar: Button = self.map_buttons['guardar']
        self.btn_eliminar: Button = self.map_buttons['eliminar']
        self.btn_limpiar: Button = self.map_buttons['limpiar']
        self.btn_obtener_online: Button = self.map_buttons['datos_online']

        # Entidades
        self.documento: Documento = None
        self.bibliografia: Bibliografia = None

        # trace
        self.var_radio_documento.trace_add('write', lambda *args: self.on_change_documento())

        # establecemos los eventos
        self.btn_abrir.config(command=self.on_abrir_documento)
        self.btn_guardar.config(command=self.on_guardar)
        self.btn_eliminar.config(command=self.on_eliminar)
        self.btn_limpiar.config(command=self.on_limpiar)
        self.btn_obtener_online.config(command=self.on_obtener_online)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos privados
    # └────────────────────────────────────────────────────────────┘

    def _instanciar_bibliografia(self, id_documento: int):
        if id_documento != 0:
            self.bibliografia = Bibliografia(
                titulo="",
                autores="",
                id=0,
                id_documento=id_documento,
                ano_publicacion=0,
                lugar_publicacion="",
                editorial="",
                numero_edicion="",
                idioma="",
                volumen_tomo="",
                numero_paginas="",
                isbn="",
            )
            if self.bibliografia.existe():
                # si existe los instanciamos
                if self.bibliografia.instanciar():
                    # mostramos los datos en los entrys
                    self._show_bibliografia()

    def _show_bibliografia(self):
        # mostramos los datos de la bibliografia instanciada
        if self.bibliografia.id != 0:
            titulo = self.bibliografia.titulo
            autores = self.bibliografia.autores
            id_bibliografia = self.bibliografia.id
            ano_publicacion = self.bibliografia.ano_publicacion
            lugar_publicacion = self.bibliografia.lugar_publicacion
            editorial = self.bibliografia.editorial
            numero_edicion = self.bibliografia.numero_edicion
            numero_pagina = self.bibliografia.numero_paginas
            isbn = self.bibliografia.isbn
            idioma = self.bibliografia.idioma
            volumen_tomo = self.bibliografia.volumen_tomo

            # cargamos los datos a las variables
            self.var_titulo.set(value=titulo)
            self.var_autores.set(value=autores)
            self.var_id_bibliografia.set(value=id_bibliografia)
            self.var_ano_publicacion.set(value=ano_publicacion)
            self.var_lugar_publicacion.set(value=lugar_publicacion)
            self.var_editorial.set(value=editorial)
            self.var_numero_edicion.set(value=numero_edicion)
            self.var_numero_paginas.set(value=numero_pagina)
            self.var_isbn.set(value=isbn)
            self.var_idioma.set(value=idioma)
            self.var_volumen_tomo.set(value=volumen_tomo)

    def _set_bibliografia(self):
        id_documento = self.var_radio_documento.get()
        if id_documento != 0:
            if not self.var_titulo.get():
                showwarning(
                    title="Advertencia",
                    message="El campo titulo no puede estar vacio",
                    parent=self.master,
                )
                return

            self.bibliografia = Bibliografia(
                titulo=self.var_titulo.get(),
                autores=self.var_autores.get(),
                id=self.var_id_bibliografia.get(),
                id_documento=id_documento,
                ano_publicacion=self.var_ano_publicacion.get(),
                lugar_publicacion=self.var_lugar_publicacion.get(),
                editorial=self.var_editorial.get(),
                numero_edicion=self.var_numero_edicion.get(),
                idioma=self.var_idioma.get(),
                volumen_tomo=self.var_volumen_tomo.get(),
                numero_paginas=self.var_numero_paginas.get(),
                isbn=self.var_isbn.get(),
            )

    def _clear_entrys(self):
        # limpiamos los entrys
        self.var_titulo.set(value="")
        self.var_autores.set(value="")
        self.var_id_bibliografia.set(value=0)
        self.var_ano_publicacion.set(value=0)
        self.var_lugar_publicacion.set(value="")
        self.var_editorial.set(value="")
        self.var_numero_edicion.set(value="")
        self.var_numero_paginas.set(value=0)
        self.var_isbn.set(value="")
        self.var_idioma.set(value="")
        self.var_volumen_tomo.set(value="")
        self.var_numero_paginas.set(value=0)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def on_obtener_online(self):
        isbn = self.var_isbn.get()
        if not isbn:
            showwarning(
                title="Obtener Online",
                message="El campo ISBN, no puede estar vacio, para buscar los datos",
                parent=self.master,
            )
            return
        datos = obtener_datos_libros(isbn=isbn)
        if not datos:
            showinfo(
                title="Datos no obtenidos",
                message=f"No se encontraron datos sobre el documento en el sitio: googleapis, con el ISBN: {isbn}",
                parent=self.master,
            )

        # En caso que se encuentre datos los mostramos
        self.var_titulo.set(datos['titulo'])
        self.var_autores.set(datos['autores'])
        self.var_ano_publicacion.set(datos['ano_publicacion'])
        self.var_editorial.set(datos['editorial'])
        self.var_numero_edicion.set(datos['numero_edicion'])
        self.var_idioma.set(datos['idioma'])
        self.var_numero_paginas.set(datos['numero_paginas'])

    def on_limpiar(self):
        self.var_radio_documento.set(value=0)
        self._clear_entrys()

    def on_eliminar(self):
        if self.documento is not None:
            if self.documento.id != 0:
                # mensaje de de comfimacion
                ask = askyesno(
                    title="Eliminacion de datos",
                    message="¿Esta seguro que quiere eliminar los registros de los datos bibliograficos?",
                    parent=self.master,
                )
                if ask:
                    if self.documento.eliminar():
                        # si la eliminacion de los datos fue existosa borramos los campos
                        self._clear_entrys()

    def on_change_documento(self):

        # limpiamos siempre los entrys, al cambiar un documento
        self._clear_entrys()

        id_documento = self.var_radio_documento.get()
        if id_documento == 0 or id_documento is None:
            showwarning(
                title="Advertencia",
                message="Seleccione un documento",
                icon='warning',
                parent=self.master,
            )
            return

        self.documento = Documento(nombre="", extension="", hash="", id=id_documento, tamano=0)
        if isinstance(self.documento, Documento):
            # instanciamos
            if self.documento.instanciar():
                # instancimos la bibliografia si existe
                self._instanciar_bibliografia(id_documento=id_documento)

    def on_guardar(self):
        self._set_bibliografia()
        if self.bibliografia is not None:
            if isinstance(self.bibliografia, Bibliografia):
                if self.bibliografia.id == 0:
                    new_id = self.bibliografia.insertar()
                    if new_id is not None:
                        self.var_id_bibliografia.set(value=new_id)
                else:
                    if self.bibliografia.id > 0:
                        self.bibliografia.actualizar()

    def on_abrir_documento(self):
        """
        Placeholder para la lógica de abrir el documento seleccionado.
        Los documentos e abriran en la carpeta temporal del sistema.
        """
        from os.path import join, exists
        from utilities.configuracion import DIRECTORIO_TEMPORAL
        from models.controllers.configuracion_controller import ConfiguracionController
        from utilities.auxiliar import generar_ruta_documento, abrir_archivo, copiar_archivo

        if self.documento:
            doc = self.documento
            configuracion = ConfiguracionController()
            ruta_biblioteca = configuracion.obtener_ubicacion_biblioteca()
            if not exists(ruta_biblioteca):
                showerror(title="Error", message="La ubicación de la biblioteca no existe.")
                return
            ruta_documento = generar_ruta_documento(
                ruta_biblioteca=ruta_biblioteca,
                id_documento=doc.id,
                nombre_documento=f"{doc.nombre}.{doc.extension}",
            )
            ruta_destino = join(DIRECTORIO_TEMPORAL, f"{doc.nombre}.{doc.extension}")
            if not exists(ruta_documento):
                showerror(
                    title="Error",
                    message=f"El documento no existe en la biblioteca: {ruta_documento}",
                )
                return
            # copiamos el documento en la carpeta temporal
            try:
                copiar_archivo(ruta_origen=ruta_documento, ruta_destino=ruta_destino)
            except Exception as e:
                print(f"Error al copiar el documento: {e}")
                return
            # abrimos el documento en la carpeta temporal
            abrir_archivo(ruta_origen=ruta_destino)
        else:
            print("Error: No hay documento seleccionado para abrir.")
