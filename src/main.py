import argparse
import os
import traceback
from models.controllers.configuracion_controller import ConfiguracionController
from models.daos.database_dao import DataBaseDAO
from utilities.configuracion import inicializar_directorios
from views.apps.factory import crear_app, UI_TKINTER


def _parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BibliotecaTK")
    parser.add_argument(
        "--ui",
        choices=["tkinter"],
        default=None,
        help="Framework visual a utilizar. Tambien puedes usar BIBLIOTECA_UI.",
    )
    return parser.parse_args()


def _resolver_ui(args: argparse.Namespace) -> str:
    # Prioridad: argumento CLI > variable de entorno > configuracion INI > fallback
    if args.ui:
        return args.ui

    entorno_variable = (os.getenv("BIBLIOTECA_UI", "") or "").strip().lower()
    if entorno_variable == UI_TKINTER:
        return entorno_variable

    entorno_guardado = ConfiguracionController().obtener_entorno_ui()
    if entorno_guardado:
        return entorno_guardado

    return UI_TKINTER


def main():
    try:
        args = _parsear_argumentos()

        # creamos la estructura de la base datos
        data_base = DataBaseDAO()
        data_base.crear_base_de_datos()

        # inicializamos los directorios principales
        inicializar_directorios()

        # Abrimos la aplicacion principal
        ui = _resolver_ui(args)
        app = crear_app(ui)
        app.ejecutar()
    except Exception as e:
        # Imprime el error y el traceback completo para una mejor depuración
        traceback.print_exc()


if __name__ == "__main__":
    main()
