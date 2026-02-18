from typing import Optional

from tkinter import Text
from ttkbootstrap import Toplevel, Frame, Label, Button, Scrollbar
from ttkbootstrap.constants import BOTH, EW, RIGHT, TOP


def ask_resizable_text(
    master,
    title: str,
    prompt: str,
    initialvalue: str = "",
    min_width: int = 520,
    min_height: int = 320,
) -> Optional[str]:
    """
    Muestra un diálogo de texto multilínea redimensionable y retorna el valor ingresado.
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
    frame.rowconfigure(1, weight=1)

    Label(frame, text=prompt).grid(row=0, column=0, sticky=EW, pady=(0, 6))

    text_frame = Frame(frame)
    text_frame.grid(row=1, column=0, sticky="nsew")
    text_frame.rowconfigure(0, weight=1)
    text_frame.columnconfigure(0, weight=1)

    txt_value = Text(text_frame, wrap="word")
    txt_value.grid(row=0, column=0, sticky="nsew")

    scrollbar = Scrollbar(text_frame, orient="vertical", command=txt_value.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    txt_value.configure(yscrollcommand=scrollbar.set)

    if initialvalue:
        txt_value.insert("1.0", initialvalue)

    frame_buttons = Frame(frame)
    frame_buttons.grid(row=2, column=0, sticky=EW, pady=(10, 0))

    def accept():
        result["value"] = txt_value.get("1.0", "end-1c")
        dialog.destroy()

    def cancel():
        result["value"] = None
        dialog.destroy()

    Button(frame_buttons, text="Cancelar", command=cancel).pack(side=RIGHT, padx=(6, 0))
    Button(frame_buttons, text="Guardar", command=accept, style="primary.TButton").pack(
        side=RIGHT
    )

    dialog.bind("<Escape>", lambda event: cancel())
    dialog.bind("<Control-Return>", lambda event: accept())
    dialog.bind("<Control-s>", lambda event: accept())

    txt_value.focus_set()

    dialog.grab_set()
    dialog.wait_window()
    return result["value"]
