# Explicación de `trace` en Tkinter/ttkbootstrap

`trace` es un mecanismo que permite **observar** y **reaccionar** a los cambios en las variables de Tkinter (`StringVar`, `IntVar`, `BooleanVar`, etc.).

## Concepto básico

Es como un "espía" que vigila una variable y ejecuta una función cada vez que detecta un cambio.

## Sintaxis

```python
variable.trace_add(mode, callback)
```

### Modos disponibles:

- **`"write"`**: Se ejecuta cuando la variable **cambia de valor**
- **`"read"`**: Se ejecuta cuando se **lee** la variable
- **`"unset"`**: Se ejecuta cuando la variable se **elimina**

## Ejemplo simple

```python
import ttkbootstrap as ttk

root = ttk.Window()

# Crear variable
nombre = ttk.StringVar()

# Función que se ejecuta cuando cambia
def cuando_cambia(*args):
    print(f"El nombre cambió a: {nombre.get()}")

# Agregar el "espía"
nombre.trace_add("write", cuando_cambia)

# Entry vinculado a la variable
entry = ttk.Entry(root, textvariable=nombre)
entry.pack(padx=20, pady=20)

root.mainloop()
```

**Resultado**: Cada vez que escribes en el Entry, se imprime el nuevo valor automáticamente.

## Ejemplo con Checkbutton

```python
import ttkbootstrap as ttk

root = ttk.Window()

check_var = ttk.BooleanVar()

def cuando_cambia_check(*args):
    if check_var.get():
        print("✓ Checkbox activado")
    else:
        print("☐ Checkbox desactivado")

# El trace detecta cuando haces clic
check_var.trace_add("write", cuando_cambia_check)

check = ttk.Checkbutton(
    root, 
    text="Aceptar términos",
    variable=check_var
)
check.pack(padx=20, pady=20)

root.mainloop()
```

## Uso en código real

```python
# En _cargar_colecciones
var = BooleanVar(value=False)

# Cada vez que se marca/desmarca el checkbox, se ejecuta on_coleccion_seleccionado
var.trace_add('write', lambda *args: self.on_coleccion_seleccionado())

self.var_check_colecciones[coleccion.nombre] = var
```

### ¿Por qué `lambda *args:`?

La función callback de `trace` **siempre recibe 3 argumentos automáticos**:
1. Nombre de la variable
2. Índice (vacío para variables simples)
3. Modo ('write', 'read', etc.)

Pero normalmente **no los necesitas**, por eso usamos:

```python
lambda *args: self.on_coleccion_seleccionado()
```

Esto significa: "ignora los argumentos automáticos y solo ejecuta mi función"

## Ejemplo completo práctico

```python
import ttkbootstrap as ttk

class FormularioConTrace(ttk.Window):
    def __init__(self):
        super().__init__()
        
        self.var_nombre = ttk.StringVar()
        self.var_edad = ttk.IntVar()
        self.var_acepta = ttk.BooleanVar()
        
        # Agregar traces
        self.var_nombre.trace_add("write", lambda *args: self.validar_nombre())
        self.var_edad.trace_add("write", lambda *args: self.validar_edad())
        self.var_acepta.trace_add("write", lambda *args: self.verificar_envio())
        
        # Widgets
        ttk.Label(self, text="Nombre:").pack(pady=5)
        ttk.Entry(self, textvariable=self.var_nombre).pack(pady=5)
        
        ttk.Label(self, text="Edad:").pack(pady=5)
        ttk.Entry(self, textvariable=self.var_edad).pack(pady=5)
        
        ttk.Checkbutton(
            self, 
            text="Acepto términos",
            variable=self.var_acepta
        ).pack(pady=5)
        
        self.btn_enviar = ttk.Button(
            self, 
            text="Enviar",
            state="disabled"
        )
        self.btn_enviar.pack(pady=20)
    
    def validar_nombre(self):
        nombre = self.var_nombre.get()
        if len(nombre) < 3:
            print("❌ Nombre muy corto")
        else:
            print("✓ Nombre válido")
    
    def validar_edad(self):
        try:
            edad = self.var_edad.get()
            if edad < 18:
                print("❌ Debes ser mayor de edad")
            else:
                print("✓ Edad válida")
        except:
            pass
    
    def verificar_envio(self):
        # Habilitar botón solo si acepta términos
        if self.var_acepta.get():
            self.btn_enviar.config(state="normal")
            print("✓ Botón habilitado")
        else:
            self.btn_enviar.config(state="disabled")
            print("❌ Debes aceptar términos")

if __name__ == "__main__":
    app = FormularioConTrace()
    app.mainloop()
```

## Ventajas de usar `trace`

✅ **Validación en tiempo real** mientras el usuario escribe  
✅ **Sincronización automática** entre widgets  
✅ **Lógica reactiva** sin necesidad de botones "Actualizar"  
✅ **Menos código** que usar eventos `bind()`

## Diferencia con `bind()`

```python
# CON BIND (eventos de widget)
entry.bind("<KeyRelease>", self.on_cambio)  # Solo para Entry específico

# CON TRACE (cambios de variable)
var.trace_add("write", self.on_cambio)  # Para CUALQUIER cambio en la variable
```

`trace` es más poderoso porque detecta cambios desde **cualquier lugar**, no solo eventos del usuario.

## Remover un trace

```python
# Agregar trace y guardar referencia
trace_id = variable.trace_add("write", callback)

# Remover después
variable.trace_remove("write", trace_id)
```

## Casos de uso comunes

### 1. Búsqueda en tiempo real

```python
var_busqueda = StringVar()
var_busqueda.trace_add("write", lambda *args: self.filtrar_resultados())

def filtrar_resultados(self):
    termino = self.var_busqueda.get().lower()
    # Filtrar y actualizar lista
```

### 2. Cálculos automáticos

```python
var_cantidad = IntVar()
var_precio = IntVar()
var_total = StringVar()

var_cantidad.trace_add("write", lambda *args: self.calcular_total())
var_precio.trace_add("write", lambda *args: self.calcular_total())

def calcular_total(self):
    try:
        total = self.var_cantidad.get() * self.var_precio.get()
        self.var_total.set(f"${total}")
    except:
        self.var_total.set("$0")
```

### 3. Validación de formularios

```python
var_email = StringVar()
var_email.trace_add("write", lambda *args: self.validar_email())

def validar_email(self):
    email = self.var_email.get()
    if "@" in email and "." in email:
        self.label_estado.config(text="✓ Email válido", bootstyle="success")
    else:
        self.label_estado.config(text="❌ Email inválido", bootstyle="danger")
```

## Notas importantes

- `trace` es específico de las **variables de Tkinter**, no de variables Python normales
- Puedes tener **múltiples traces** en la misma variable
- Ten cuidado con **loops infinitos** (un trace que modifica la variable que está observando)
- `trace_add()` es el método moderno, `trace()` es la versión antigua (deprecada)