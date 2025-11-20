from ttkbootstrap import Frame, Button
from ttkbootstrap.constants import *


class FrameInferior(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # instanciamos los widgets
        self.crear_widgets()

    def crear_widgets(self):
        button_inferior = Button(self, text="Button Inferior")
        button_inferior.pack(side=LEFT, fill=X)
