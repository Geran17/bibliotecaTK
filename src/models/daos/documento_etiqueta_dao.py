from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class DocumentoEtiquetaDAO(DAO):
    """
    DAO para la gestión de la tabla pivote `documento_etiqueta`.

    Esta clase maneja la relación muchos a muchos entre documentos y etiquetas.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de DocumentoEtiqueta.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `documento_etiqueta` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS documento_etiqueta(
            id_documento INTEGER NOT NULL,
            id_etiqueta INTEGER NOT NULL,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id_documento, id_etiqueta),
            FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
            FOREIGN KEY (id_etiqueta) REFERENCES etiqueta(id) ON DELETE CASCADE
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla documento_etiqueta: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Asocia un documento a una etiqueta.

        Por defecto, espera los parámetros en el orden: (id_documento, id_etiqueta).

        Returns:
            Optional[int]: El rowid de la fila insertada, o None si falla.
        """
        if sql is None:
            sql = "INSERT INTO documento_etiqueta (id_documento, id_etiqueta) VALUES (?, ?)"
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina la asociación entre un documento y una etiqueta.

        Por defecto, elimina por la clave compuesta (id_documento, id_etiqueta).

        Returns:
            bool: True si se eliminó la asociación, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM documento_etiqueta WHERE id_documento = ? AND id_etiqueta = ?"
        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta asociaciones.

        Por defecto, busca todas las etiquetas de un documento.
        Espera el parámetro: (id_documento).

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con las asociaciones.
        """
        if sql is None:
            sql = "SELECT * FROM documento_etiqueta WHERE id_documento = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Este método no es aplicable a una tabla pivote sin campos adicionales.
        Lanza una excepción si se intenta usar.
        """
        raise NotImplementedError("La actualización no es aplicable a la tabla documento_etiqueta.")

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si una asociación entre documento y etiqueta existe.

        Por defecto, busca por la clave compuesta (id_documento, id_etiqueta).
        """
        if sql is None:
            sql = "SELECT 1 FROM documento_etiqueta WHERE id_documento = ? AND id_etiqueta = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
