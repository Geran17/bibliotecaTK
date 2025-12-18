from typing import Optional, List, Dict, Any
from models.daos.dao import DAO
from models.dtos.bibliografia_dto import BibliografiaDTO
import sqlite3


class BibliografiaDAO(DAO):
    """
    DAO para la gestión de los datos bibliográficos.

    Gestiona las operaciones CRUD para la tabla consolidada `bibliografia`
    de forma unificada, utilizando
    el DTO `BibliografiaDTO`.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el DAO de Bibliografia.

        Args:
            ruta_db (Optional[str]): Ruta opcional al archivo de la base de datos.
        """
        super().__init__(ruta_db)

    def crear_tabla(self) -> None:
        """
        Crea la tabla `bibliografia` si no existe, consolidando los campos
        de las tablas anteriores.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS bibliografia(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autores TEXT NULL,
            ano_publicacion INTEGER CHECK (ano_publicacion >= 0),
            editorial TEXT NULL,
            lugar_publicacion TEXT NULL,
            numero_edicion TEXT NULL, -- Puede ser '2da', 'revisada', etc.
            idioma TEXT NULL,
            volumen_tomo TEXT NULL,
            numero_paginas INTEGER CHECK (numero_paginas > 0),
            isbn TEXT NULL UNIQUE,
            id_documento INTEGER NOT NULL UNIQUE,
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
            print(f"Error al crear las tablas de bibliografía: {ex}")
            self._conectar().rollback()
            raise

    def insertar(self, params: tuple = ()) -> Optional[int]:
        """
        Inserta un nuevo registro bibliográfico.

        Args:
            params (tuple): Tupla con los datos en el siguiente orden:
                            (titulo, autores, ano_publicacion, editorial,
                             lugar_publicacion, numero_edicion, idioma,
                             volumen_tomo, numero_paginas, isbn, id_documento)

        Returns:
            Optional[int]: El ID del registro insertado, o None si falla.
        """
        sql = """
            INSERT INTO bibliografia (
                titulo, autores, ano_publicacion, editorial, lugar_publicacion,
                numero_edicion, idioma, volumen_tomo, numero_paginas, isbn, id_documento
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, id_documento: int) -> bool:
        """
        Elimina los datos bibliográficos asociados a un documento.

        Gracias a `ON DELETE CASCADE` en la tabla `documento`, esta eliminación
        se produce automáticamente si se borra el documento padre.

        Args:
            id_documento (int): El ID del documento cuyos datos se eliminarán.

        Returns:
            bool: True si se eliminó al menos una fila, False en caso contrario.
        """
        sql = "DELETE FROM bibliografia WHERE id_documento = ?"
        return self._ejecutar_actualizacion(sql, (id_documento,))

    def instanciar(self, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Obtiene los datos bibliográficos de un documento como una lista de diccionarios.

        Args:
            id_documento (int): El ID del documento a consultar.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios con los datos.
                                  Estará vacía si no se encuentra.
        """
        sql = "SELECT * FROM bibliografia WHERE id_documento = ?"
        resultado = self._ejecutar_consulta(sql, params=params)
        return resultado

    def existe(self, params: tuple = ()) -> bool:
        """
        Verifica si existen datos bibliográficos para un documento.

        Args:
            id_documento (int): El ID del documento a verificar.

        Returns:
            bool: True si existen datos, False en caso contrario.
        """
        sql = "SELECT 1 FROM bibliografia WHERE id_documento = ?"
        return len(self._ejecutar_consulta(sql, params=params)) > 0

    def actualizar(self, params: tuple = ()) -> bool:
        """
        Actualiza un registro bibliográfico existente.

        Args:
            params (tuple): Tupla con los datos en el siguiente orden:
                            (titulo, autores, ano_publicacion, editorial,
                             lugar_publicacion, numero_edicion, idioma,
                             volumen_tomo, numero_paginas, isbn, id_documento)

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        sql = """
            UPDATE bibliografia SET
                titulo = ?,
                autores = ?,
                ano_publicacion = ?,
                editorial = ?,
                lugar_publicacion = ?,
                numero_edicion = ?,
                idioma = ?,
                volumen_tomo = ?,
                numero_paginas = ?,
                isbn = ?
            WHERE id_documento = ?
        """
        return self._ejecutar_actualizacion(sql, params)
