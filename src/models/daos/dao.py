from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import sqlite3
from models.daos.connection_sqlite import Database


class DAO(ABC):
    """
    Clase abstracta base para los Data Access Objects (DAO).

    Define una interfaz común para las operaciones CRUD (Crear, Leer, Actualizar,
    Eliminar) en la base de datos. Las clases que hereden de DAO deben
    implementar los métodos abstractos para una tabla específica.

    Attributes:
        _db (Database): Instancia del gestor de la conexión a la base de datos.
    """

    _db = None

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO, establece la conexión a la base de datos y crea la tabla.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
                                     Si es None, se usará la ruta por defecto.
        """
        super().__init__()
        self._db = Database(ruta_db=ruta_db)

        # creamos la tabla
        self.crear_tabla()

    @abstractmethod
    def crear_tabla(self):
        """
        Método abstracto para crear la tabla específica del DAO en la base de datos.

        Las clases hijas deben implementar este método para definir el esquema
        de su tabla correspondiente.
        """
        pass

    @abstractmethod
    def insertar(self, sql: str, params: tuple = ()) -> Optional[int]:
        """
        Método abstracto para insertar un registro en la base de datos.

        Args:
            sql (str): La sentencia SQL de inserción.
            params (tuple): Los parámetros para la sentencia SQL.

        Returns:
            Optional[int]: El ID del último registro insertado, o None si falla.
        """
        pass

    @abstractmethod
    def eliminar(self, sql: str, params: tuple = ()) -> bool:
        """
        Método abstracto para eliminar un registro de la base de datos.

        Args:
            sql (str): La sentencia SQL de eliminación.
            params (tuple): Los parámetros para la sentencia SQL.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        pass

    @abstractmethod
    def instanciar(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Método abstracto para consultar y obtener registros de la base de datos.

        Args:
            sql (str): La sentencia SQL de consulta.
            params (tuple): Los parámetros para la sentencia SQL.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios, donde cada diccionario
                                  representa un registro.
        """
        pass

    @abstractmethod
    def existe(self, sql: str, params: tuple = ()) -> bool:
        """
        Método abstracto para verificar si existen datos que cumplen una condición.

        Args:
            sql (str): La sentencia SQL de consulta (generalmente un SELECT COUNT).
            params (tuple): Los parámetros para la sentencia SQL.

        Returns:
            bool: True si la consulta devuelve algún resultado, False en caso contrario.
        """
        pass

    def _conectar(self):
        """
        Obtiene el objeto de conexión a la base de datos.

        Returns:
            sqlite3.Connection: El objeto de conexión.
        """
        return self._db.obtener_conexion()

    def _cursor(self):
        """
        Obtiene un cursor para ejecutar consultas en la base de datos.

        Returns:
            sqlite3.Cursor: Un objeto cursor.
        """
        return self._db.obtener_cursor()

    def _ejecutar_insertar(self, sql: str, params: tuple = ()) -> Optional[int]:
        """
        Ejecuta una sentencia de inserción de forma segura y transaccional.

        Args:
            sql (str): La sentencia SQL de inserción.
            params (tuple): Los parámetros para la sentencia SQL.

        Returns:
            Optional[int]: El ID del último registro insertado, o None si ocurre un error.
        """
        con = self._conectar()
        cursor = con.cursor()
        try:
            cursor.execute(sql, params)
            con.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as ex:
            print(f"Error al tratar de ejecutar la insercion: {ex}")
            con.rollback()
            return None

    def _ejecutar_consulta(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SELECT y retorna los resultados como una lista de diccionarios.

        Args:
            sql (str): La sentencia SQL de consulta.
            params (tuple): Los parámetros para la sentencia SQL.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios que representan las filas.
                                  Retorna una lista vacía si no hay resultados o si ocurre un error.
        """
        try:
            cursor = self._cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as ex:
            print(f"Error al ejecutar consulta: {ex}")
            return []

    def _ejecutar_actualizacion(self, sql: str, params: tuple = ()) -> bool:
        """
        Ejecuta una sentencia de actualización o eliminación de forma segura.

        Args:
            sql (str): La sentencia SQL (UPDATE, DELETE).
            params (tuple): Los parámetros para la sentencia SQL.

        Returns:
            bool: True si al menos una fila fue afectada, False en caso contrario.
        """
        con = self._conectar()
        cursor = con.cursor()
        try:
            cursor.execute(sql, params)
            con.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(f"Error al ejecutar actualización/eliminación: {ex}")
            con.rollback()
            return False
