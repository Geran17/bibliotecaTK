from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class DocumentoDAO(DAO):
    """
    DAO para la gestión de la tabla `documento` en la base de datos.

    Proporciona métodos para realizar operaciones CRUD (Crear, Leer, Actualizar,
    Eliminar) sobre los registros de documentos.
    """

    def __init__(self, ruta_db=None):
        """
        Inicializa el DAO de Documento.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `documento` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS documento(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            extension TEXT NOT NULL CHECK (length(extension) <= 10),
            hash TEXT NOT NULL UNIQUE, 
            tamano INTEGER CHECK (tamano >= 0),
            esta_activo INTEGER DEFAULT 1,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla documento: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Inserta un nuevo documento en la base de datos.

        Si no se proporciona una consulta SQL, se utiliza una inserción por defecto
        que espera los siguientes parámetros en orden:
        (nombre, extension, hash, tamano, esta_activo)

        Args:
            sql (str, optional): Consulta SQL de inserción. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Defaults to ().

        Returns:
            Optional[int]: El ID del documento insertado, o None si falla.
        """
        if sql is None:
            sql = """
            INSERT INTO documento (nombre, extension, hash, tamano, esta_activo)
            VALUES (?, ?, ?, ?, ?)
            """
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina un documento de la base de datos.

        Por defecto, si no se proporciona SQL, elimina un documento por su `id`.

        Returns:
            bool: True si se eliminó al menos una fila, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM documento WHERE id = ?"

        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta y retorna documentos.

        Por defecto, si no se proporciona SQL, busca un documento por su `id`.

        Args:
            sql (str, optional): Consulta SQL de selección. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Defaults to ().

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos del/los documento(s).
        """
        if sql is None:
            sql = "SELECT * FROM documento WHERE id = ?"
        return self._ejecutar_consulta(sql, params)

    def instanciar_por_hash(self, hash: str) -> List[Dict[str, Any]]:
        """
        Consulta y retorna un documento específico basado en su hash.

        Args:
            hash (str): El hash del documento a buscar.

        Returns:
            List[Dict[str, Any]]: Una lista que contiene el diccionario del documento
                                  encontrado, o una lista vacía si no se encuentra.
        """
        sql = "SELECT * FROM documento WHERE hash = ?"
        return self._ejecutar_consulta(sql, (hash,))

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Actualiza todos los campos de un registro de documento existente.

        Si no se proporciona SQL, se usa una consulta por defecto que actualiza
        `nombre`, `extension`, `hash`, `tamano` y `esta_activo` usando el `id`.

        Args:
            sql (str, optional): Consulta SQL de actualización. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Para la consulta
                                      por defecto, el orden es (nombre, extension,
                                      hash, tamano, esta_activo, id).

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if sql is None:
            sql = """
            UPDATE documento
            SET nombre = ?, extension = ?, hash = ?, tamano = ?, esta_activo = ?
            WHERE id = ?
            """
        return self._ejecutar_actualizacion(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si un documento existe en la base de datos.

        Por defecto, si no se proporciona SQL, busca por `hash`.
        """
        if sql is None:
            sql = "SELECT 1 FROM documento WHERE hash = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
