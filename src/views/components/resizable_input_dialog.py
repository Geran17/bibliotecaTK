from typing import Optional

from ttkbootstrap import Toplevel, Frame, Label, Entry, Button, StringVar
from ttkbootstrap.constants import BOTH, EW, RIGHT, TOP


def ask_resizable_string(
    master,
    title: str,
    prompt: str,
    initialvalue: str = "",
    min_width: int = 420,
    min_height: int = 140,
) -> Optional[str]:
    """
    Muestra un diálogo de texto redimensionable y retorna el valor ingresado.
    Devuelve `None` si el usuario cancela.
    """
    result = {"value": None}

    dialog = Toplevel(master=master)
    dialog.title(title)
    dialog.transient(master)
    dialog.resizable(True, True)
    dialog.minsize(min_width, min_height)

    frame = Frame(dialog, padding=10)
    frame.pack(side=TOP, fill=BOTH, expand=True)
    frame.columnconfigure(0, weight=1)

    Label(frame, text=prompt).grid(row=0, column=0, sticky=EW, pady=(0, 6))

    var_value = StringVar(value=initialvalue)
    ent_value = Entry(frame, textvariable=var_value)
    ent_value.grid(row=1, column=0, sticky=EW)

    frame_buttons = Frame(frame)
    frame_buttons.grid(row=2, column=0, sticky=EW, pady=(10, 0))

    def accept():
        result["value"] = var_value.get()
        dialog.destroy()

    def cancel():
        result["value"] = None
        dialog.destroy()

    Button(frame_buttons, text="Cancelar", command=cancel).pack(side=RIGHT, padx=(6, 0))
    Button(frame_buttons, text="Aceptar", command=accept, style="primary.TButton").pack(side=RIGHT)

    dialog.bind("<Return>", lambda event: accept())
    dialog.bind("<Escape>", lambda event: cancel())

    ent_value.focus_set()
    ent_value.icursor("end")
    ent_value.select_range(0, "end")

    dialog.grab_set()
    dialog.wait_window()
    return result["value"]
