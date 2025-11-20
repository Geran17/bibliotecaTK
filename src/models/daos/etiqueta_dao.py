from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class EtiquetaDAO(DAO):
    """
    DAO para la gestión de la tabla `etiqueta` en la base de datos.

    Proporciona métodos para realizar operaciones CRUD sobre las etiquetas.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de Etiqueta.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `etiqueta` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS etiqueta(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT NULL,
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
            print(f"Error al crear la tabla etiqueta: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Inserta una nueva etiqueta en la base de datos.

        Por defecto, espera los parámetros en el orden: (nombre, descripcion)

        Returns:
            Optional[int]: El ID de la etiqueta insertada, o None si falla.
        """
        if sql is None:
            sql = "INSERT INTO etiqueta (nombre, descripcion) VALUES (?, ?)"
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina una etiqueta de la base de datos.

        Por defecto, elimina por `id`.

        Returns:
            bool: True si se eliminó al menos una fila, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM etiqueta WHERE id = ?"
        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta y retorna etiquetas.

        Por defecto, busca por `id`.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos.
        """
        if sql is None:
            sql = "SELECT * FROM etiqueta WHERE id = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Actualiza todos los campos de una etiqueta.

        Por defecto, espera los parámetros en el orden: (nombre, descripcion, id)

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        if sql is None:
            sql = "UPDATE etiqueta SET nombre = ?, descripcion = ? WHERE id = ?"
        return self._ejecutar_actualizacion(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si una etiqueta existe.

        Por defecto, busca por `nombre` debido a su restricción UNIQUE.
        """
        if sql is None:
            sql = "SELECT 1 FROM etiqueta WHERE nombre = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
