# Tutorial de Treeview en ttkbootstrap

## Introducción

El widget `Treeview` en ttkbootstrap es una herramienta poderosa para mostrar datos jerárquicos en forma de árbol. Este tutorial cubre las operaciones más comunes.

## Instalación

```bash
pip install ttkbootstrap
```

## Configuración Básica

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Crear ventana principal
root = ttk.Window(themename="darkly")
root.title("Tutorial Treeview")
root.geometry("600x400")

# Crear Treeview con columnas
tree = ttk.Treeview(root, columns=("Edad", "Ciudad"), show="tree headings")

# Configurar encabezados
tree.heading("#0", text="Nombre")
tree.heading("Edad", text="Edad")
tree.heading("Ciudad", text="Ciudad")

# Configurar ancho de columnas
tree.column("#0", width=200)
tree.column("Edad", width=100)
tree.column("Ciudad", width=150)

tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
```

## Métodos Principales

### 1. Insertar Nodos

```python
def insertar_nodo(parent="", index=END, text="", values=()):
    """
    Inserta un nodo en el Treeview
    
    Args:
        parent: ID del nodo padre ("" para raíz)
        index: Posición de inserción (END para el final)
        text: Texto a mostrar en la primera columna
        values: Tupla con valores para las demás columnas
    
    Returns:
        ID del nodo insertado
    """
    return tree.insert(parent, index, text=text, values=values)

# Ejemplos de uso
raiz1 = insertar_nodo(text="Juan Pérez", values=(30, "Madrid"))
hijo1 = insertar_nodo(parent=raiz1, text="María Pérez", values=(5, "Madrid"))
raiz2 = insertar_nodo(text="Ana García", values=(28, "Barcelona"))
```

### 2. Limpiar el Árbol

```python
def limpiar_arbol():
    """
    Elimina todos los elementos del Treeview
    """
    for item in tree.get_children():
        tree.delete(item)

# Uso
# limpiar_arbol()
```

### 3. Eliminar Nodos Específicos

```python
def eliminar_nodo_seleccionado():
    """
    Elimina el nodo actualmente seleccionado
    """
    seleccion = tree.selection()
    if seleccion:
        for item in seleccion:
            tree.delete(item)
    else:
        print("No hay ningún nodo seleccionado")

def eliminar_nodo_por_id(item_id):
    """
    Elimina un nodo específico por su ID
    
    Args:
        item_id: ID del nodo a eliminar
    """
    try:
        tree.delete(item_id)
    except:
        print(f"No se pudo eliminar el nodo {item_id}")
```

### 4. Seleccionar Nodos

```python
def seleccionar_nodo(item_id):
    """
    Selecciona un nodo específico
    
    Args:
        item_id: ID del nodo a seleccionar
    """
    tree.selection_set(item_id)
    tree.focus(item_id)
    tree.see(item_id)  # Hace scroll para mostrar el nodo

def obtener_seleccion():
    """
    Obtiene los IDs de los nodos seleccionados
    
    Returns:
        Tupla con los IDs seleccionados
    """
    return tree.selection()
```

### 5. Obtener Datos de Nodos

```python
def obtener_datos_nodo(item_id):
    """
    Obtiene todos los datos de un nodo
    
    Args:
        item_id: ID del nodo
    
    Returns:
        Diccionario con los datos del nodo
    """
    return {
        'text': tree.item(item_id, 'text'),
        'values': tree.item(item_id, 'values'),
        'parent': tree.parent(item_id),
        'children': tree.get_children(item_id)
    }

def obtener_datos_seleccionados():
    """
    Obtiene los datos de todos los nodos seleccionados
    
    Returns:
        Lista de diccionarios con los datos
    """
    seleccion = tree.selection()
    datos = []
    
    for item_id in seleccion:
        datos.append({
            'id': item_id,
            'text': tree.item(item_id, 'text'),
            'values': tree.item(item_id, 'values')
        })
    
    return datos

def mostrar_datos_seleccionados():
    """
    Imprime los datos de los nodos seleccionados
    """
    datos = obtener_datos_seleccionados()
    
    if not datos:
        print("No hay nodos seleccionados")
        return
    
    for item in datos:
        print(f"ID: {item['id']}")
        print(f"Nombre: {item['text']}")
        print(f"Edad: {item['values'][0]}, Ciudad: {item['values'][1]}")
        print("-" * 40)
```

## Ejemplo Completo con Interfaz

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class TreeviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Treeview")
        self.root.geometry("700x500")
        
        # Crear Treeview
        self.tree = ttk.Treeview(root, columns=("Edad", "Ciudad"), 
                                 show="tree headings", height=15)
        
        self.tree.heading("#0", text="Nombre")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Ciudad", text="Ciudad")
        
        self.tree.column("#0", width=250)
        self.tree.column("Edad", width=100)
        self.tree.column("Ciudad", width=150)
        
        self.tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Frame de botones
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Insertar Nodo", 
                  command=self.insertar_ejemplo).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Selección", 
                  command=self.eliminar_seleccionado).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar Todo", 
                  command=self.limpiar).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Mostrar Selección", 
                  command=self.mostrar_seleccion).pack(side=LEFT, padx=5)
        
        # Agregar datos iniciales
        self.cargar_datos_ejemplo()
    
    def insertar_ejemplo(self):
        seleccion = self.tree.selection()
        parent = seleccion[0] if seleccion else ""
        self.tree.insert(parent, END, text="Nuevo Nodo", 
                        values=("25", "Ciudad"))
    
    def eliminar_seleccionado(self):
        for item in self.tree.selection():
            self.tree.delete(item)
    
    def limpiar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def mostrar_seleccion(self):
        for item_id in self.tree.selection():
            datos = self.tree.item(item_id)
            print(f"Seleccionado: {datos['text']} - {datos['values']}")
    
    def cargar_datos_ejemplo(self):
        p1 = self.tree.insert("", END, text="Carlos López", 
                             values=(45, "Madrid"))
        self.tree.insert(p1, END, text="Laura López", 
                        values=(20, "Madrid"))
        self.tree.insert(p1, END, text="Pedro López", 
                        values=(18, "Madrid"))
        
        p2 = self.tree.insert("", END, text="Elena Martín", 
                             values=(38, "Barcelona"))
        self.tree.insert(p2, END, text="Sofia Martín", 
                        values=(12, "Barcelona"))

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = TreeviewApp(root)
    root.mainloop()
```

## Eventos Útiles

```python
# Detectar doble clic
def on_double_click(event):
    item = tree.selection()[0]
    print(f"Doble clic en: {tree.item(item, 'text')}")

tree.bind("<Double-1>", on_double_click)

# Detectar cambio de selección
def on_select(event):
    seleccion = tree.selection()
    if seleccion:
        print(f"Seleccionado: {tree.item(seleccion[0], 'text')}")

tree.bind("<<TreeviewSelect>>", on_select)
```

## Consejos y Buenas Prácticas

1. **Guarda los IDs**: Almacena los IDs de los nodos insertados si necesitas referenciarlos después
2. **Valida selecciones**: Siempre verifica si hay algo seleccionado antes de operar
3. **Usa parent=""**: Para insertar en la raíz del árbol
4. **Mantén la jerarquía**: Los nodos hijos se eliminan automáticamente al eliminar el padre
5. **Optimiza inserciones**: Para muchos datos, considera deshabilitar la actualización visual temporalmente

## Recursos Adicionales

- [Documentación oficial de ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
- [Tkinter Treeview Reference](https://docs.python.org/3/library/tkinter.ttk.html#treeview)