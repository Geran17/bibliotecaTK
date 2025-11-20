from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class DatoBibliograficoComplementarioDAO(DAO):
    """
    DAO para la gestión de la tabla `dato_bibliografico_complementario`.

    Proporciona métodos CRUD para los datos bibliográficos complementarios.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de DatoBibliograficoComplementario.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `dato_bibliografico_complementario` si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS dato_bibliografico_complementario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_dato_bibliografico INTEGER NOT NULL UNIQUE,
            numero_edicion INTEGER NULL CHECK (numero_edicion > 0),
            idioma TEXT NULL,
            volumen_tomo TEXT NULL,
            numero_paginas INTEGER CHECK (numero_paginas > 0),
            isbn TEXT NULL UNIQUE,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_dato_bibliografico) REFERENCES dato_bibliografico (id) ON DELETE CASCADE
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla dato_bibliografico_complementario: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Inserta un nuevo registro bibliográfico complementario.

        Por defecto, espera los parámetros en el orden:
        (id_dato_bibliografico, numero_edicion, idioma, volumen_tomo, numero_paginas, isbn)

        Returns:
            Optional[int]: El ID del registro insertado, o None si falla.
        """
        if sql is None:
            sql = """
            INSERT INTO dato_bibliografico_complementario
            (id_dato_bibliografico, numero_edicion, idioma, volumen_tomo, numero_paginas, isbn)
            VALUES (?, ?, ?, ?, ?, ?)
            """
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina un registro bibliográfico complementario.

        Por defecto, elimina por `id`.

        Returns:
            bool: True si se eliminó al menos una fila, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM dato_bibliografico_complementario WHERE id = ?"

        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql, params)
            con.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(f"Error al eliminar dato_bibliografico_complementario: {ex}")
            con.rollback()
            return False

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta y retorna registros bibliográficos complementarios.

        Por defecto, busca por `id`.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos.
        """
        if sql is None:
            sql = "SELECT * FROM dato_bibliografico_complementario WHERE id = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Actualiza todos los campos de un registro bibliográfico complementario.

        Por defecto, espera los parámetros en el orden:
        (id_dato_bibliografico, numero_edicion, idioma, volumen_tomo, numero_paginas, isbn, id)

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if sql is None:
            sql = """
            UPDATE dato_bibliografico_complementario
            SET id_dato_bibliografico = ?, numero_edicion = ?, idioma = ?,
                volumen_tomo = ?, numero_paginas = ?, isbn = ?
            WHERE id = ?
            """
        return self._ejecutar_actualizacion(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si un registro bibliográfico complementario existe.

        Por defecto, busca por `id_dato_bibliografico` debido a su restricción UNIQUE.
        """
        if sql is None:
            sql = "SELECT 1 FROM dato_bibliografico_complementario WHERE id_dato_bibliografico = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
