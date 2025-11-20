from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class DatoBibliograficoDAO(DAO):
    """
    DAO para la gestión de la tabla `dato_bibliografico` en la base de datos.

    Proporciona métodos para realizar operaciones CRUD sobre los datos
    bibliográficos de los documentos.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de DatoBibliografico.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `dato_bibliografico` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS dato_bibliografico(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autores TEXT NULL,
            ano_publicacion INTEGER CHECK (ano_publicacion >= 0 AND ano_publicacion <= strftime('%Y', 'now')),
            editorial TEXT NULL,
            lugar_publicacion TEXT NULL,
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
            print(f"Error al crear la tabla dato_bibliografico: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Inserta un nuevo registro bibliográfico en la base de datos.

        Por defecto, espera los parámetros en el orden:
        (titulo, autores, ano_publicacion, editorial, lugar_publicacion, id_documento)

        Returns:
            Optional[int]: El ID del registro insertado, o None si falla.
        """
        if sql is None:
            sql = """
            INSERT INTO dato_bibliografico (titulo, autores, ano_publicacion, editorial, lugar_publicacion, id_documento)
            VALUES (?, ?, ?, ?, ?, ?)
            """
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina un registro bibliográfico de la base de datos.

        Por defecto, elimina por `id`.

        Returns:
            bool: True si se eliminó al menos una fila, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM dato_bibliografico WHERE id = ?"

        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql, params)
            con.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(f"Error al eliminar dato_bibliografico: {ex}")
            con.rollback()
            return False

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta y retorna registros bibliográficos.

        Por defecto, busca por `id`.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos.
        """
        if sql is None:
            sql = "SELECT * FROM dato_bibliografico WHERE id = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Actualiza todos los campos de un registro bibliográfico.

        Por defecto, espera los parámetros en el orden:
        (titulo, autores, ano_publicacion, editorial, lugar_publicacion, id_documento, id)

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if sql is None:
            sql = """
            UPDATE dato_bibliografico
            SET titulo = ?, autores = ?, ano_publicacion = ?, editorial = ?,
                lugar_publicacion = ?, id_documento = ?
            WHERE id = ?
            """
        return self._ejecutar_actualizacion(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si un registro bibliográfico existe.

        Por defecto, busca por `id_documento` debido a su restricción UNIQUE.
        """
        if sql is None:
            sql = "SELECT 1 FROM dato_bibliografico WHERE id_documento = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
