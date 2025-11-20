from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
from models.dtos.coleccion_dto import ColeccionDTO
import sqlite3


class ColeccionDAO(DAO):
    """
    DAO para la gestión de la tabla `coleccion`.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `coleccion` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS coleccion(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            cursor.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_coleccion_nombre ON coleccion(nombre)"
            )
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla coleccion: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, data: ColeccionDTO) -> Optional[int]:
        """
        Inserta una nueva colección en la base de datos.

        Args:
            data (ColeccionDTO): El objeto con los datos de la colección.

        Returns:
            Optional[int]: El ID de la colección insertada, o None si falla.
        """
        sql = "INSERT INTO coleccion (nombre, descripcion) VALUES (?, ?)"
        return self._ejecutar_insertar(sql, (data.nombre, data.descripcion))

    def eliminar(self, id_coleccion: int) -> bool:
        """
        Elimina una colección por su ID.

        Args:
            id_coleccion (int): El ID de la colección a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        sql = "DELETE FROM coleccion WHERE id = ?"
        return self._ejecutar_actualizacion(sql, (id_coleccion,))

    def instanciar(self, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Obtiene registros de la tabla coleccion.
        """
        sql = "SELECT * FROM coleccion WHERE id = ?"
        return self._ejecutar_consulta(sql, params)

    def existe(self, nombre: str) -> bool:
        """
        Verifica si una colección con un nombre específico ya existe.

        Args:
            nombre (str): El nombre de la colección a verificar.

        Returns:
            bool: True si la colección existe, False en caso contrario.
        """
        sql = "SELECT 1 FROM coleccion WHERE nombre = ?"
        return len(self._ejecutar_consulta(sql, (nombre,))) > 0

    def actualizar(self, id_coleccion: int, nombre: str, descripcion: Optional[str]) -> bool:
        sql = "UPDATE coleccion SET nombre = ?, descripcion = ? WHERE id = ?"
        return self._ejecutar_actualizacion(sql, (nombre, descripcion, id_coleccion))
