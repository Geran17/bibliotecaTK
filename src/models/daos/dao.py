from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import sqlite3
from contextlib import contextmanager
import threading
from utilities.configuracion import RUTA_DATA
from os.path import join


class DAO(ABC):
    """
    Clase abstracta base para los Data Access Objects (DAO).
    Versión thread-safe que crea conexiones independientes por operación.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO y guarda la ruta de la base de datos.
        """
        super().__init__()
        if ruta_db is None:
            ruta_db = join(RUTA_DATA, "bibliotecaTK.sqlite3")

        self._ruta_db = ruta_db
        self._lock = threading.Lock()

        # Crear la tabla
        self.crear_tabla()

    @contextmanager
    def _get_connection(self):
        """
        Context manager para obtener una conexión thread-safe.
        Crea una nueva conexión que se cierra automáticamente.
        """
        con = sqlite3.connect(self._ruta_db)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")

        try:
            yield con
            con.commit()
        except Exception as e:
            con.rollback()
            raise e
        finally:
            con.close()

    @abstractmethod
    def crear_tabla(self):
        """
        Método abstracto para crear la tabla específica del DAO.
        """
        pass

    @abstractmethod
    def insertar(self, sql: str, params: tuple = ()) -> Optional[int]:
        """
        Método abstracto para insertar un registro.
        """
        pass

    @abstractmethod
    def eliminar(self, sql: str, params: tuple = ()) -> bool:
        """
        Método abstracto para eliminar un registro.
        """
        pass

    @abstractmethod
    def instanciar(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Método abstracto para consultar registros.
        """
        pass

    @abstractmethod
    def existe(self, sql: str, params: tuple = ()) -> bool:
        """
        Método abstracto para verificar existencia.
        """
        pass

    def _ejecutar_insertar(self, sql: str, params: tuple = ()) -> Optional[int]:
        """
        Ejecuta una sentencia de inserción thread-safe.
        """
        try:
            with self._get_connection() as con:
                cursor = con.cursor()
                cursor.execute(sql, params)
                return cursor.lastrowid
        except sqlite3.Error as ex:
            print(f"Error al ejecutar inserción: {ex}")
            return None

    def _ejecutar_consulta(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SELECT thread-safe.
        """
        try:
            with self._get_connection() as con:
                cursor = con.cursor()
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as ex:
            print(f"Error al ejecutar consulta: {ex}")
            return []

    def _ejecutar_actualizacion(self, sql: str, params: tuple = ()) -> bool:
        """
        Ejecuta una actualización o eliminación thread-safe.
        """
        try:
            with self._get_connection() as con:
                cursor = con.cursor()
                cursor.execute(sql, params)
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(f"Error al ejecutar actualización: {ex}")
            return False

    # Métodos de compatibilidad para código existente
    def _conectar(self):
        """
        DEPRECATED: Usar _get_connection() context manager en su lugar.
        Retorna una conexión temporal (debe cerrarse manualmente).
        """
        con = sqlite3.connect(self._ruta_db)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _cursor(self):
        """
        DEPRECATED: Usar _get_connection() context manager en su lugar.
        Crea una nueva conexión y retorna un cursor.
        ADVERTENCIA: Esta conexión no se cierra automáticamente.
        """
        con = self._conectar()
        return con.cursor()
