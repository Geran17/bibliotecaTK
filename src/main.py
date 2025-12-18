from os.path import join
from models.daos.database_dao import DataBaseDAO
from utilities.configuracion import inicializar_directorios, RUTA_DATA
from views.appTK import AppTK


def main():
    try:
        # creamos la estructura de la base datos
        data_base = DataBaseDAO()
        data_base.crear_base_de_datos()

        # inicializamos los directorios principales
        inicializar_directorios()
        # Abrimos la aplicacion principal
        appTK = AppTK()
        appTK.ejeuctar()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
