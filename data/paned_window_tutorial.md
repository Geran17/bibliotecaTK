# Tutorial de PanedWindow en ttkbootstrap

## ¿Qué es PanedWindow?

`PanedWindow` es un widget contenedor que permite dividir el espacio en múltiples paneles ajustables. Los usuarios pueden redimensionar estos paneles arrastrando los separadores entre ellos, lo que lo hace ideal para crear interfaces flexibles y personalizables.

## Instalación de ttkbootstrap

```bash
pip install ttkbootstrap
```

## Conceptos Básicos

### Importación y Creación Básica

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Crear ventana principal
root = ttk.Window(themename="superhero")

# Crear PanedWindow horizontal
paned = ttk.PanedWindow(root, orient=HORIZONTAL)
paned.pack(fill=BOTH, expand=True)

root.mainloop()
```

### Orientación

PanedWindow puede tener dos orientaciones:

- **HORIZONTAL**: Los paneles se organizan de izquierda a derecha
- **VERTICAL**: Los paneles se organizan de arriba hacia abajo

```python
# Horizontal
paned_h = ttk.PanedWindow(root, orient=HORIZONTAL)

# Vertical
paned_v = ttk.PanedWindow(root, orient=VERTICAL)
```

## Añadiendo Paneles

### Método add()

```python
# Crear frames para los paneles
frame1 = ttk.Frame(paned, width=200, height=300)
frame2 = ttk.Frame(paned, width=300, height=300)

# Añadir paneles al PanedWindow
paned.add(frame1, weight=1)
paned.add(frame2, weight=2)
```

El parámetro `weight` determina cómo se distribuye el espacio extra:
- `weight=1` y `weight=2` significa que frame2 recibirá el doble de espacio adicional que frame1

## Ejemplo Completo: Editor de Texto Dual

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

root = ttk.Window(themename="darkly")
root.title("Editor Dual con PanedWindow")
root.geometry("800x600")

# PanedWindow principal (horizontal)
paned_h = ttk.PanedWindow(root, orient=HORIZONTAL)
paned_h.pack(fill=BOTH, expand=True, padx=5, pady=5)

# Panel izquierdo con título
left_frame = ttk.Frame(paned_h)
ttk.Label(left_frame, text="Archivo 1", 
          bootstyle="inverse-primary", 
          font=("Arial", 12, "bold")).pack(pady=5)
text1 = ScrolledText(left_frame, wrap=WORD, autohide=True)
text1.pack(fill=BOTH, expand=True)

# Panel derecho con título
right_frame = ttk.Frame(paned_h)
ttk.Label(right_frame, text="Archivo 2", 
          bootstyle="inverse-success", 
          font=("Arial", 12, "bold")).pack(pady=5)
text2 = ScrolledText(right_frame, wrap=WORD, autohide=True)
text2.pack(fill=BOTH, expand=True)

# Añadir paneles
paned_h.add(left_frame, weight=1)
paned_h.add(right_frame, weight=1)

root.mainloop()
```

## PanedWindow Anidado

Puedes crear layouts complejos anidando PanedWindows:

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename="cosmo")
root.geometry("900x600")

# PanedWindow principal (vertical)
main_paned = ttk.PanedWindow(root, orient=VERTICAL)
main_paned.pack(fill=BOTH, expand=True, padx=5, pady=5)

# Panel superior (horizontal)
top_paned = ttk.PanedWindow(main_paned, orient=HORIZONTAL)

frame1 = ttk.Frame(top_paned, relief=RIDGE, borderwidth=2)
ttk.Label(frame1, text="Panel Superior Izquierdo", 
          font=("Arial", 10)).pack(pady=10)

frame2 = ttk.Frame(top_paned, relief=RIDGE, borderwidth=2)
ttk.Label(frame2, text="Panel Superior Derecho", 
          font=("Arial", 10)).pack(pady=10)

top_paned.add(frame1, weight=1)
top_paned.add(frame2, weight=1)

# Panel inferior
bottom_frame = ttk.Frame(main_paned, relief=RIDGE, borderwidth=2)
ttk.Label(bottom_frame, text="Panel Inferior", 
          font=("Arial", 10)).pack(pady=10)

# Añadir al PanedWindow principal
main_paned.add(top_paned, weight=2)
main_paned.add(bottom_frame, weight=1)

root.mainloop()
```

## Opciones y Configuración

### Opciones Principales

```python
paned = ttk.PanedWindow(
    root,
    orient=HORIZONTAL,        # Orientación: HORIZONTAL o VERTICAL
    bootstyle="secondary"     # Estilo de ttkbootstrap
)
```

### Configuración de Paneles

Al añadir paneles, puedes usar estas opciones:

```python
paned.add(frame,
    weight=1,        # Proporción de espacio adicional
    minsize=100,     # Tamaño mínimo en píxeles
    padx=5,          # Padding horizontal
    pady=5           # Padding vertical
)
```

## Métodos Útiles

```python
# Obtener información de los paneles
num_panes = len(paned.panes())  # Número de paneles

# Configurar un panel específico
paned.paneconfig(frame1, weight=3)

# Insertar un panel en una posición específica
paned.insert(0, new_frame)  # Insertar al inicio

# Remover un panel
paned.remove(frame1)
```

## Estilos Disponibles en ttkbootstrap

Puedes aplicar diferentes estilos con el parámetro `bootstyle`:

- `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`

```python
paned = ttk.PanedWindow(root, orient=HORIZONTAL, bootstyle="info")
```

## Consejos Prácticos

1. **Usa weight apropiadamente**: Asigna weights según la importancia de cada panel
2. **Establece minsize**: Evita que los paneles se vuelvan demasiado pequeños
3. **Combina con otros widgets**: PanedWindow funciona excelente con Notebook, ScrolledText, y más
4. **Anidación moderada**: No anides demasiados niveles, puede volverse confuso para el usuario
5. **Temas consistentes**: Usa temas de ttkbootstrap para mantener una apariencia profesional

## Ejemplo Práctico: Dashboard

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename="solar")
root.title("Dashboard")
root.geometry("1000x700")

# Layout principal
main_paned = ttk.PanedWindow(root, orient=HORIZONTAL)
main_paned.pack(fill=BOTH, expand=True)

# Sidebar
sidebar = ttk.Frame(main_paned, width=200)
ttk.Label(sidebar, text="Menú", bootstyle="inverse-dark", 
          font=("Arial", 14, "bold")).pack(pady=10)
for item in ["Dashboard", "Reportes", "Configuración"]:
    ttk.Button(sidebar, text=item, bootstyle="link").pack(fill=X, padx=10, pady=5)

# Área de contenido
content_paned = ttk.PanedWindow(main_paned, orient=VERTICAL)

# Área superior
top_content = ttk.Frame(content_paned)
ttk.Label(top_content, text="Gráficos y Estadísticas", 
          font=("Arial", 12)).pack(pady=20)

# Área inferior
bottom_content = ttk.Frame(content_paned)
ttk.Label(bottom_content, text="Tabla de Datos", 
          font=("Arial", 12)).pack(pady=20)

content_paned.add(top_content, weight=2)
content_paned.add(bottom_content, weight=1)

main_paned.add(sidebar, weight=0)
main_paned.add(content_paned, weight=1)

root.mainloop()
```

## Recursos Adicionales

- [Documentación oficial de ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
- [Repositorio GitHub](https://github.com/israel-dryer/ttkbootstrap)

---

Con este tutorial, tienes las bases para crear interfaces flexibles y profesionales usando PanedWindow en ttkbootstrap. ¡Experimenta con diferentes layouts y estilos!