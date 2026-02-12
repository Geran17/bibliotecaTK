from views.appTK import AppTK


class AppTkinter:
    """
    Punto de entrada del backend Tkinter.

    Mantiene compatibilidad con la implementacion actual en views.appTK
    mientras migramos frames/dialogs a views.tk.
    """

    def __init__(self):
        self._app = AppTK()

    def ejecutar(self) -> None:
        self._app.ejecutar()
