from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class DocumentoCategoriaDAO(DAO):
    """
    DAO para la gestión de la tabla pivote `documento_categoria`.

    Esta clase maneja la relación muchos a muchos entre documentos y categorías.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de DocumentoCategoria.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `documento_categoria` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS documento_categoria(
            id_documento INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id_documento, id_categoria),
            FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id) ON DELETE CASCADE
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla documento_categoria: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Asocia un documento a una categoría.

        Por defecto, espera los parámetros en el orden: (id_documento, id_categoria).
        Retorna el rowid de la inserción, pero no es un ID único significativo.
        La existencia de un valor de retorno indica éxito.

        Returns:
            Optional[int]: El rowid de la fila insertada, o None si falla.
        """
        if sql is None:
            sql = "INSERT INTO documento_categoria (id_documento, id_categoria) VALUES (?, ?)"
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina la asociación entre un documento y una categoría.

        Por defecto, elimina por la clave compuesta (id_documento, id_categoria).

        Returns:
            bool: True si se eliminó la asociación, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM documento_categoria WHERE id_documento = ? AND id_categoria = ?"
        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta asociaciones.

        Por defecto, busca todas las categorías de un documento.
        Espera el parámetro: (id_documento).

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con las asociaciones.
        """
        if sql is None:
            sql = "SELECT * FROM documento_categoria WHERE id_documento = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Este método no es aplicable a una tabla pivote sin campos adicionales.
        Lanza una excepción si se intenta usar.
        """
        raise NotImplementedError(
            "La actualización no es aplicable a la tabla documento_categoria."
        )

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si una asociación entre documento y categoría existe.

        Por defecto, busca por la clave compuesta (id_documento, id_categoria).
        """
        if sql is None:
            sql = "SELECT 1 FROM documento_categoria WHERE id_documento = ? AND id_categoria = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
