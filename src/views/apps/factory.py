from typing import Final
from views.apps.base_app import AppVisual

UI_TKINTER: Final[str] = "tkinter"


def crear_app(ui: str) -> AppVisual:
    ui_normalizada = (ui or "").strip().lower()

    if ui_normalizada == UI_TKINTER:
        from views.tk.app import AppTkinter

        return AppTkinter()

    raise ValueError(
        f"Framework visual no soportado: '{ui}'. "
        f"Opciones disponibles: '{UI_TKINTER}'."
    )
