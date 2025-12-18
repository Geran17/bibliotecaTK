import sqlite3
from models.daos.connection_sqlite import Database
from models.dtos.database_dto import DataBaseDTO


class DataBaseDAO:
    """
    DAO para la gestión y creación de la estructura completa de la base de datos.

    Utiliza DataBaseDTO para obtener las sentencias SQL y construir el esquema.
    """

    def __init__(self, ruta_db: str = None):
        """
        Inicializa el DAO de la base de datos.

        Args:
            ruta_db (str, optional): Ruta al archivo de la base de datos.
                                     Si es None, se usa la ruta por defecto.
        """
        self._db = Database(ruta_db=ruta_db)
        self._dto = DataBaseDTO()

    def crear_base_de_datos(self):
        """
        Crea todas las tablas, vistas, índices y disparadores de la base de datos.

        Ejecuta las sentencias SQL en el orden correcto para asegurar que las
        dependencias (como las claves foráneas) se resuelvan correctamente.
        """
        try:
            con = self._db.obtener_conexion()
            cursor = con.cursor()

            # Lista de todas las sentencias de creación de tablas
            tablas_sql = [
                self._dto.sql_table_documento,
                self._dto.sql_table_metadato,
                self._dto.sql_table_bibliografia,
                self._dto.sql_table_capitulo,
                self._dto.sql_table_seccion,
                self._dto.sql_table_favorito,
                self._dto.sql_table_categoria,
                self._dto.sql_table_grupo,
                self._dto.sql_table_coleccion,
                self._dto.sql_table_palabra_clave,
                self._dto.sql_table_etiqueta,
                self._dto.sql_table_documento_palabra_clave,
                self._dto.sql_table_documento_categoria,
                self._dto.sql_table_documento_coleccion,
                self._dto.sql_table_documento_grupo,
                self._dto.sql_table_documento_etiqueta,
            ]

            # 1. Crear todas las tablas
            for sql in tablas_sql:
                cursor.execute(sql)

            # 2. Crear la vista
            views_sql = [
                self._dto.sql_view_asociaciones_documentos,
                self._dto.sql_view_documento_asociaciones,
            ]
            for sql in views_sql:
                cursor.execute(sql)

            # 3. Crear todos los disparadores
            for sql in self._dto.sql_triggers:
                cursor.execute(sql)

            # 4. Crear todos los índices
            for sql in self._dto.sql_indexes:
                cursor.execute(sql)

            con.commit()

        except sqlite3.Error as e:
            print(f"Error al crear la base de datos: {e}")
            self._db.obtener_conexion().rollback()
            raise
