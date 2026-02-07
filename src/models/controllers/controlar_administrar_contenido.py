from typing import Dict, Any, Optional
from ttkbootstrap import Treeview, Button, StringVar, IntVar, Combobox
from ttkbootstrap.constants import *
from models.entities.documento import Documento
from models.entities.capitulo import Capitulo
from models.entities.seccion import Seccion
from models.entities.consulta import Consulta
from tkinter.messagebox import showwarning, showerror


class ControlarAdministrarContenido:
    def __init__(self, map_vars: Dict[str, Any], map_widgets: Dict[str, Any], master):
        self.map_vars = map_vars
        self.map_widgets = map_widgets
        self.master = master

        # map_items
        self.map_items: Dict[str, Any] = {}
        self.map_padres: Dict[str, Seccion] = {}

        # Variables Entidades
        self.documento: Documento = None
        self.seccion: Seccion = None
        self.capitulo: Capitulo = None

        # instanciamos los maps
        # Vars
        self.var_radio_documento: IntVar = self.map_vars["radio_documento"]
        self.var_id_seccion_padre: IntVar = self.map_vars["id_seccion_padre"]
        self.var_id_capitulo: IntVar = self.map_vars["id_capitulo"]
        self.var_numero_capitulo: StringVar = self.map_vars["numero_capitulo"]
        self.var_pagina_capitulo: StringVar = self.map_vars["pagina_capitulo"]
        self.var_titulo_capitulo: StringVar = self.map_vars["titulo_capitulo"]
        self.var_id_seccion: IntVar = self.map_vars["id_seccion"]
        self.var_nivel_seccion: StringVar = self.map_vars["nivel_seccion"]
        self.var_pagina_seccion: StringVar = self.map_vars["pagina_seccion"]
        self.var_titulo_seccion: StringVar = self.map_vars["titulo_seccion"]

        # Widgets
        self.btn_agregar_capitulo: Button = self.map_widgets["agregar_capitulo"]
        self.btn_editar_capitulo: Button = self.map_widgets["editar_capitulo"]
        self.btn_eliminar_capitulo: Button = self.map_widgets["eliminar_capitulo"]
        self.btn_nuevo_capitulo: Button = self.map_widgets["nuevo_capitulo"]
        self.btn_agregar_seccion: Button = self.map_widgets["agregar_seccion"]
        self.btn_editar_seccion: Button = self.map_widgets["editar_seccion"]
        self.btn_eliminar_seccion: Button = self.map_widgets["eliminar_seccion"]
        self.btn_nuevo_seccion: Button = self.map_widgets["nuevo_seccion"]
        self.btn_abrir_documento: Button = self.map_widgets["abrir_documento"]
        self.btn_importar_capitulos: Button = self.map_widgets["importar_capitulos"]
        self.btn_importar_secciones: Button = self.map_widgets["importar_secciones"]
        self.tree_view: Treeview = self.map_widgets["tree_view"]
        self.cbx_seccion_padre: Combobox = self.map_widgets["seccion_padre"]

        # trace
        self.var_radio_documento.trace_add('write', lambda *args: self.on_change_documento())
        self.var_id_capitulo.trace_add('write', lambda *args: self._toggle_buttons_capitulo())
        self.var_id_seccion.trace_add('write', lambda *args: self._toggle_buttons_seccion())

        # Agregamos los eventos
        self.btn_agregar_capitulo.config(command=self.on_agregar_capitulo)
        self.btn_agregar_seccion.config(command=self.on_agregar_seccion)
        self.btn_abrir_documento.config(command=self.on_abrir_documento)
        self.btn_editar_capitulo.config(command=self.on_editar_capitulo)
        self.btn_editar_seccion.config(command=self.on_editar_seccion)
        self.btn_nuevo_seccion.config(command=self.on_nueva_seccion)
        self.btn_nuevo_capitulo.config(command=self.on_nuevo_capitulo)
        self.btn_eliminar_capitulo.config(command=self.on_eliminar_capitulo)
        self.btn_eliminar_seccion.config(command=self.on_eliminar_seccion)
        self.btn_importar_capitulos.config(command=self.on_importar_capitulos)
        self.btn_importar_secciones.config(command=self.on_importar_secciones)
        # evento el tree_view
        self.tree_view.bind("<Double-1>", self.on_doble_click_tree)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘
    def on_eliminar_seccion(self):
        self._eliminar_seccion()

    def on_eliminar_capitulo(self):
        self._eliminar_capitulo()

    def on_nueva_seccion(self):
        self._nueva_seccion()

    def on_nuevo_capitulo(self):
        self._nuevo_capitulo()

    def on_editar_seccion(self):
        self._editar_seccion()

    def on_editar_capitulo(self):
        self._editar_capitulo()

    def on_agregar_seccion(self):
        self._agregar_seccion()

    def on_change_documento(self):
        # cuando cambiamos de documentos, lo instanciamos
        id_documento = self.var_radio_documento.get()
        self._instanciar_documento(id_documento=id_documento)
        # cargamos los capitulos y secciones, si hubiere
        self._cargar_capitulos(id_documento=id_documento)

    def on_agregar_capitulo(self):
        self._agregar_capitulo()

    def on_doble_click_tree(self, event):
        seleccion = self.tree_view.selection()
        if not seleccion:  # Validar que hay algo seleccionado
            return

        iid = seleccion[0]

        resultado = self._obtener_seleccion(iid=iid)

        # Validar que se obtuvo un resultado válido
        if resultado is None:
            return

        tipo, objecto = resultado

        if tipo == "capitulo":
            # si es un capitulo lo cargamos a los entrys
            self._show_entrys_capitulo(capitulo=objecto)
            # cargamos las secciones que tiene en el combobox
            self._listar_secciones(capitulo=objecto)
            # cargamos la variable capitulo
            self._set_capitulo()
            # limpiamos la seccion
            self._nueva_seccion()

        elif tipo == "seccion":
            # si es una seccion cargamos los entrys
            self._show_entrys_seccion(seccion=objecto)
            # instanciamos un capitulo
            capitulo = Capitulo(
                id_documento=self.documento.id,
                id=objecto.id_capitulo,
                titulo="",
                pagina_inicio=0,
                numero_capitulo="",
            )
            if capitulo.instanciar():
                self._show_entrys_capitulo(capitulo=capitulo)
                # cargamos ambas variables
                self._set_seccion()
                self._set_capitulo()
                # cargamos la lista de padres
                self._listar_secciones(capitulo=capitulo)

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

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘

    def _set_capitulo(self):
        id_documento = self.documento.id
        numero_capitulo = self.var_numero_capitulo.get()
        titulo_capitulo = self.var_titulo_capitulo.get()
        pagina_capitulo = self.var_pagina_capitulo.get()
        id_capitulo = self.var_id_capitulo.get()
        self.capitulo = Capitulo(
            id_documento=id_documento,
            numero_capitulo=numero_capitulo,
            titulo=titulo_capitulo,
            pagina_inicio=pagina_capitulo,
            id=id_capitulo,
        )

    def _set_seccion(self):
        id_capitulo = self.var_id_capitulo.get()
        id_seccion = self.var_id_seccion.get()
        titulo_seccion = self.var_titulo_seccion.get()
        nivel_seccion = self.var_nivel_seccion.get()
        numero_pagina = self.var_pagina_seccion.get()
        # obtenemos el elemento seleccionado el combobox
        seccion_name = self.cbx_seccion_padre.get()
        if seccion_name == "Sin padre":
            id_padre = None
        else:
            # buscamos en el mapa y obtenemos el id
            if seccion_name in self.map_padres.keys():
                seccion_padre = self.map_padres[seccion_name]
                id_padre = seccion_padre.id
        self.seccion = Seccion(
            id_capitulo=id_capitulo,
            titulo=titulo_seccion,
            nivel=nivel_seccion,
            id=id_seccion,
            numero_pagina=numero_pagina,
            id_padre=id_padre,
        )

    def _toggle_buttons_capitulo(self):
        id_capitulo = self.var_id_capitulo.get()
        if id_capitulo == 0:
            self.btn_agregar_capitulo.config(state=NORMAL)
            self.btn_editar_capitulo.config(state=DISABLED)
        else:
            self.btn_agregar_capitulo.config(state=DISABLED)
            self.btn_editar_capitulo.config(state=NORMAL)

    def _toggle_buttons_seccion(self):
        id_seccion = self.var_id_seccion.get()
        if id_seccion == 0:
            self.btn_agregar_seccion.config(state=NORMAL)
            self.btn_editar_seccion.config(state=DISABLED)
        else:
            self.btn_agregar_seccion.config(state=DISABLED)
            self.btn_editar_seccion.config(state=NORMAL)

    def _listar_secciones(self, capitulo: Capitulo):
        """Lista las secciones de un capitulo para cargarlo en el combobox"""
        # limpiamos el map_padres
        self.map_padres.clear()
        # creamos una lista de posibles, padres
        lista_padres = []
        lista_padres.append("Sin padre")
        # borramos todos los elementos de un combobox
        self.cbx_seccion_padre.config(values=[])
        if isinstance(capitulo, Capitulo):
            consulta = Consulta()
            lista_secciones = consulta.secciones_capitulo(id_capitulo=capitulo.id)
            if lista_secciones:
                for seccion in lista_secciones:
                    lista_padres.append(f"{seccion.nivel} - {seccion.titulo}")
                    # agregamos al mapa de padres
                    self.map_padres[f"{seccion.nivel} - {seccion.titulo}"] = seccion
        # una vez que se genere o no la lista lo cargamos
        self.cbx_seccion_padre.config(values=lista_padres)

    def _obtener_seleccion(self, iid: str = None) -> Optional[tuple]:
        """
        Obtiene el tipo y el objeto de la selección en el tree view.

        Args:
            iid: El identificador del item en el tree view

        Returns:
            Una tupla (tipo, objeto) donde tipo es "capitulo" o "seccion",
            o None si no se encuentra el item.
        """
        if iid is None:
            return None

        if iid in self.map_items:
            # Verificar que el iid tenga al menos 3 caracteres
            if len(iid) >= 3:
                value = iid[0:3]
                if value == "cap":
                    return "capitulo", self.map_items[iid]
                elif value == "sec":
                    return "seccion", self.map_items[iid]

        # Si no se encuentra el item, retornar None explícitamente
        return None

    def _show_entrys_capitulo(self, capitulo: Capitulo):
        """Mostramos el capitulo en los campos"""
        if isinstance(capitulo, Capitulo):
            id_capitulo = capitulo.id
            titulo_capitulo = capitulo.titulo
            numero_pagina = capitulo.pagina_inicio
            numero_capitulo = capitulo.numero_capitulo
            # cargamos los valores en el entrys
            self.var_id_capitulo.set(value=id_capitulo)
            self.var_titulo_capitulo.set(value=titulo_capitulo)
            self.var_numero_capitulo.set(value=numero_capitulo)
            self.var_pagina_capitulo.set(value=numero_pagina)

    def _show_entrys_seccion(self, seccion: Seccion):
        """Mostramos la seccion en los campos"""
        if isinstance(seccion, Seccion):
            id_seccion = seccion.id
            titulo_seccion = seccion.titulo
            nivel_seccion = seccion.nivel
            numero_pagina = seccion.numero_pagina
            id_padre = seccion.id_padre
            id_capitulo = seccion.id_capitulo
            # cargamos los valores en entrys
            self.var_id_seccion.set(value=id_seccion)
            self.var_titulo_seccion.set(value=titulo_seccion)
            self.var_nivel_seccion.set(value=nivel_seccion)
            self.var_pagina_seccion.set(value=numero_pagina)
            # buscamos la seccion en la lista
            seccion_padre = Seccion(
                id=id_padre,
                titulo="",
                nivel="",
                id_padre=0,
                numero_pagina=0,
                id_capitulo=id_capitulo,
            )
            if seccion_padre.instanciar():
                self.cbx_seccion_padre.set(f"{seccion_padre.nivel} - {seccion_padre.titulo}")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos para agregar capitulos y secciones
    # └────────────────────────────────────────────────────────────┘

    def _eliminar_seccion(self):
        if not isinstance(self.documento, Documento):
            showwarning(title="Advertencia", message="Seleccione un documento", parent=self.master)
            return

        if isinstance(self.seccion, Seccion):
            if self.seccion.eliminar():
                self._nueva_seccion()
                self._cargar_capitulos(self.documento.id)

    def _eliminar_capitulo(self):
        if not isinstance(self.documento, Documento):
            showwarning(title="Advertencia", message="Seleccione un documento", parent=self.master)
            return

        if isinstance(self.capitulo, Capitulo):
            if self.capitulo.eliminar():
                self._nuevo_capitulo()
                self._cargar_capitulos(self.documento.id)

    def _nueva_seccion(self):
        self.var_id_seccion.set(value=0)
        self.var_titulo_seccion.set(value="")
        self.var_nivel_seccion.set(value="")
        self.var_pagina_seccion.set(value=0)

    def _nuevo_capitulo(self):
        self.var_id_capitulo.set(value=0)
        self.var_titulo_capitulo.set(value="")
        self.var_numero_capitulo.set(value=0)
        self.var_pagina_capitulo.set(value=0)

    def _editar_seccion(self):
        if isinstance(self.documento, Documento):
            self._set_seccion()
            # No se puede cargar, si no tiene capitulo asignado
            if self.seccion.id_capitulo == 0:
                showwarning(
                    title="Advertencia",
                    message="Debe de seleccionar un capitulo",
                    parent=self.master,
                )
                return
            # No se puede cargar si no tenemos el titulo
            if not self.seccion.titulo:
                showwarning(
                    title="Advertencia",
                    message="Debe de seleccionar un capitulo",
                    parent=self.master,
                )
                return

            if self.seccion.id != 0:
                if self.seccion.actualizar():
                    # cargamos los capitulos
                    self._cargar_capitulos(id_documento=self.documento.id)
        else:
            showwarning(title="Advertencia", message="Seleccione un documento", parent=self.master)

    def _agregar_seccion(self):
        if isinstance(self.documento, Documento):
            self._set_seccion()
            # No se puede cargar, si no tiene capitulo asignado
            if self.seccion.id_capitulo == 0:
                showwarning(
                    title="Advertencia",
                    message="Debe de seleccionar un capitulo",
                    parent=self.master,
                )
                return
            # No se puede cargar si no tenemos el titulo
            if not self.seccion.titulo:
                showwarning(
                    title="Advertencia",
                    message="Debe de seleccionar un capitulo",
                    parent=self.master,
                )
                return

            if self.seccion.id == 0:
                # verificamos que no exista la seccion
                if self.seccion.existe():
                    showwarning(
                        title="Advertencia", message="Ya existe la seccion", parent=self.master
                    )
                    return

                new_id = self.seccion.insertar()

                if new_id is not None:
                    self.var_id_seccion.set(value=new_id)
                    # cargamos los capitulos
                    self._cargar_capitulos(id_documento=self.documento.id)
        else:
            showwarning(title="Advertencia", message="Seleccione un documento", parent=self.master)

    def _editar_capitulo(self):
        if isinstance(self.documento, Documento):
            # instanciamos
            self._set_capitulo()

            if not self.capitulo.titulo:
                showwarning(
                    title="Advertencia",
                    message="El titulo no puede estar vacio",
                    parent=self.master,
                )
                return

            if not self.capitulo.numero_capitulo:
                showwarning(
                    title="Advertencia",
                    message="El numero de capitulo no puede estar vacio",
                    parent=self.master,
                )
                return

            if self.capitulo.id != 0:
                if self.capitulo.actualizar():
                    self._cargar_capitulos(id_documento=self.documento.id)

        else:
            showwarning(title="Advertencia", message="Seleccione un documento", parent=self.master)

    def _agregar_capitulo(self):
        if isinstance(self.documento, Documento):
            # instanciamos
            self._set_capitulo()

            if not self.capitulo.titulo:
                showwarning(
                    title="Advertencia",
                    message="El titulo no puede estar vacio",
                    parent=self.master,
                )
                return

            if not self.capitulo.numero_capitulo:
                showwarning(
                    title="Advertencia",
                    message="El numero de capitulo no puede estar vacio",
                    parent=self.master,
                )
                return

            if self.capitulo.id == 0:

                # verificamos que no exista
                if self.capitulo.existe():
                    showwarning(
                        title="Advertencia", message="Ya existe el capitulo", parent=self.master
                    )
                    return

                new_id = self.capitulo.insertar()
                if new_id is not None:
                    self.var_id_capitulo.set(value=new_id)
                    self._cargar_capitulos(id_documento=self.documento.id)

        else:
            showwarning(title="Advertencia", message="Seleccione un documento", parent=self.master)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos para cargar capitulos y secciones
    # └────────────────────────────────────────────────────────────┘

    def _cargar_capitulos(self, id_documento: int):
        """Carga los capitulos en el tree view"""
        # limpiamos el map_items (mapa de items)
        self.map_items.clear()
        # limpiamos el tree
        self.tree_view.delete(*self.tree_view.get_children())
        # generamos una consulta
        consulta = Consulta()
        lista_capitulos = consulta.capitulos_documento(id_documento=id_documento)
        if lista_capitulos:
            for capitulo in lista_capitulos:
                iid_capitulo = self._insertar_tree_capitulo(capitulo=capitulo)
                # Solo agregamos al mapa si el iid no es None
                if iid_capitulo is not None:
                    self.map_items[iid_capitulo] = capitulo
                    # cargamos las secciones que tiene el capitulo
                    self._cargar_secciones(iid_capitulo=iid_capitulo, id_capitulo=capitulo.id)
        # Aplicar formato visual
        self.tree_view.tag_configure("capitulo", font=("", 9, "bold"))

    def _cargar_secciones(self, iid_capitulo: str, id_capitulo: int):
        """Cargamos las secciones que tiene cada capitulo el tree_view"""
        # hacemos una consulta para obtener las secciones
        consulta = Consulta()
        lista_secciones = consulta.secciones_capitulo(id_capitulo=id_capitulo)
        if lista_secciones:
            # si la lista de secciones no esta vacia, la recorremos
            for seccion in lista_secciones:
                # cargamos las secciones solamente si no es hijo
                id_padre = seccion.id_padre
                if id_padre is None:
                    iid_seccion = self._insertar_tree_seccion(
                        seccion=seccion, iid_padre=iid_capitulo
                    )
                    # Solo insertamos el iid_seccion en mapa si no es None
                    if iid_seccion is not None:
                        self.map_items[iid_seccion] = seccion
                else:
                    # aqui hacemos la funcion recursiva
                    self._recursiva_seccion(
                        seccion_padre=seccion, iid_seccion=f"sec_{seccion.id_padre}"
                    )

    def _recursiva_seccion(self, seccion_padre: Seccion, iid_seccion: str) -> str:
        lista_hijos = seccion_padre.hijos_directos()
        if lista_hijos:
            for hijo_seccion in lista_hijos:
                iid = self._insertar_tree_seccion(seccion=hijo_seccion, iid_padre=iid_seccion)
                # Solo agregamos al mapa si el iid no es None
                if iid is not None:
                    self.map_items[iid] = hijo_seccion
                    # Solo continuamos la recursión si el item existe en el tree
                    if not self.tree_view.exists(iid):
                        self._recursiva_seccion(seccion_padre=hijo_seccion, iid_seccion=iid)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos para nsertamos los capitulos y secciones al tree
    # └────────────────────────────────────────────────────────────┘

    def _insertar_tree_capitulo(self, capitulo: Capitulo) -> str:
        """Insertamos en el tree un capitulo"""
        iid = None
        if isinstance(capitulo, Capitulo):
            titulo = capitulo.titulo
            numero_capitulo = capitulo.numero_capitulo
            numero_pagina = capitulo.pagina_inicio
            text = f"{numero_capitulo} - {titulo}"
            iid = f"cap_{capitulo.id}"
            if not self.tree_view.exists(iid):
                self.tree_view.insert(
                    "",
                    "end",
                    iid=iid,
                    text=text,
                    values=(numero_pagina,),
                    tags=("capitulo",),
                )
        return iid

    def _insertar_tree_seccion(self, seccion: Seccion, iid_padre: str) -> str:
        """Insertamos en el tree una seccion"""
        iid = None
        if isinstance(seccion, Seccion):
            titulo = seccion.titulo
            nivel = seccion.nivel
            numero_pagina = seccion.numero_pagina
            text = f"{nivel} - {titulo}"
            iid = f"sec_{seccion.id}"
            if not self.tree_view.exists(iid):
                self.tree_view.insert(
                    iid_padre, "end", iid=iid, text=text, values=(numero_pagina,), tags=("seccion",)
                )
        return iid

    def _instanciar_documento(self, id_documento: int):
        if id_documento == 0 or id_documento is None:
            showwarning(
                title="Instanciar Documento",
                message="No se puedo instanciar el documento",
                parent=self.master,
            )
            return

        self.documento = Documento(
            nombre="",
            extension="",
            tamano=0,
            hash="",
            id=id_documento,
        )
        self.documento.instanciar()

    def on_importar_capitulos(self):
        """Delega la importación de capítulos a la vista."""
        self.master.importar_capitulos()

    def on_importar_secciones(self):
        """Delega la importación de secciones a la vista."""
        self.master.importar_secciones()
