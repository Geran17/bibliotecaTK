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
# show="headings" - Oculta la columna #0 y muestra solo los encabezados de las columnas definidas
# show="tree headings" - Muestra la columna #0 con el árbol y los encabezados
tree = ttk.Treeview(root, columns=("Edad", "Ciudad"), show="headings")

# Configurar encabezados (no es necesario configurar #0 si está oculta)
tree.heading("Edad", text="Edad")
tree.heading("Ciudad", text="Ciudad")

# Configurar ancho de columnas
tree.column("Edad", width=100)
tree.column("Ciudad", width=150)

tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
```

## Ocultar/Mostrar la Columna #0

La columna `#0` es la columna del árbol que muestra la jerarquía. Puedes controlar su visibilidad:

```python
# Ocultar la columna #0 (solo mostrar columnas definidas)
tree = ttk.Treeview(root, columns=("Edad", "Ciudad"), show="headings")

# Mostrar la columna #0 con el árbol (comportamiento predeterminado)
tree = ttk.Treeview(root, columns=("Edad", "Ciudad"), show="tree headings")

# Mostrar solo el árbol sin encabezados
tree = ttk.Treeview(root, columns=("Edad", "Ciudad"), show="tree")
```

**Nota importante:** Cuando ocultas la columna #0, los datos aún deben insertarse usando el parámetro `text`, pero no serán visibles. La jerarquía padre-hijo se mantiene funcionando normalmente.

## Manejo de IID (Item Identifier)

El `iid` es el identificador único de cada nodo en el Treeview. Puedes dejarlo automático o especificarlo manualmente.

### IID Automático vs Manual

```python
# IID automático (generado por Tkinter)
item1 = tree.insert("", END, text="Nodo 1", values=(25, "Madrid"))
print(item1)  # Imprime algo como: 'I001'

# IID manual (tú defines el identificador)
tree.insert("", END, iid="usuario_001", text="Nodo 2", values=(30, "Barcelona"))

# Ahora puedes usar ese ID directamente
tree.item("usuario_001", values=(31, "Barcelona"))  # Modificar
tree.delete("usuario_001")  # Eliminar
```

### Ventajas de IID Manual

- **Referencia fácil**: Puedes usar IDs significativos como "cliente_123" o "producto_456"
- **Sincronización con BD**: Usa el mismo ID de tu base de datos
- **Evita búsquedas**: No necesitas buscar el nodo, ya conoces su ID

### Ejemplo con Base de Datos

```python
import sqlite3

def cargar_usuarios_desde_bd():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.execute("SELECT id, nombre, edad, ciudad FROM usuarios")
    
    for row in cursor:
        user_id, nombre, edad, ciudad = row
        # Usar el ID de la BD como iid del Treeview
        tree.insert("", END, iid=f"user_{user_id}", 
                   text=nombre, values=(edad, ciudad))
    
    conn.close()

def actualizar_usuario_en_bd(user_id):
    # Obtener datos del Treeview usando el iid
    item_data = tree.item(f"user_{user_id}")
    edad, ciudad = item_data['values']
    
    conn = sqlite3.connect("usuarios.db")
    conn.execute("UPDATE usuarios SET edad=?, ciudad=? WHERE id=?",
                (edad, ciudad, user_id))
    conn.commit()
    conn.close()
```

### Verificar si un IID Existe

```python
def existe_iid(iid):
    """
    Verifica si un IID existe en el Treeview
    
    Args:
        iid: ID del item a verificar
    
    Returns:
        True si existe, False si no
    """
    return tree.exists(iid)

# Uso
if existe_iid("usuario_001"):
    tree.delete("usuario_001")
else:
    print("El item no existe")
```

### Obtener Todos los IIDs

```python
def obtener_todos_los_iids(parent=""):
    """
    Obtiene todos los IIDs del árbol o de un nodo específico
    
    Args:
        parent: ID del nodo padre ("" para obtener todos)
    
    Returns:
        Tupla con todos los IIDs
    """
    return tree.get_children(parent)

# Obtener todos los IIDs de nivel raíz
iids_raiz = obtener_todos_los_iids()
print(f"IIDs en raíz: {iids_raiz}")

# Obtener IIDs hijos de un nodo específico
iids_hijos = obtener_todos_los_iids("usuario_001")
print(f"IIDs hijos: {iids_hijos}")
```

### Ejemplo Completo con IID Personalizado

```python
class GestorProductos:
    def __init__(self, tree):
        self.tree = tree
        self.contador = 0
    
    def generar_iid(self, tipo="producto"):
        """Genera un IID único personalizado"""
        self.contador += 1
        return f"{tipo}_{self.contador}"
    
    def agregar_producto(self, nombre, precio, stock):
        """Agrega un producto con IID personalizado"""
        iid = self.generar_iid("producto")
        self.tree.insert("", END, iid=iid, 
                        text=nombre, values=(precio, stock))
        return iid
    
    def agregar_categoria(self, nombre):
        """Agrega una categoría con IID personalizado"""
        iid = self.generar_iid("categoria")
        self.tree.insert("", END, iid=iid, text=nombre)
        return iid
    
    def agregar_producto_a_categoria(self, categoria_iid, nombre, precio, stock):
        """Agrega un producto dentro de una categoría"""
        iid = self.generar_iid("producto")
        self.tree.insert(categoria_iid, END, iid=iid,
                        text=nombre, values=(precio, stock))
        return iid
    
    def buscar_por_iid(self, iid):
        """Busca y retorna los datos de un item por su IID"""
        if self.tree.exists(iid):
            return self.tree.item(iid)
        return None

# Uso
gestor = GestorProductos(tree)
cat1 = gestor.agregar_categoria("Electrónica")
prod1 = gestor.agregar_producto_a_categoria(cat1, "Laptop", 999.99, 10)

# Modificar producto usando su IID
tree.item(prod1, values=(899.99, 8))  # Cambiar precio y stock
```

### Mejores Prácticas con IID

1. **Usa prefijos descriptivos**: `"user_123"`, `"order_456"`, `"category_789"`
2. **Mantén consistencia**: Si usas IID manual, úsalo en todo el proyecto
3. **Evita caracteres especiales**: Usa solo letras, números y guiones bajos
4. **Guarda referencias importantes**: Almacena los IIDs en diccionarios o listas si los necesitas después
5. **Verifica existencia**: Siempre usa `tree.exists(iid)` antes de operar con un IID

## Métodos Principales

### 1. Insertar Nodos

```python
def insertar_nodo(parent="", index=END, iid=None, text="", values=()):
    """
    Inserta un nodo en el Treeview
    
    Args:
        parent: ID del nodo padre ("" para raíz)
        index: Posición de inserción (END para el final)
        iid: Identificador único del item (None para auto-generar)
        text: Texto a mostrar en la primera columna
        values: Tupla con valores para las demás columnas
    
    Returns:
        ID del nodo insertado
    """
    if iid:
        return tree.insert(parent, index, iid=iid, text=text, values=values)
    else:
        return tree.insert(parent, index, text=text, values=values)

# Ejemplos de uso
# Con IID automático
raiz1 = insertar_nodo(text="Juan Pérez", values=(30, "Madrid"))
print(f"IID generado: {raiz1}")

# Con IID manual
raiz2 = insertar_nodo(iid="user_001", text="Ana García", values=(28, "Barcelona"))
hijo1 = insertar_nodo(parent="user_001", iid="user_002", 
                     text="Pedro García", values=(5, "Barcelona"))
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
                                 show="headings", height=15)
        
        # Configurar encabezados (sin #0 porque está oculta)
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Ciudad", text="Ciudad")
        
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