import traceback
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
        appTK.ejecutar()
    except Exception as e:
        # Imprime el error y el traceback completo para una mejor depuración
        traceback.print_exc()


if __name__ == "__main__":
    main()
