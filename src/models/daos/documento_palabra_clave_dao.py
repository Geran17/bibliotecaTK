from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class DocumentoPalabraClaveDAO(DAO):
    """
    DAO para la gestión de la tabla pivote `documento_palabra_clave`.

    Esta clase maneja la relación muchos a muchos entre documentos y palabras clave.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de DocumentoPalabraClave.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `documento_palabra_clave` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS documento_palabra_clave(
            id_documento INTEGER NOT NULL,
            id_palabra_clave INTEGER NOT NULL,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id_documento, id_palabra_clave),
            FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
            FOREIGN KEY (id_palabra_clave) REFERENCES palabra_clave(id) ON DELETE CASCADE
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla documento_palabra_clave: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Asocia un documento a una palabra clave.

        Por defecto, espera los parámetros en el orden: (id_documento, id_palabra_clave).

        Returns:
            Optional[int]: El rowid de la fila insertada, o None si falla.
        """
        if sql is None:
            sql = (
                "INSERT INTO documento_palabra_clave (id_documento, id_palabra_clave) VALUES (?, ?)"
            )
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina la asociación entre un documento y una palabra clave.

        Por defecto, elimina por la clave compuesta (id_documento, id_palabra_clave).

        Returns:
            bool: True si se eliminó la asociación, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM documento_palabra_clave WHERE id_documento = ? AND id_palabra_clave = ?"
        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta asociaciones.

        Por defecto, busca todas las palabras clave de un documento.
        Espera el parámetro: (id_documento).

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con las asociaciones.
        """
        if sql is None:
            sql = "SELECT * FROM documento_palabra_clave WHERE id_documento = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Este método no es aplicable a una tabla pivote sin campos adicionales.
        Lanza una excepción si se intenta usar.
        """
        raise NotImplementedError(
            "La actualización no es aplicable a la tabla documento_palabra_clave."
        )

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si una asociación entre documento y palabra clave existe.

        Por defecto, busca por la clave compuesta (id_documento, id_palabra_clave).
        """
        if sql is None:
            sql = "SELECT 1 FROM documento_palabra_clave WHERE id_documento = ? AND id_palabra_clave = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
