import fitz  # PyMuPDF
from PIL import Image, ImageTk
import io
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def pdf_primera_pagina_a_png(pdf_path, output_path, dpi=72, thumbnail_size=(150, 200)):
    """
    Extrae la primera página de un PDF y la guarda como PNG miniatura.

    Args:
        pdf_path (str): Ruta al archivo PDF
        output_path (str): Ruta donde guardar el PNG
        dpi (int): Resolución (72 para miniaturas, 150 para calidad)
        thumbnail_size (tuple): (ancho, alto) para miniatura

    Returns:
        bool: True si fue exitoso, False en caso contrario
    """
    try:
        doc = fitz.open(pdf_path)
        pagina = doc[0]

        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = pagina.get_pixmap(matrix=mat)

        # Guardar temporalmente
        pix.save(output_path)

        # Redimensionar para miniatura
        img = Image.open(output_path)
        img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        img.save(output_path, optimize=True, quality=85)

        doc.close()
        return True

    except Exception as e:
        print(f"Error al extraer portada: {e}")
        return False


def pdf_a_photoimage(pdf_path, thumbnail_size=(150, 200)):
    """
    Convierte la primera página de un PDF directamente a PhotoImage
    para usar en ttkbootstrap sin guardar archivo.

    Args:
        pdf_path (str): Ruta al archivo PDF
        thumbnail_size (tuple): (ancho, alto) para miniatura

    Returns:
        ImageTk.PhotoImage: Imagen lista para usar en tkinter/ttkbootstrap
    """
    try:
        doc = fitz.open(pdf_path)
        pagina = doc[0]

        # Usar DPI bajo para miniaturas
        mat = fitz.Matrix(1, 1)  # DPI 72
        pix = pagina.get_pixmap(matrix=mat)

        # Convertir a PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))

        # Redimensionar manteniendo proporción
        img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)

        doc.close()

        # Convertir a PhotoImage para tkinter
        return ImageTk.PhotoImage(img)

    except Exception as e:
        print(f"Error: {e}")
        return None


# EJEMPLO DE USO CON TTKBOOTSTRAP
class VisorPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de PDFs")
        self.root.geometry("800x600")

        # Frame principal
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=BOTH, expand=YES)

        # Frame izquierdo para lista
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Treeview para listar PDFs
        ttk.Label(left_frame, text="Documentos PDF", font=("Helvetica", 12, "bold")).pack(
            pady=(0, 10)
        )

        self.tree = ttk.Treeview(left_frame, columns=("archivo",), show="tree", height=15)
        self.tree.pack(fill=BOTH, expand=YES)
        self.tree.bind("<<TreeviewSelect>>", self.mostrar_portada)

        # Frame derecho para portada
        right_frame = ttk.Frame(main_frame, bootstyle="secondary")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        ttk.Label(right_frame, text="Portada", font=("Helvetica", 12, "bold")).pack(pady=(0, 10))

        # Label para mostrar la portada
        self.portada_label = ttk.Label(right_frame, text="Selecciona un PDF")
        self.portada_label.pack(pady=20)

        # Botón para cargar PDFs
        ttk.Button(
            left_frame, text="Cargar PDF", command=self.cargar_pdf, bootstyle="success"
        ).pack(pady=10, fill=X)

        # Diccionario para guardar rutas
        self.pdfs = {}

    def cargar_pdf(self):
        from tkinter import filedialog

        archivo = filedialog.askopenfilename(
            title="Seleccionar PDF", filetypes=[("PDF files", "*.pdf")]
        )

        if archivo:
            nombre = archivo.split("/")[-1]
            item_id = self.tree.insert("", END, text=nombre)
            self.pdfs[item_id] = archivo

    def mostrar_portada(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item_id = seleccion[0]
            pdf_path = self.pdfs.get(item_id)

            if pdf_path:
                # Generar portada (300x400 para visualización)
                photo = pdf_a_photoimage(pdf_path, thumbnail_size=(300, 400))

                if photo:
                    self.portada_label.config(image=photo, text="")
                    # Importante: mantener referencia
                    self.portada_label.image = photo
                else:
                    self.portada_label.config(text="Error al cargar portada", image="")


if __name__ == "__main__":
    # Opción 1: Guardar como archivo PNG
    pdf_primera_pagina_a_png(
        "/home/geran/Contenedor/algebr - manhattan.pdf",
        "portada_mini.png",
        dpi=72,
        thumbnail_size=(150, 200),
    )

    # Opción 2: Aplicación completa con ttkbootstrap
    root = ttk.Window(themename="cosmo")  # Puedes cambiar el tema
    app = VisorPDFApp(root)
    root.mainloop()
