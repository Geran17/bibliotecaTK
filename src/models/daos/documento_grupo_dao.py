from typing import Dict, Any, List, Optional
from models.daos.dao import DAO
import sqlite3


class DocumentoGrupoDAO(DAO):
    """
    DAO para la gestión de la tabla pivote `documento_grupo`.

    Esta clase maneja la relación muchos a muchos entre documentos y grupos.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de DocumentoGrupo.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self):
        """
        Crea la tabla `documento_grupo` en la base de datos si no existe.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS documento_grupo(
            id_documento INTEGER NOT NULL,
            id_grupo INTEGER NOT NULL,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id_documento, id_grupo),
            FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
            FOREIGN KEY (id_grupo) REFERENCES grupo(id) ON DELETE CASCADE
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as ex:
            print(f"Error al crear la tabla documento_grupo: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """
        Asocia un documento a un grupo.

        Por defecto, espera los parámetros en el orden: (id_documento, id_grupo).

        Returns:
            Optional[int]: El rowid de la fila insertada, o None si falla.
        """
        if sql is None:
            sql = "INSERT INTO documento_grupo (id_documento, id_grupo) VALUES (?, ?)"
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Elimina la asociación entre un documento y un grupo.

        Por defecto, elimina por la clave compuesta (id_documento, id_grupo).

        Returns:
            bool: True si se eliminó la asociación, False en caso contrario.
        """
        if sql is None:
            sql = "DELETE FROM documento_grupo WHERE id_documento = ? AND id_grupo = ?"
        return self._ejecutar_actualizacion(sql, params)

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Consulta asociaciones.

        Por defecto, busca todos los grupos de un documento.
        Espera el parámetro: (id_documento).

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con las asociaciones.
        """
        if sql is None:
            sql = "SELECT * FROM documento_grupo WHERE id_documento = ?"
        return self._ejecutar_consulta(sql, params)

    def actualizar_todo(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Este método no es aplicable a una tabla pivote sin campos adicionales.
        Lanza una excepción si se intenta usar.
        """
        raise NotImplementedError("La actualización no es aplicable a la tabla documento_grupo.")

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """
        Verifica si una asociación entre documento y grupo existe.

        Por defecto, busca por la clave compuesta (id_documento, id_grupo).
        """
        if sql is None:
            sql = "SELECT 1 FROM documento_grupo WHERE id_documento = ? AND id_grupo = ?"

        resultados = self._ejecutar_consulta(sql, params)
        return len(resultados) > 0
