from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class CapituloDAO(DAO):
    """
    DAO para la gestión de la tabla `capitulo` en la base de datos.

    Proporciona métodos para realizar operaciones CRUD (Crear, Leer, Actualizar,
    Eliminar) sobre los registros de capítulos de documentos.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de Capitulo.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `capitulo` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS capitulo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_documento INTEGER NOT NULL,
            numero_capitulo INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            pagina_inicio INTEGER,
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
            print(f"Error al crear la tabla capitulo: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Inserta un nuevo capítulo en la base de datos.

        Si no se proporciona una consulta SQL, se utiliza una inserción por defecto
        que espera los siguientes parámetros en orden:
        (id_documento, numero_capitulo, titulo, pagina_inicio)

        Args:
            sql (str, optional): Consulta SQL de inserción. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Defaults to ().

        Returns:
            Optional[int]: El ID del capítulo insertado, o None si falla.
        """
        if sql is None:
            sql = """
            INSERT INTO capitulo (id_documento, numero_capitulo, titulo, pagina_inicio)
            VALUES (?, ?, ?, ?)
            """
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina un capítulo de la base de datos.

        Por defecto, si no se proporciona SQL, elimina un capítulo por su `id`.

        Returns:
            bool: True si se eliminó al menos una fila, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM capitulo WHERE id = ?"

        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta y retorna capítulos.

        Por defecto, si no se proporciona SQL, busca un capítulo por su `id`.

        Args:
            sql (str, optional): Consulta SQL de selección. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Defaults to ().

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos del/los capítulo(s).
        """
        if sql is None:
            sql = "SELECT * FROM capitulo WHERE id = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Actualiza todos los campos de un registro de capítulo existente.

        Si no se proporciona SQL, se usa una consulta por defecto que actualiza
        `id_documento`, `numero_capitulo`, `titulo` y `pagina_inicio` usando el `id`.

        Args:
            sql (str, optional): Consulta SQL de actualización. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Para la consulta
                                      por defecto, el orden es (id_documento,
                                      numero_capitulo, titulo, pagina_inicio, id).

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if sql is None:
            sql = """
            UPDATE capitulo
            SET id_documento = ?, numero_capitulo = ?, titulo = ?, pagina_inicio = ?
            WHERE id = ?
            """
        return self._ejecutar_actualizacion(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si un capítulo existe en la base de datos.

        Por defecto, si no se proporciona SQL, busca por `id_documento` y `numero_capitulo`.
        """
        if sql is None:
            sql = "SELECT 1 FROM capitulo WHERE id_documento = ? AND numero_capitulo = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
