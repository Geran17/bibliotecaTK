from os.path import join
from models.daos.connection_sqlite import Database
from utilities.configuracion import inicializar_directorios, RUTA_DATA
from views.appTK import AppTK


def main():
    try:
        # inicializamos los directorios principales
        inicializar_directorios()
        # Abrimos la aplicacion principal
        appTK = AppTK()
        appTK.ejeuctar()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
