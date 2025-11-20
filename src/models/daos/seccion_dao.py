from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class SeccionDAO(DAO):
    """
    DAO para la gestión de la tabla `seccion` en la base de datos.

    Proporciona métodos para realizar operaciones CRUD (Crear, Leer, Actualizar,
    Eliminar) sobre los registros de secciones de capítulos.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de Seccion.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `seccion` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS seccion(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_capitulo INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            nivel TEXT NULL,
            id_padre INTEGER NULL,
            numero_pagina INTEGER,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_capitulo) REFERENCES capitulo (id) ON DELETE CASCADE,
            FOREIGN KEY (id_padre) REFERENCES seccion (id) ON DELETE CASCADE
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla seccion: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Inserta una nueva sección en la base de datos.

        Si no se proporciona una consulta SQL, se utiliza una inserción por defecto
        que espera los siguientes parámetros en orden:
        (id_capitulo, titulo, nivel, id_padre, numero_pagina)

        Args:
            sql (str, optional): Consulta SQL de inserción. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Defaults to ().

        Returns:
            Optional[int]: El ID de la sección insertada, o None si falla.
        """
        if sql is None:
            sql = """
            INSERT INTO seccion (id_capitulo, titulo, nivel, id_padre, numero_pagina)
            VALUES (?, ?, ?, ?, ?)
            """
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina una sección de la base de datos.

        Por defecto, si no se proporciona SQL, elimina una sección por su `id`.

        Returns:
            bool: True si se eliminó al menos una fila, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM seccion WHERE id = ?"

        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta y retorna secciones.

        Por defecto, si no se proporciona SQL, busca una sección por su `id`.

        Args:
            sql (str, optional): Consulta SQL de selección. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Defaults to ().

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos de la(s) sección(es).
        """
        if sql is None:
            sql = "SELECT * FROM seccion WHERE id = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Actualiza todos los campos de un registro de sección existente.

        Si no se proporciona SQL, se usa una consulta por defecto que actualiza
        `id_capitulo`, `titulo`, `nivel`, `id_padre` y `numero_pagina` usando el `id`.

        Args:
            sql (str, optional): Consulta SQL de actualización. Defaults to None.
            params (tuple, optional): Parámetros para la consulta. Para la consulta
                                      por defecto, el orden es (id_capitulo, titulo,
                                      nivel, id_padre, numero_pagina, id).

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if sql is None:
            sql = """
            UPDATE seccion
            SET id_capitulo = ?, titulo = ?, nivel = ?, id_padre = ?, numero_pagina = ?
            WHERE id = ?
            """
        return self._ejecutar_actualizacion(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si una sección existe en la base de datos.

        Por defecto, si no se proporciona SQL, busca por `id_capitulo` y `titulo`.
        """
        if sql is None:
            sql = "SELECT 1 FROM seccion WHERE id_capitulo = ? AND titulo = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
