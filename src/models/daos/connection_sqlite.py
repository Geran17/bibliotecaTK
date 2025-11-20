import sqlite3
from sqlite3 import Connection, Cursor
from utilities.configuracion import RUTA_DATA
from os.path import join


class Database:
    """Clase Singleton"""

    _instancia = None
    _conexion = None

    def __new__(cls, ruta_db: str = None):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self, ruta_db: str = None):
        # Solo inicializar si no hay conexión
        if self._conexion is None:
            try:
                if ruta_db is None:
                    ruta_db = join(RUTA_DATA, "bibliotecaTK.sqlite3")

                self._conexion = sqlite3.connect(ruta_db)
                self._conexion.row_factory = sqlite3.Row
                self._conexion.execute("PRAGMA foreign_keys = ON")
            except sqlite3.Error as err:
                print(f"Error al conectar: {err}")
                self._conexion = None
                raise

    def obtener_conexion(self) -> Connection:
        """Retorna la conexion de la base de datos"""
        if self._conexion is None:
            raise RuntimeError("No hay conexion a la base de datos establecida")
        return self._conexion

    def obtener_cursor(self) -> Cursor:
        """Retorna un cursor para ejectar consultas"""
        return self.obtener_conexion().cursor()

    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self._conexion is not None:
            self._conexion.close()
            self._conexion = None

    @classmethod
    def resetear(cls):
        """
        Resetea el Singleton (útil principalmente para tests).
        Cierra la conexión si existe y reinicia las variables de clase.
        """
        if cls._conexion is not None:
            cls._conexion.close()
        cls._instancia = None
        cls._conexion = None
