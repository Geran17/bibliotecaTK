# Tutorial: Cómo Usar un Combobox en Tkinter

## ¿Qué es un Combobox?

Un Combobox (también llamado menú desplegable) es un widget que combina un campo de texto con una lista desplegable de opciones. Permite al usuario seleccionar un valor de la lista o escribir uno personalizado.

## Requisitos Previos

Para usar Combobox necesitas importar `ttk` de tkinter:

```python
import tkinter as tk
from tkinter import ttk
```

## Ejemplo Básico

```python
import tkinter as tk
from tkinter import ttk

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Ejemplo de Combobox")
ventana.geometry("300x200")

# Crear etiqueta
etiqueta = tk.Label(ventana, text="Selecciona un país:")
etiqueta.pack(pady=10)

# Crear Combobox
combo = ttk.Combobox(ventana, values=["Argentina", "Paraguay", "Brasil", "Uruguay", "Chile"])
combo.pack(pady=10)

# Establecer valor por defecto
combo.set("Paraguay")

ventana.mainloop()
```

## Propiedades Importantes

### Values (Valores)
Define la lista de opciones del Combobox:

```python
combo = ttk.Combobox(ventana, values=["Opción 1", "Opción 2", "Opción 3"])
```

### State (Estado)
Controla si el usuario puede escribir en el Combobox:

```python
# Modo normal: se puede seleccionar y escribir
combo = ttk.Combobox(ventana, state="normal")

# Modo readonly: solo se puede seleccionar de la lista
combo = ttk.Combobox(ventana, state="readonly")

# Modo disabled: deshabilitado
combo = ttk.Combobox(ventana, state="disabled")
```

### Width (Ancho)
Define el ancho del Combobox:

```python
combo = ttk.Combobox(ventana, width=30)
```

## Métodos Principales

### set() - Establecer valor
```python
combo.set("Valor por defecto")
```

### get() - Obtener valor seleccionado
```python
valor_seleccionado = combo.get()
print(valor_seleccionado)
```

### current() - Obtener/establecer índice
```python
# Obtener índice del elemento seleccionado
indice = combo.current()

# Establecer elemento por índice
combo.current(0)  # Selecciona el primer elemento
```

## Eventos del Combobox

Para detectar cuando se selecciona un valor:

```python
import tkinter as tk
from tkinter import ttk

def al_seleccionar(evento):
    print(f"Seleccionaste: {combo.get()}")

ventana = tk.Tk()
ventana.title("Combobox con Evento")
ventana.geometry("300x200")

combo = ttk.Combobox(ventana, values=["Rojo", "Verde", "Azul"])
combo.pack(pady=20)

# Vincular el evento
combo.bind("<<ComboboxSelected>>", al_seleccionar)

ventana.mainloop()
```

## Ejemplo Completo con Botón

```python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def mostrar_seleccion():
    seleccion = combo.get()
    if seleccion:
        messagebox.showinfo("Selección", f"Has seleccionado: {seleccion}")
    else:
        messagebox.showwarning("Advertencia", "Por favor selecciona una opción")

# Crear ventana
ventana = tk.Tk()
ventana.title("Combobox Completo")
ventana.geometry("350x250")

# Etiqueta
etiqueta = tk.Label(ventana, text="Selecciona tu lenguaje favorito:", font=("Arial", 12))
etiqueta.pack(pady=15)

# Combobox
lenguajes = ["Python", "JavaScript", "Java", "C++", "Ruby", "Go"]
combo = ttk.Combobox(ventana, values=lenguajes, state="readonly", width=25)
combo.pack(pady=10)
combo.set("Python")  # Valor por defecto

# Botón
boton = tk.Button(ventana, text="Confirmar", command=mostrar_seleccion, 
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
boton.pack(pady=20)

ventana.mainloop()
```

## Agregar o Modificar Valores Dinámicamente

```python
# Agregar valores después de crear el Combobox
combo["values"] = ["Nuevo1", "Nuevo2", "Nuevo3"]

# Agregar a los valores existentes
valores_actuales = list(combo["values"])
valores_actuales.append("Nuevo Item")
combo["values"] = valores_actuales
```

## Consejos y Buenas Prácticas

1. Usa `state="readonly"` si solo quieres que el usuario seleccione de la lista
2. Siempre valida que el usuario haya seleccionado algo antes de procesar
3. Establece un valor por defecto con `set()` para mejorar la experiencia del usuario
4. El evento `<<ComboboxSelected>>` es útil para actualizar la interfaz automáticamente
5. Puedes usar `current()` para seleccionar elementos por su posición en la lista

## Conclusión

El Combobox es un widget muy útil para crear interfaces limpias y fáciles de usar. Es ideal cuando necesitas que el usuario elija entre varias opciones predefinidas.