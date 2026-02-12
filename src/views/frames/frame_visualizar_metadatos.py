from ttkbootstrap import Frame, LabelFrame
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *
from ttkbootstrap import Entry, Combobox, StringVar, Label, IntVar, Button
from tkinter.messagebox import showinfo, showerror
from models.entities.documento import Documento
from models.entities.metadato import Metadato
from models.daos.metadato_dao import MetadatoDAO
from typing import List
from utilities.auxiliar import editar_metadato
from models.controllers.configuracion_controller import ConfiguracionController
from utilities.auxiliar import generar_ruta_documento


class FrameVisualizarMetadatos(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # variables
        self.documento: Documento = None
        self.var_buscar = StringVar()
        self.lista_metadatos: List[Metadato] = []
        self.var_id_metadato = IntVar(value=0)
        self.var_clave = StringVar()
        self.var_valor = StringVar()
        self.claves_editables_pdf = [
            "PDF:Title",
            "PDF:Author",
            "PDF:Subject",
            "PDF:Keywords",
            "PDF:Creator",
            "PDF:Producer",
            "PDF:CreationDate",
        ]

        # cargamos los widgets
        self.cargar_widgets()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Widgets
    # └────────────────────────────────────────────────────────────┘
    def cargar_widgets(self):
        # Panel superior para la búsqueda
        frame_superior = LabelFrame(self, text="Buscar Metadatos", padding=(5, 5))
        self.panel_superior(frame=frame_superior)
        frame_superior.pack(side=TOP, fill=X, padx=5, pady=5)

        # Panel central para la tabla de metadatos
        frame_central = LabelFrame(self, text="Metadatos del Documento", padding=(5, 5))
        self.panel_central(frame=frame_central)
        frame_central.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=TRUE)

        # Panel inferior para la edición de metadatos
        frame_inferior = LabelFrame(self, text="Editar Metadato", padding=(5, 5))
        self.panel_inferior(frame=frame_inferior)
        frame_inferior.pack(side=TOP, fill=X, padx=5, pady=5)

    def panel_superior(self, frame: Frame):
        ent_buscar = Entry(frame, textvariable=self.var_buscar)
        ent_buscar.pack(side=LEFT, fill=X, padx=(0, 5), pady=5, expand=TRUE)
        ent_buscar.bind("<Return>", self.on_buscar)  # Evento para la tecla Enter
        ToolTip(ent_buscar, "Ingrese el término de búsqueda y presione Enter.")

        self.cbx_campos = Combobox(
            frame,
            values=("Todos", "Clave", "Valor"),
            state=READONLY,
        )
        self.cbx_campos.current(0)
        self.cbx_campos.pack(side=LEFT, padx=(0, 5), pady=5)
        self.cbx_campos.bind("<<ComboboxSelected>>", self.on_buscar)  # Evento al cambiar selección
        ToolTip(self.cbx_campos, "Seleccione el campo por el cual filtrar la búsqueda.")

    def panel_central(self, frame: Frame):
        self.table_view = Tableview(
            frame,
            bootstyle=PRIMARY,
            coldata=["Id", "Clave", "Valor"],
            rowdata=[],
            paginated=True,
            searchable=True,
            autofit=True,
            autoalign=True,
        )
        self.table_view.pack(side=TOP, expand=TRUE, padx=5, pady=5, fill=BOTH)
        ToolTip(
            self.table_view,
            "Haga doble clic en una fila para cargar sus datos en el panel de edición.",
        )

        # Vinculamos el evento al Treeview interno para la selección
        self.table_view.view.bind("<Double-Button-1>", self.on_double_click_table)

    def panel_inferior(self, frame: Frame):

        frame_label = Frame(frame)
        frame_label.pack(side=TOP, fill=X, padx=1, pady=1)

        self.lbl_documento = Label(frame_label, padding=(1, 1), text="")
        self.lbl_documento.pack(side=LEFT, padx=1, pady=1, fill=X)

        frame_editar = Frame(frame, padding=(1, 1))
        frame_editar.pack(side=TOP, fill=X, padx=1, pady=1)

        ent_id_metadato = Entry(
            frame_editar,
            textvariable=self.var_id_metadato,
            state=READONLY,
            justify=CENTER,
            width=10,
        )
        ent_id_metadato.pack(side=LEFT, padx=(0, 5), pady=5)
        ToolTip(ent_id_metadato, "ID del metadato (no editable).")

        cbx_clave = Combobox(
            frame_editar,
            textvariable=self.var_clave,
            values=self.claves_editables_pdf,
            state=READONLY,
            justify=LEFT,
        )
        cbx_clave.pack(side=LEFT, padx=(0, 5), pady=5)
        ToolTip(cbx_clave, "Seleccione la clave del metadato a modificar.")

        ent_valor = Entry(
            frame_editar,
            textvariable=self.var_valor,
            justify=LEFT,
        )
        ent_valor.pack(side=LEFT, padx=(0, 5), pady=5, expand=True, fill=X)
        ToolTip(ent_valor, "Ingrese el nuevo valor para la clave seleccionada.")

        btn_guardar = Button(frame_editar, text="Guardar", command=self.on_guardar_metadato)
        btn_guardar.pack(side=LEFT, padx=5, pady=5)
        ToolTip(btn_guardar, "Guardar los cambios en el archivo y en la base de datos.")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘
    def on_buscar(self, event=None):
        """Filtra los metadatos mostrados en la tabla según el término de búsqueda."""
        termino = self.var_buscar.get().lower()
        campo = self.cbx_campos.get()

        if not termino:
            self._mostrar_metadatos(self.lista_metadatos)
            return

        resultados_filtrados = []
        for metadato in self.lista_metadatos:
            clave = str(metadato.clave).lower()
            valor = str(metadato.valor).lower()

            if campo == "Todos":
                if termino in clave or termino in valor:
                    resultados_filtrados.append(metadato)
            elif campo == "Clave":
                if termino in clave:
                    resultados_filtrados.append(metadato)
            elif campo == "Valor":
                if termino in valor:
                    resultados_filtrados.append(metadato)
        self._mostrar_metadatos(resultados_filtrados)

    def on_double_click_table(self, event):
        # Obtener la tupla de items seleccionados
        selection = self.table_view.view.selection()
        if not selection:
            return  # No hay nada seleccionado

        # Obtener el ID del primer item seleccionado
        item_id = selection[0]
        # Obtener los valores de la fila usando el ID
        row_values = self.table_view.view.item(item_id, "values")

        # Asignar los valores a las variables para que se muestren en los Entry
        self.var_id_metadato.set(row_values[0])
        self.var_clave.set(row_values[1])
        self.var_valor.set(row_values[2])

    def on_guardar_metadato(self):
        if not self.documento:
            showerror("Error", "No hay un documento seleccionado.")
            return

        clave = self.var_clave.get()
        valor = self.var_valor.get()
        id_metadato = self.var_id_metadato.get()

        if not clave:
            showerror("Error", "Debe seleccionar una clave para editar.")
            return

        # 1. Obtener la ruta del archivo en la biblioteca
        conf = ConfiguracionController()
        ruta_biblioteca = conf.obtener_ubicacion_biblioteca()
        ruta_documento = generar_ruta_documento(
            ruta_biblioteca=ruta_biblioteca,
            nombre_documento=f"{self.documento.nombre}.{self.documento.extension}",
            id_documento=self.documento.id,
        )

        # 2. Editar el metadato en el archivo físico
        if not editar_metadato(clave=clave, valor=valor, path_file=ruta_documento):
            showerror(
                "Error de archivo", f"No se pudo actualizar el metadato '{clave}' en el archivo."
            )
            return

        # 3. Actualizar el metadato en la base de datos
        metadato = Metadato(
            id=id_metadato,
            id_documento=self.documento.id,
            clave=clave,
            valor=valor,
        )

        if metadato.existe():
            if not metadato.actualizar():
                showerror(
                    "Error de base de datos",
                    "No se pudo actualizar el registro en la base de datos.",
                )
                return
        else:
            metadato.insertar()

        showinfo("Éxito", "Metadato actualizado correctamente.")
        self._refrescar_datos()

    def set_documento(self, documento: Documento):
        self.documento = documento
        # mostramos el nombre del documento
        self._mostrar_nombre_documento()
        # obtenemos los metadatos
        self._obtener_metadatos_sql()
        # mostramos los metadatos en la tabla
        self._mostrar_metadatos(self.lista_metadatos)

    def set_path_file(self, path_file: str):
        self.path_file = path_file
        # aca debemos de pasa la funcion,
        # que se encargara de cargar los datos en table view

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos Privados
    # └────────────────────────────────────────────────────────────┘

    def _refrescar_datos(self):
        """Limpia y vuelve a cargar los metadatos desde la BD."""
        self.lista_metadatos.clear()
        self._obtener_metadatos_sql()
        self._mostrar_metadatos(self.lista_metadatos)

    def _mostrar_nombre_documento(self):
        if self.documento:
            self.lbl_documento.config(text=self.documento.nombre)

    def _obtener_metadatos_sql(self):
        if self.documento:
            # instanciamos el DAO metadatos
            dao = MetadatoDAO()
            # parametros para la consulta
            sql = "SELECT * FROM metadato WHERE id_documento=?"
            params = (self.documento.id,)
            # instanciamos todos los metadatos que tiene el documento
            datos = dao.instanciar(sql=sql, params=params)
            # listamos
            if datos:
                for dato in datos:
                    metadato = Metadato(
                        id_documento=dato['id_documento'],
                        id=dato['id'],
                        clave=dato['clave'],
                        valor=dato['valor'],
                    )
                    self.lista_metadatos.append(metadato)

    def _mostrar_metadatos(self, datos_a_mostrar: List[Metadato]):
        """Limpia la tabla y muestra la lista de metadatos proporcionada."""
        self.table_view.delete_rows()
        if datos_a_mostrar:
            for data in datos_a_mostrar:
                fila = [data.id, data.clave, str(data.valor)]
                self.table_view.insert_row(index=END, values=fila)
        # autofit_columns() puede ser lento con muchos datos,
        # pero para este caso de uso está bien.
        self.table_view.autofit_columns()
