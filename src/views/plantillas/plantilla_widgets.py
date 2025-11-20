from ttkbootstrap import Frame, Text, Scrollbar
from ttkbootstrap.constants import *


def crear_area_descripcion(parent_frame: Frame):
    # 1. Crear un Frame para contener el Text y el Scrollbar (para un diseño limpio)
    frame_contenedor = Frame(parent_frame, padding=5)
    frame_contenedor.pack(fill=BOTH, expand=True)

    # 2. Crear la barra de desplazamiento
    scrollbar = Scrollbar(frame_contenedor, bootstyle="round")

    # 3. Crear el widget Text
    area_texto = Text(
        frame_contenedor,
        wrap=WORD,  # Hace que el texto salte de línea en la última palabra visible
        height=10,  # Define la altura inicial en número de líneas
        yscrollcommand=scrollbar.set,  # Vincula el Text a la Scrollbar
        bootstyle="light",  # Estilo de fondo
    )

    # Insertar un texto de ejemplo
    area_texto.insert(
        END,
        "Escriba aquí la descripción detallada de la colección. Este widget Text soporta múltiples líneas, lo que es ideal para textos largos y párrafos completos. Si el texto supera la altura del widget (10 líneas en este caso), la barra de desplazamiento se activará automáticamente.",
    )

    # 4. Empaquetar el Scrollbar (a la derecha y relleno vertical)
    scrollbar.pack(side=RIGHT, fill=Y)

    # 5. Empaquetar el Text (a la izquierda, relleno completo, y expandir)
    area_texto.pack(side=LEFT, fill=BOTH, expand=True)

    # 6. Vincular el Scrollbar al Text
    scrollbar.config(command=area_texto.yview)

    return area_texto
