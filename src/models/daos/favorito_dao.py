from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class FavoritoDAO(DAO):
    """
    DAO para la gestión de la tabla `favorito` en la base de datos.

    Proporciona métodos para marcar y desmarcar documentos como favoritos.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de Favorito.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `favorito` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS favorito(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_documento INTEGER NOT NULL UNIQUE,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla favorito: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Marca un documento como favorito.

        Por defecto, espera el parámetro: (id_documento).

        Returns:
            Optional[int]: El ID del registro de favorito, o None si falla.
        """
        if sql is None:
            sql = "INSERT INTO favorito (id_documento) VALUES (?)"
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina un documento de la lista de favoritos.

        Por defecto, elimina usando `id_documento`, que es más práctico.

        Returns:
            bool: True si se eliminó la marca de favorito, False en caso contrario.
        """
        if sql is None:
            # Es más intuitivo eliminar un favorito por el ID del documento
            sql = "DELETE FROM favorito WHERE id_documento = ?"
        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta registros de favoritos.

        Por defecto, busca un favorito por `id_documento`.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos.
        """
        if sql is None:
            sql = "SELECT * FROM favorito WHERE id_documento = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Actualiza el documento asociado a un registro de favorito.
        Este método es poco común para esta tabla, pero se implementa por completitud.

        Por defecto, espera los parámetros en el orden: (id_documento, id)

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if sql is None:
            sql = "UPDATE favorito SET id_documento = ? WHERE id = ?"
        return self._ejecutar_actualizacion(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si un documento está marcado como favorito.

        Por defecto, busca por `id_documento` debido a su restricción UNIQUE.
        """
        if sql is None:
            sql = "SELECT 1 FROM favorito WHERE id_documento = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0

    def obtener_todos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los documentos marcados como favoritos.

        Returns:
            List[Dict[str, Any]]: Una lista de todos los registros de favoritos.
        """
        sql = "SELECT * FROM favorito ORDER BY creado_en DESC"
        return self._ejecutar_consulta(sql)
