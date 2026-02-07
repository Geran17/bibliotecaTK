import os
import math
import threading
from typing import Dict, Any
from ttkbootstrap import Frame, StringVar, Entry, Combobox, Button, Label, Separator
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter.messagebox import showwarning, showerror, showinfo
from tkinter import Menu
from ttkbootstrap.tooltip import ToolTip
from PIL import Image, ImageTk

from models.entities.consulta import Consulta
from models.entities.favorito import Favorito
from models.entities.documento import Documento
from models.controllers.configuracion_controller import ConfiguracionController
from utilities.auxiliar import (
    crear_directorio_id_documento,
    abrir_archivo,
    generar_ruta_documento,
    copiar_archivo,
)
from utilities.configuracion import DIRECTORIO_TEMPORAL
from views.dialogs.dialog_visualizar_metadatos import DialogVisualizarMetadatos
from ttkbootstrap.constants import *

ANCHO_PORTADA = 100
PORTADAS_POR_REPISA = 8
DOCUMENTOS_POR_PAGINA = 40  # Número de documentos por página


class ControlarVisualizarEstante:
    """
    Controlador para la lógica de visualización y búsqueda en el estante.
    """

    def __init__(
        self,
        master: Frame,
        map_widgets: Dict[str, Any],
        map_vars: Dict[str, Any],
        map_documentos: Dict[str, Any],
        scroll_frame: ScrolledFrame,
    ):
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars
        self.map_documentos = map_documentos
        self.scroll_frame = scroll_frame
        self.config = ConfiguracionController()

        # Acceso a los widgets
        self.ent_buscar: Entry = self.map_widgets["ent_buscar"]
        self.cbx_campos: Combobox = self.map_widgets["cbx_campos"]
        self.btn_buscar: Button = self.map_widgets["btn_buscar"]
        self.btn_anterior: Button = self.map_widgets.get("btn_anterior")
        self.btn_siguiente: Button = self.map_widgets.get("btn_siguiente")
        self.lbl_pagina: Label = self.map_widgets.get("lbl_pagina")

        # Acceso a las variables
        self.var_buscar: StringVar = self.map_vars["var_buscar"]

        # Variables de paginación
        self.pagina_actual = 1
        self.total_documentos = 0
        self.campo_busqueda_actual = ""
        self.termino_busqueda_actual = ""

        # Almacenamiento de referencias de imágenes para evitar que el recolector de basura las elimine
        self._referencias_imagenes = []
        self.documento_seleccionado_contextual = None

        self._crear_menu_contextual()
        self._vincular_eventos()
        self._cargar_estante()

    def _crear_menu_contextual(self):
        """Crea el menú contextual para las portadas."""
        self.menu_contextual = Menu(self.master, tearoff=0)
        self.menu_contextual.add_command(
            label="📖 Abrir documento", command=self._on_abrir_documento_contextual
        )
        self.menu_contextual.add_command(
            label="ℹ️ Ver detalles", command=self._on_ver_detalles_contextual
        )
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(
            label="⭐ Marcar como favorito",  # El texto se actualizará dinámicamente
            command=self._on_marcar_favorito_contextual,
        )

    def _vincular_eventos(self):
        """Vincula los eventos de los widgets a los métodos del controlador."""
        self.btn_buscar.config(command=self.on_buscar)
        self.ent_buscar.bind("<Return>", self.on_buscar)
        if self.btn_anterior:
            self.btn_anterior.config(command=self.on_pagina_anterior)
        if self.btn_siguiente:
            self.btn_siguiente.config(command=self.on_pagina_siguiente)

    def _cargar_estante(self):
        """Inicializa el estante mostrando el catálogo completo paginado."""
        self.campo_busqueda_actual = "todo"
        self.termino_busqueda_actual = ""
        self.pagina_actual = 1
        self.total_documentos = Consulta().contar_resultados_busqueda(campo="todo", termino="")
        self._mostrar_pagina_actual()

    def on_buscar(self, event=None):
        """Maneja el evento de búsqueda."""
        termino_busqueda = self.var_buscar.get()
        campo_seleccionado = self.cbx_campos.get()

        # Mapeo de texto de UI a nombre de campo en BD
        mapa_campos = {
            "Título": "titulo",
            "Autores": "autores",
            "Editorial": "editorial",
            "ISBN": "isbn",
            "Colección": "coleccion",
            "Grupo": "grupo",
            "Nombre": "nombre",
            "Todo": "todo",
        }
        campo_db = mapa_campos.get(campo_seleccionado, "todo")

        if not termino_busqueda.strip() and campo_seleccionado.lower() != "todo":
            self._cargar_estante()
            return

        if not termino_busqueda.strip() and campo_db != "todo":
            showwarning(
                "Búsqueda vacía", "Por favor, ingrese un término para buscar.", parent=self.master
            )
            return

        # Obtener total de resultados para paginación
        self.total_documentos = Consulta().contar_resultados_busqueda(
            campo=campo_db, termino=termino_busqueda
        )
        self.campo_busqueda_actual = campo_db
        self.termino_busqueda_actual = termino_busqueda
        self.pagina_actual = 1
        self._mostrar_pagina_actual()

    def _mostrar_documentos_en_estante(self, lista_documentos):
        """
        Renderiza las portadas de los documentos en el ScrolledFrame.
        """
        # Limpiar widgets anteriores
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self._referencias_imagenes.clear()
        ruta_portadas = self.config.obtener_ubicacion_portadas()

        if not lista_documentos:
            Label(
                self.scroll_frame, text="No se encontraron documentos.", bootstyle="inverse-dark"
            ).pack(pady=20)
            return

        # Contenedor principal dentro del ScrolledFrame
        main_container = Frame(self.scroll_frame, bootstyle="dark")
        main_container.pack(fill=X, padx=10, pady=10)

        repisa_actual = None
        tareas_carga = []

        for i, doc in enumerate(lista_documentos):
            # Crear una nueva repisa cada 5 portadas
            if i % PORTADAS_POR_REPISA == 0:
                repisa_actual = Frame(main_container, bootstyle="dark")
                repisa_actual.pack(fill=X, pady=10)
                Separator(main_container, bootstyle="secondary").pack(fill=X, padx=20)

            id_documento = doc["id"]
            nombre_documento = doc["nombre"]

            # Crear un frame para cada portada y su etiqueta
            frame_portada = Frame(repisa_actual, bootstyle="dark")
            frame_portada.pack(side=LEFT, anchor=N, padx=10, pady=10)

            # --- Tooltip ---
            nombre = doc.get("nombre", "N/A")
            titulo = doc.get("titulo")  # Será None si no existe
            paginas = doc.get("numero_paginas")
            tamano_bytes = doc.get("tamano", 0)
            tamano_str = self._formatear_tamano(tamano_bytes)

            tooltip_text = f"Nombre: {nombre}"
            if titulo:
                tooltip_text += f"\nTítulo: {titulo}"
            if paginas:
                tooltip_text += f"\nPáginas: {paginas}"
            tooltip_text += f"\nTamaño: {tamano_str}"
            ToolTip(frame_portada, text=tooltip_text, bootstyle=(INFO, INVERSE))

            ruta_portada_miniatura = os.path.join(
                crear_directorio_id_documento(ruta_portadas, id_documento),
                f"{id_documento}_miniatura.png",
            )

            # Placeholder inicial mientras carga
            lbl_imagen = Label(frame_portada, bootstyle="dark", text="⌛", font=("Helvetica", 16))

            # Añadir a la lista de tareas para el hilo
            tareas_carga.append((ruta_portada_miniatura, lbl_imagen))

            lbl_imagen.pack(pady=(0, 5))

            lbl_nombre = Label(
                frame_portada,
                text=nombre_documento,
                bootstyle="inverse-dark",
                wraplength=ANCHO_PORTADA,  # Ajustar texto al ancho de la portada
                justify=CENTER,
            )
            lbl_nombre.pack()

            # --- Vinculación de eventos ---
            # Usamos una función lambda para pasar el documento específico al manejador
            handler_contextual = lambda event, d=doc: self._mostrar_menu_contextual(event, d)
            frame_portada.bind("<Button-3>", handler_contextual)
            lbl_imagen.bind("<Button-3>", handler_contextual)
            lbl_nombre.bind("<Button-3>", handler_contextual)

            # Doble clic para abrir el documento
            handler_abrir = lambda event, d=doc: self._abrir_documento(d)
            frame_portada.bind("<Double-1>", handler_abrir)
            lbl_imagen.bind("<Double-1>", handler_abrir)
            lbl_nombre.bind("<Double-1>", handler_abrir)

        # Iniciar hilo de carga
        threading.Thread(
            target=self._procesar_carga_imagenes, args=(tareas_carga,), daemon=True
        ).start()

    def _mostrar_pagina_actual(self):
        """Muestra la página actual de documentos."""
        if not self.campo_busqueda_actual:
            self._cargar_estante()
            return
        offset = (self.pagina_actual - 1) * DOCUMENTOS_POR_PAGINA
        documentos_pagina = Consulta().buscar_en_estante(
            campo=self.campo_busqueda_actual,
            termino=self.termino_busqueda_actual,
            limit=DOCUMENTOS_POR_PAGINA,
            offset=offset,
        )
        self._mostrar_documentos_en_estante(documentos_pagina)
        self._actualizar_controles_paginacion()

    def _actualizar_controles_paginacion(self):
        """Actualiza los controles de paginación."""
        total_paginas = (self.total_documentos + DOCUMENTOS_POR_PAGINA - 1) // DOCUMENTOS_POR_PAGINA
        total_paginas = max(1, total_paginas)
        if self.lbl_pagina:
            self.lbl_pagina.config(text=f"Página {self.pagina_actual} de {total_paginas}")
        if self.btn_anterior:
            self.btn_anterior.config(state=NORMAL if self.pagina_actual > 1 else DISABLED)
        if self.btn_siguiente:
            self.btn_siguiente.config(
                state=NORMAL if self.pagina_actual < total_paginas else DISABLED
            )

    def on_pagina_anterior(self):
        """Navega a la página anterior."""
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self._mostrar_pagina_actual()

    def on_pagina_siguiente(self):
        """Navega a la página siguiente."""
        total_paginas = (self.total_documentos + DOCUMENTOS_POR_PAGINA - 1) // DOCUMENTOS_POR_PAGINA
        if self.pagina_actual < total_paginas:
            self.pagina_actual += 1
            self._mostrar_pagina_actual()

    def recargar_estante(self):
        """
        Refresca el estado visual del estante.
        Si hay una búsqueda activa, recarga la página actual.
        """
        if self.termino_busqueda_actual:
            self._mostrar_pagina_actual()
            return

        self.pagina_actual = 1
        self.total_documentos = 0
        self._cargar_estante()
        self._actualizar_controles_paginacion()

    def _procesar_carga_imagenes(self, tareas):
        """Procesa la carga de imágenes en un hilo separado."""
        for ruta, label in tareas:
            if os.path.exists(ruta):
                try:
                    img = Image.open(ruta)
                    img.thumbnail((ANCHO_PORTADA, ANCHO_PORTADA * 1.5))
                    img.load()  # Forzar carga en memoria
                    self.master.after(0, self._actualizar_imagen_label, label, img)
                except Exception as e:
                    print(f"Error al cargar la imagen {ruta}: {e}")
                    self.master.after(0, self._configurar_label_error, label)
            else:
                self.master.after(0, self._configurar_label_sin_portada, label)

    def _actualizar_imagen_label(self, label, pil_image):
        """Actualiza el label con la imagen cargada (en el hilo principal)."""
        try:
            if label.winfo_exists():
                photo = ImageTk.PhotoImage(pil_image)
                label.config(text="", image=photo)
                self._referencias_imagenes.append(photo)
        except Exception:
            pass

    def _configurar_label_sin_portada(self, label):
        """Configura el label cuando no hay portada (en el hilo principal)."""
        try:
            if label.winfo_exists():
                label.config(
                    text="🖼️\nSin Portada", font=("Helvetica", 10), bootstyle="inverse-dark"
                )
        except Exception:
            pass

    def _configurar_label_error(self, label):
        """Configura el label cuando hay error (en el hilo principal)."""
        try:
            if label.winfo_exists():
                label.config(text="🖼️\nError", font=("Helvetica", 10))
        except Exception:
            pass

    # --- Métodos para el menú contextual ---

    def _mostrar_menu_contextual(self, event, documento):
        """Guarda el documento seleccionado y muestra el menú en la posición del cursor."""
        self.documento_seleccionado_contextual = documento

        # Actualizar etiqueta del menú de favoritos
        es_favorito = documento.get("es_favorito", 0)
        label_favorito = "🌟 Quitar de favoritos" if es_favorito else "⭐ Marcar como favorito"
        # El índice 3 corresponde al comando de favoritos (0: Abrir, 1: Detalles, 2: Separador, 3: Favorito)
        self.menu_contextual.entryconfig(3, label=label_favorito)

        self.menu_contextual.post(event.x_root, event.y_root)

    def _on_abrir_documento_contextual(self):
        """Manejador para la opción 'Abrir' del menú."""
        if self.documento_seleccionado_contextual:
            self._abrir_documento(self.documento_seleccionado_contextual)

    def _on_ver_detalles_contextual(self):
        """Manejador para la opción 'Ver detalles' del menú. Abre el diálogo de metadatos."""
        if not self.documento_seleccionado_contextual:
            return

        doc_id = self.documento_seleccionado_contextual["id"]
        # Creamos una instancia de Documento para pasarla al diálogo
        doc_obj = Documento(id=doc_id, nombre="", extension="", hash="", tamano=0)

        if doc_obj.instanciar():
            dialog = DialogVisualizarMetadatos(title="Metadatos del Documento", master=self.master)
            dialog.set_documento(doc_obj)
            dialog.grab_set()
        else:
            showerror(
                "Error",
                "No se pudo cargar la información completa del documento.",
                parent=self.master,
            )

    def _on_marcar_favorito_contextual(self):
        """Manejador para la opción 'Marcar/Quitar favorito' del menú."""
        if not self.documento_seleccionado_contextual:
            return

        doc_id = self.documento_seleccionado_contextual["id"]
        # Creamos una instancia de Documento para pasarla al diálogo
        doc_obj = Documento(id=doc_id, nombre="", extension="", hash="", tamano=0)

        es_favorito_actual = self.documento_seleccionado_contextual.get("es_favorito", 0)
        favorito = Favorito(id_documento=doc_id)

        if es_favorito_actual:
            if favorito.desmarcar():
                showinfo("Favorito", "Documento quitado de favoritos.", parent=self.master)
                self.documento_seleccionado_contextual["es_favorito"] = 0
            else:
                showerror("Error", "No se pudo quitar de favoritos.", parent=self.master)
        else:
            if favorito.marcar():
                showinfo("Favorito", "Documento añadido a favoritos.", parent=self.master)
                self.documento_seleccionado_contextual["es_favorito"] = 1
            else:
                showerror("Error", "No se pudo añadir a favoritos.", parent=self.master)

    def _abrir_documento(self, doc_data: Dict[str, Any]):
        """Abre un documento copiándolo a la carpeta temporal."""
        ruta_biblioteca = self.config.obtener_ubicacion_biblioteca()
        if not ruta_biblioteca or not os.path.exists(ruta_biblioteca):
            showerror(
                "Error de Configuración",
                "La ubicación de la biblioteca no está configurada o no existe.",
                parent=self.master,
            )
            return

        nombre_archivo = f"{doc_data['nombre']}.{doc_data['extension']}"
        ruta_origen = generar_ruta_documento(
            ruta_biblioteca=ruta_biblioteca,
            id_documento=doc_data["id"],
            nombre_documento=nombre_archivo,
        )

        if not os.path.exists(ruta_origen):
            showerror(
                "Archivo no encontrado",
                f"El archivo no se encontró en la biblioteca:\n{ruta_origen}",
                parent=self.master,
            )
            return

        ruta_destino_temporal = os.path.join(DIRECTORIO_TEMPORAL, nombre_archivo)
        try:
            copiar_archivo(ruta_origen=ruta_origen, ruta_destino=ruta_destino_temporal)
            abrir_archivo(ruta_origen=ruta_destino_temporal)
        except Exception as e:
            showerror("Error al abrir", f"No se pudo abrir el documento: {e}", parent=self.master)

    def _formatear_tamano(self, bytes_size: int) -> str:
        """
        Formatea el tamaño de un archivo de bytes a una unidad legible.
        """
        if not isinstance(bytes_size, (int, float)) or bytes_size < 0:
            return "0 B"

        if bytes_size == 0:
            return "0 B"

        unidades = ["B", "KB", "MB", "GB", "TB", "PB"]
        # Calcular el índice de la unidad apropiada
        try:
            indice = min(int(math.log(bytes_size, 1024)), len(unidades) - 1)
        except (ValueError, TypeError):
            return "0 B"

        # Calcular el valor en la unidad correspondiente
        valor = bytes_size / (1024**indice)

        # Formatear según la unidad
        if indice == 0:  # Bytes
            return f"{int(valor)} B"
        else:
            return f"{valor:.2f} {unidades[indice]}"
