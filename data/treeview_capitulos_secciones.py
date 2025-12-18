import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Optional, Dict, List
from models.entities.capitulo import Capitulo
from models.entities.seccion import Seccion


class GestorDocumentoTreeView:
    """
    Gestor del TreeView para mostrar la estructura jerárquica 
    de Capítulos y Secciones de un documento.
    """
    
    def __init__(self, parent, ruta_db: Optional[str] = None):
        """
        Inicializa el TreeView y sus componentes.
        
        Args:
            parent: Widget padre donde se colocará el TreeView
            ruta_db: Ruta a la base de datos (opcional)
        """
        self.ruta_db = ruta_db
        
        # Frame principal
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Crear TreeView con columnas
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Tipo", "Nivel", "Página"),
            show="tree headings",
            height=20
        )
        
        # Configurar encabezados
        self.tree.heading("#0", text="Título")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Nivel", text="Nivel")
        self.tree.heading("Página", text="Página")
        
        # Configurar anchos
        self.tree.column("#0", width=300)
        self.tree.column("Tipo", width=100)
        self.tree.column("Nivel", width=100)
        self.tree.column("Página", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Vincular eventos
        self.tree.bind("<<TreeviewSelect>>", self.on_seleccion_cambio)
        self.tree.bind("<Double-1>", self.on_doble_click)
        
        # Diccionario para mapear IID -> objeto (Capitulo o Seccion)
        self.mapa_items: Dict[str, tuple] = {}
    
    def limpiar(self):
        """Limpia todo el contenido del árbol."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.mapa_items.clear()
    
    def agregar_capitulo(self, capitulo: Capitulo) -> str:
        """
        Agrega un capítulo al árbol.
        
        Args:
            capitulo: Instancia de Capitulo a agregar
            
        Returns:
            IID del nodo insertado
        """
        # Crear IID usando el patrón: cap_<id>
        iid = f"cap_{capitulo.id}"
        
        # Insertar en el árbol
        self.tree.insert(
            "",  # Parent = raíz
            END,
            iid=iid,
            text=f"Cap {capitulo.numero_capitulo}: {capitulo.titulo}",
            values=("Capítulo", capitulo.numero_capitulo, capitulo.pagina_inicio or ""),
            tags=("capitulo",)
        )
        
        # Guardar en el mapa: (tipo, objeto)
        self.mapa_items[iid] = ("capitulo", capitulo)
        
        # Aplicar formato visual
        self.tree.tag_configure("capitulo", font=("", 10, "bold"))
        
        return iid
    
    def agregar_seccion(self, seccion: Seccion) -> str:
        """
        Agrega una sección al árbol bajo su capítulo correspondiente.
        
        Args:
            seccion: Instancia de Seccion a agregar
            
        Returns:
            IID del nodo insertado
        """
        # Crear IID usando el patrón: sec_<id>
        iid = f"sec_{seccion.id}"
        
        # Determinar el padre
        if seccion.id_padre:
            # Es una subsección
            parent_iid = f"sec_{seccion.id_padre}"
        else:
            # Es una sección de primer nivel, su padre es el capítulo
            parent_iid = f"cap_{seccion.id_capitulo}"
        
        # Verificar que el padre exista
        if not self.tree.exists(parent_iid):
            print(f"Advertencia: El padre {parent_iid} no existe para la sección {iid}")
            return ""
        
        # Insertar en el árbol
        self.tree.insert(
            parent_iid,
            END,
            iid=iid,
            text=seccion.titulo,
            values=("Sección", seccion.nivel or "", seccion.numero_pagina or ""),
            tags=("seccion",)
        )
        
        # Guardar en el mapa
        self.mapa_items[iid] = ("seccion", seccion)
        
        # Aplicar formato visual
        self.tree.tag_configure("seccion", font=("", 9))
        
        return iid
    
    def cargar_documento(self, id_documento: int):
        """
        Carga todos los capítulos y secciones de un documento.
        
        Args:
            id_documento: ID del documento a cargar
        """
        self.limpiar()
        
        # Cargar capítulos (necesitarías implementar un método en tu DAO)
        # Este es un ejemplo conceptual
        capitulo_dao = Capitulo(
            id_documento=id_documento,
            numero_capitulo=0,
            titulo="",
            ruta_db=self.ruta_db
        )._dao
        
        # Obtener todos los capítulos del documento
        capitulos_data = capitulo_dao.obtener_por_documento(id_documento)
        
        for cap_data in capitulos_data:
            # Crear objeto Capitulo
            cap = Capitulo(
                id=cap_data["id"],
                id_documento=cap_data["id_documento"],
                numero_capitulo=cap_data["numero_capitulo"],
                titulo=cap_data["titulo"],
                pagina_inicio=cap_data.get("pagina_inicio"),
                ruta_db=self.ruta_db
            )
            
            # Agregar al árbol
            cap_iid = self.agregar_capitulo(cap)
            
            # Cargar secciones del capítulo
            self._cargar_secciones_capitulo(cap.id)
    
    def _cargar_secciones_capitulo(self, id_capitulo: int):
        """
        Carga todas las secciones de un capítulo específico.
        
        Args:
            id_capitulo: ID del capítulo
        """
        seccion_dao = Seccion(
            id_capitulo=id_capitulo,
            titulo="",
            ruta_db=self.ruta_db
        )._dao
        
        # Obtener todas las secciones del capítulo
        secciones_data = seccion_dao.obtener_por_capitulo(id_capitulo)
        
        for sec_data in secciones_data:
            # Crear objeto Seccion
            sec = Seccion(
                id=sec_data["id"],
                id_capitulo=sec_data["id_capitulo"],
                titulo=sec_data["titulo"],
                nivel=sec_data.get("nivel"),
                id_padre=sec_data.get("id_padre"),
                numero_pagina=sec_data.get("numero_pagina"),
                ruta_db=self.ruta_db
            )
            
            # Agregar al árbol
            self.agregar_seccion(sec)
    
    def obtener_seleccion(self) -> Optional[tuple]:
        """
        Obtiene el item seleccionado en el árbol.
        
        Returns:
            Tupla (tipo, objeto) donde:
            - tipo: "capitulo" o "seccion"
            - objeto: instancia de Capitulo o Seccion
            None si no hay selección
        """
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        
        iid = seleccion[0]
        return self.mapa_items.get(iid)
    
    def identificar_tipo_seleccion(self) -> Optional[str]:
        """
        Identifica el tipo del nodo seleccionado.
        
        Returns:
            "capitulo", "seccion" o None
        """
        resultado = self.obtener_seleccion()
        if resultado:
            return resultado[0]
        return None
    
    def on_seleccion_cambio(self, event):
        """Evento disparado cuando cambia la selección."""
        resultado = self.obtener_seleccion()
        
        if not resultado:
            print("No hay selección")
            return
        
        tipo, objeto = resultado
        
        if tipo == "capitulo":
            cap: Capitulo = objeto
            print(f"\n{'='*50}")
            print(f"CAPÍTULO SELECCIONADO")
            print(f"{'='*50}")
            print(f"ID: {cap.id}")
            print(f"Número: {cap.numero_capitulo}")
            print(f"Título: {cap.titulo}")
            print(f"Página inicio: {cap.pagina_inicio}")
            print(f"ID Documento: {cap.id_documento}")
            
        elif tipo == "seccion":
            sec: Seccion = objeto
            print(f"\n{'='*50}")
            print(f"SECCIÓN SELECCIONADA")
            print(f"{'='*50}")
            print(f"ID: {sec.id}")
            print(f"Título: {sec.titulo}")
            print(f"Nivel: {sec.nivel}")
            print(f"Página: {sec.numero_pagina}")
            print(f"ID Capítulo: {sec.id_capitulo}")
            print(f"ID Padre: {sec.id_padre}")
    
    def on_doble_click(self, event):
        """Evento disparado en doble click."""
        resultado = self.obtener_seleccion()
        
        if not resultado:
            return
        
        tipo, objeto = resultado
        
        if tipo == "capitulo":
            print(f"\n✏️  Editando capítulo: {objeto.titulo}")
            # Aquí podrías abrir un diálogo de edición
            
        elif tipo == "seccion":
            print(f"\n✏️  Editando sección: {objeto.titulo}")
            # Aquí podrías abrir un diálogo de edición
    
    def eliminar_seleccion(self):
        """Elimina el item seleccionado del árbol y de la base de datos."""
        resultado = self.obtener_seleccion()
        
        if not resultado:
            print("No hay nada seleccionado para eliminar")
            return
        
        tipo, objeto = resultado
        seleccion = self.tree.selection()[0]
        
        # Confirmar eliminación
        if tipo == "capitulo":
            respuesta = ttk.dialogs.Messagebox.yesno(
                f"¿Eliminar el capítulo '{objeto.titulo}' y todas sus secciones?",
                "Confirmar eliminación"
            )
        else:
            respuesta = ttk.dialogs.Messagebox.yesno(
                f"¿Eliminar la sección '{objeto.titulo}'?",
                "Confirmar eliminación"
            )
        
        if respuesta == "Yes":
            # Eliminar de la base de datos
            if objeto.eliminar():
                # Eliminar del árbol
                self.tree.delete(seleccion)
                # Eliminar del mapa
                del self.mapa_items[seleccion]
                print(f"✅ {tipo.capitalize()} eliminado correctamente")
            else:
                print(f"❌ Error al eliminar {tipo}")


# =============================================================================
# EJEMPLO DE USO
# =============================================================================

def main():
    # Crear ventana
    root = ttk.Window(themename="darkly")
    root.title("Estructura de Documento")
    root.geometry("800x600")
    
    # Crear gestor del TreeView
    gestor = GestorDocumentoTreeView(root, ruta_db="tu_base_datos.db")
    
    # Frame de botones
    btn_frame = ttk.Frame(root)
    btn_frame.pack(fill=X, padx=10, pady=5)
    
    def mostrar_tipo():
        tipo = gestor.identificar_tipo_seleccion()
        if tipo:
            ttk.dialogs.Messagebox.show_info(
                f"Has seleccionado un: {tipo}",
                "Tipo de selección"
            )
        else:
            ttk.dialogs.Messagebox.show_warning(
                "No hay nada seleccionado",
                "Aviso"
            )
    
    def agregar_ejemplo():
        # Ejemplo de cómo agregar datos manualmente
        cap = Capitulo(
            id=1,
            id_documento=1,
            numero_capitulo=1,
            titulo="Introducción",
            pagina_inicio=1,
            ruta_db="tu_base_datos.db"
        )
        gestor.agregar_capitulo(cap)
        
        sec = Seccion(
            id=1,
            id_capitulo=1,
            titulo="Antecedentes",
            nivel="1.1",
            numero_pagina=2,
            ruta_db="tu_base_datos.db"
        )
        gestor.agregar_seccion(sec)
        
        sec2 = Seccion(
            id=2,
            id_capitulo=1,
            titulo="Objetivos",
            nivel="1.2",
            numero_pagina=5,
            ruta_db="tu_base_datos.db"
        )
        gestor.agregar_seccion(sec2)
    
    ttk.Button(btn_frame, text="Identificar Tipo", 
              command=mostrar_tipo).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Eliminar Selección", 
              command=gestor.eliminar_seleccion).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Limpiar Todo", 
              command=gestor.limpiar).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Agregar Ejemplo", 
              command=agregar_ejemplo).pack(side=LEFT, padx=5)
    
    # Label de información
    info_label = ttk.Label(
        root,
        text="💡 Selecciona un nodo para ver su información en la consola\n"
             "Doble click para editar",
        bootstyle="info"
    )
    info_label.pack(pady=5)
    
    # Cargar datos de ejemplo (comentado, descomenta cuando tengas tu BD lista)
    # gestor.cargar_documento(id_documento=1)
    
    root.mainloop()


if __name__ == "__main__":
    main()
