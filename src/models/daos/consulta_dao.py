from models.daos.dao import DAO
from typing import List, Dict, Any


class ConsultaDAO(DAO):
    def __init__(self, ruta_db=None):
        """
        Inicializa una nueva instancia de ConsultaDAO.

        Args:
            ruta_db (str, optional): La ruta a la base de datos. Defaults to None.
        """
        super().__init__(ruta_db)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Colecciones
    # └────────────────────────────────────────────────────────────┘

    def get_colecciones(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las colecciones de la base de datos.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una colección.
        """
        params = ()
        sql = "SELECT * FROM coleccion ORDER BY nombre"
        return self._ejecutar_consulta(sql=sql, params=params)

    def find_colecciones(self, nombre: str) -> List[Dict[str, Any]]:
        """
        Busca colecciones por nombre.

        Args:
            nombre (str): El nombre de la colección a buscar.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una colección que coincide con el nombre.
        """
        like_buscar = f"%{nombre}%"
        params = (like_buscar,)
        sql = f"SELECT * FROM coleccion WHERE nombre LIKE ? ORDER BY nombre"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Grupos
    # └────────────────────────────────────────────────────────────┘

    def get_grupos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los grupos de la base de datos.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa un grupo.
        """
        params = ()
        sql = "SELECT * FROM grupo"
        return self._ejecutar_consulta(sql=sql, params=params)

    def find_grupos(self, nombre: str) -> List[Dict[str, Any]]:
        """
        Busca grupos por nombre.

        Args:
            nombre (str): El nombre del grupo a buscar.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa un grupo que coincide con el nombre.
        """
        like_buscar = f"%{nombre}%"
        params = (like_buscar,)
        sql = f"SELECT * FROM grupo WHERE nombre LIKE ? ORDER BY nombre"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Etiquetas
    # └────────────────────────────────────────────────────────────┘

    def get_etiquetas(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las etiquetas de la base de datos.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una etiqueta.
        """
        params = ()
        sql = "SELECT * FROM etiqueta"
        return self._ejecutar_consulta(sql=sql, params=params)

    def find_etiquetas(self, nombre: str) -> List[Dict[str, Any]]:
        """
        Busca etiquetas por nombre.

        Args:
            nombre (str): El nombre de la etiqueta a buscar.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una etiqueta que coincide con el nombre.
        """
        like_buscar = f"%{nombre}%"
        params = (like_buscar,)
        sql = f"SELECT * FROM etiqueta WHERE nombre LIKE ? ORDER BY nombre"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Palabras Clave
    # └────────────────────────────────────────────────────────────┘

    def get_palabras_clave(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las palabras clave de la base de datos.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una palabra clave.
        """
        params = ()
        sql = "SELECT * FROM palabra_clave"
        return self._ejecutar_consulta(sql=sql, params=params)

    def find_palabra_clave(self, nombre: str) -> List[Dict[str, Any]]:
        """
        Busca palabras clave por su nombre.

        Args:
            nombre (str): El nombre de la palabra clave a buscar.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una palabra clave que coincide con el nombre.
        """
        like_buscar = f"%{nombre}%"
        params = (like_buscar,)
        sql = f"SELECT * FROM palabra_clave WHERE palabra LIKE ? ORDER BY palabra"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Categorias
    # └────────────────────────────────────────────────────────────┘

    def get_categorias(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las categorías de la base de datos.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una categoría.
        """
        params = ()
        sql = "SELECT * FROM categoria"
        return self._ejecutar_consulta(sql=sql, params=params)

    def find_categoria(self, nombre: str) -> List[Dict[str, Any]]:
        """
        Busca categorías por nombre.

        Args:
            nombre (str): El nombre de la categoría a buscar.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa una categoría que coincide con el nombre.
        """
        like_buscar = f"%{nombre}%"
        params = (like_buscar,)
        sql = f"SELECT * FROM categoria WHERE nombre LIKE ? ORDER BY nombre"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Documentos
    # └────────────────────────────────────────────────────────────┘

    def get_documentos_por_coleccion(self, id_coleccion: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a una colección específica.

        Args:
            id_coleccion (int): El ID de la colección.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        sql = """
            SELECT d.*
            FROM documento d
            JOIN documento_coleccion dc ON d.id = dc.id_documento
            WHERE dc.id_coleccion = ?
            ORDER BY d.nombre
        """
        params = (id_coleccion,)
        return self._ejecutar_consulta(sql=sql, params=params)

    def get_documentos_por_grupo(self, id_grupo: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a un grupo específico.

        Args:
            id_grupo (int): El ID del grupo.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        sql = """
            SELECT d.*
            FROM documento d
            JOIN documento_grupo dg ON d.id = dg.id_documento
            WHERE dg.id_grupo = ?
            ORDER BY d.nombre
        """
        params = (id_grupo,)
        return self._ejecutar_consulta(sql=sql, params=params)

    def get_documentos_por_categoria(self, id_categoria: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a una categoría específica.

        Args:
            id_categoria (int): El ID de la categoría.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        sql = """
            SELECT d.*
            FROM documento d
            JOIN documento_categoria dc ON d.id = dc.id_documento
            WHERE dc.id_categoria = ?
            ORDER BY d.nombre
        """
        params = (id_categoria,)
        return self._ejecutar_consulta(sql=sql, params=params)

    def get_documentos_por_etiqueta(self, id_etiqueta: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a una etiqueta específica.

        Args:
            id_etiqueta (int): El ID de la etiqueta.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        sql = """
            SELECT d.*
            FROM documento d
            JOIN documento_etiqueta de ON d.id = de.id_documento
            WHERE de.id_etiqueta = ?
            ORDER BY d.nombre
        """
        params = (id_etiqueta,)
        return self._ejecutar_consulta(sql=sql, params=params)

    def get_documentos_por_palabra_clave(self, id_palabra_clave: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a una palabra clave específica.

        Args:
            id_palabra_clave (int): El ID de la palabra clave.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        sql = """
            SELECT d.*
            FROM documento d
            JOIN documento_palabra_clave dpc ON d.id = dpc.id_documento
            WHERE dpc.id_palabra_clave = ?
            ORDER BY d.nombre
        """
        params = (id_palabra_clave,)
        return self._ejecutar_consulta(sql=sql, params=params)

    def buscar_documentos(self, campo: str, buscar: str) -> List[Dict[str, any]]:
        """
        Busca documentos en la vista 'vistas_asociaciones_documentos' basándose en un campo y un término de búsqueda.

        Args:
            campo (str): El campo en el que se realizará la búsqueda (ej. 'nombre', 'autor', etc.).
            buscar (str): El término a buscar dentro del campo especificado.

        Returns:
            Una lista de diccionarios, donde cada diccionario representa un documento que coincide con los criterios de búsqueda.
        """
        like_buscar = f"%{buscar}%"
        params = (like_buscar,)
        sql = f"SELECT * FROM vista_asociaciones_documentos WHERE {campo} LIKE ? ORDER BY nombre"
        return self._ejecutar_consulta(sql=sql, params=params)

    def buscar_documentos_por_nombre(self, campo: str, buscar: str) -> List[Dict[str, any]]:
        """
        Busca documentos de forma segura, principalmente por nombre.

        Args:
            campo (str): El campo de búsqueda ('Todo' o 'Nombre').
            buscar (str): El término a buscar.

        Returns:
            Una lista de diccionarios con los documentos encontrados.
        """
        campos_permitidos = ["nombre"]
        like_buscar = f"%{buscar}%"

        if campo.lower() == "todo":
            sql = """
                SELECT * FROM vista_asociaciones_documentos
                WHERE nombre LIKE ?
                ORDER BY nombre
            """
            params = (like_buscar,)
        elif campo.lower() in campos_permitidos:
            sql = f"SELECT * FROM vista_asociaciones_documentos WHERE {campo.lower()} LIKE ? ORDER BY nombre"
            params = (like_buscar,)
        else:
            return []

        return self._ejecutar_consulta(sql=sql, params=params)

    def existe_asociaciones(self, id_documento: int) -> List[Dict[str, any]]:
        """
        Comprueba si un documento tiene asociaciones consultando la vista 'vista_documento_asociaciones'.

        Args:
            id_documento (int): El ID del documento a comprobar.

        Returns:
            Una lista de diccionarios con las asociaciones del documento. La lista estará vacía si no existen asociaciones.
        """
        sql = "SELECT * FROM vista_documento_asociaciones WHERE id_documento=?"
        params = (id_documento,)
        return self._ejecutar_consulta(sql=sql, params=params)

    def get_documentos_favoritos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los documentos marcados como favoritos.

        Returns:
            Una lista de diccionarios que representan los documentos favoritos.
        """
        sql = """
            SELECT v.* FROM vista_asociaciones_documentos v
            JOIN favorito f ON v.id = f.id_documento
            ORDER BY v.nombre
        """
        params = ()
        return self._ejecutar_consulta(sql=sql, params=params)

    def get_todos_documentos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los documentos de la vista 'vista_asociaciones_documentos'.

        Returns:
            Una lista de diccionarios que representan todos los documentos.
        """
        sql = """
            SELECT
                v.*,
                b.titulo,
                COALESCE(b.numero_paginas, mp.numero_paginas_meta) AS numero_paginas
            FROM vista_asociaciones_documentos v
            LEFT JOIN bibliografia b ON v.id = b.id_documento
            LEFT JOIN (
                SELECT
                    m.id_documento,
                    MAX(
                        CASE
                            WHEN (
                                lower(replace(replace(m.clave, ' ', ''), '_', ''))
                                LIKE '%pagecount%'
                                OR lower(replace(replace(m.clave, ' ', ''), '_', ''))
                                   IN ('pdf:pages', 'pages')
                            )
                                 AND trim(m.valor) <> ''
                                 AND trim(m.valor) NOT GLOB '*[^0-9]*'
                            THEN CAST(trim(m.valor) AS INTEGER)
                        END
                    ) AS numero_paginas_meta
                FROM metadato m
                GROUP BY m.id_documento
            ) mp ON v.id = mp.id_documento
            ORDER BY v.nombre
        """
        return self._ejecutar_consulta(sql=sql, params=())

    def buscar_en_bibliografia(self, campo: str, termino: str) -> List[Dict[str, Any]]:
        """
        Busca en la tabla de bibliografía y devuelve datos combinados con el documento.

        Args:
            campo (str): El campo de la tabla bibliografia en el que buscar (ej. 'titulo', 'autores').
            termino (str): El término a buscar.

        Returns:
            Una lista de diccionarios con los resultados.
        """
        campos_permitidos = ["titulo", "autores", "editorial", "isbn"]
        if campo not in campos_permitidos:
            return []

        like_termino = f"%{termino}%"
        sql = f"""
            SELECT
                b.*,
                d.nombre as nombre_doc,
                d.extension as extension_doc
            FROM bibliografia b
            JOIN documento d ON b.id_documento = d.id
            WHERE b.{campo} LIKE ?
            ORDER BY b.titulo
        """
        return self._ejecutar_consulta(sql=sql, params=(like_termino,))

    def buscar_en_contenido(self, termino: str) -> List[Dict[str, Any]]:
        """
        Busca un término en los títulos de capítulos y secciones.

        Args:
            termino (str): El término a buscar.

        Returns:
            Una lista de diccionarios con los resultados, incluyendo el tipo
            ('Capítulo' o 'Sección'), el título, la página, y datos del documento.
        """
        like_termino = f"%{termino}%"
        sql = """
            SELECT
                'Capítulo' as tipo,
                c.id as id_item,
                c.titulo as titulo_item,
                c.pagina_inicio as pagina,
                d.id as id_documento,
                d.nombre as nombre_documento,
                d.extension as extension_doc
            FROM capitulo c
            JOIN documento d ON c.id_documento = d.id
            WHERE c.titulo LIKE ?

            UNION ALL

            SELECT 'Sección', s.id, s.titulo, s.numero_pagina, d.id, d.nombre, d.extension
            FROM seccion s
            JOIN capitulo c ON s.id_capitulo = c.id
            JOIN documento d ON c.id_documento = d.id
            WHERE s.titulo LIKE ?
        """
        return self._ejecutar_consulta(sql=sql, params=(like_termino, like_termino))

    def buscar_en_estante(
        self, campo: str, termino: str, limit: int, offset: int
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos de forma dinámica en diferentes tablas (documento,
        bibliografia, coleccion, grupo) según el campo especificado.

        Args:
            campo (str): El campo por el cual buscar.
            termino (str): El término de búsqueda.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios que representan
                                  los documentos encontrados.
        """
        like_termino = f"%{termino}%"
        params = (like_termino,)
        paginas_select = "COALESCE(b.numero_paginas, mp.numero_paginas_meta) AS numero_paginas"
        join_paginas_metadato = """
            LEFT JOIN (
                SELECT
                    m.id_documento,
                    MAX(
                        CASE
                            WHEN (
                                lower(replace(replace(m.clave, ' ', ''), '_', ''))
                                LIKE '%pagecount%'
                                OR lower(replace(replace(m.clave, ' ', ''), '_', ''))
                                   IN ('pdf:pages', 'pages')
                            )
                                 AND trim(m.valor) <> ''
                                 AND trim(m.valor) NOT GLOB '*[^0-9]*'
                            THEN CAST(trim(m.valor) AS INTEGER)
                        END
                    ) AS numero_paginas_meta
                FROM metadato m
                GROUP BY m.id_documento
            ) mp ON v.id = mp.id_documento
        """

        # Mapeo de campos a sus respectivas tablas y columnas
        mapa_busqueda = {
            "nombre": ("documento", "v.nombre"),
            "titulo": ("bibliografia", "b.titulo"),
            "autores": ("bibliografia", "b.autores"),
            "editorial": ("bibliografia", "b.editorial"),
            "isbn": ("bibliografia", "b.isbn"),
            "coleccion": ("coleccion", "c.nombre"),
            "grupo": ("grupo", "g.nombre"),
        }

        campo_lower = campo.lower()

        if campo_lower == "todo":
            # Búsqueda en múltiples campos
            sql = f"""
                SELECT DISTINCT v.*, b.titulo, {paginas_select}
                FROM vista_asociaciones_documentos v
                LEFT JOIN bibliografia b ON v.id = b.id_documento
                {join_paginas_metadato}
                LEFT JOIN documento_coleccion dc ON v.id = dc.id_documento
                LEFT JOIN coleccion c ON dc.id_coleccion = c.id
                LEFT JOIN documento_grupo dg ON v.id = dg.id_documento
                LEFT JOIN grupo g ON dg.id_grupo = g.id
                WHERE v.nombre LIKE ? OR b.titulo LIKE ? OR b.autores LIKE ?
                   OR c.nombre LIKE ? OR g.nombre LIKE ?"""
            params = (
                like_termino,
                like_termino,
                like_termino,
                like_termino,
                like_termino,
            )
        elif campo_lower in mapa_busqueda:
            tabla, columna = mapa_busqueda[campo_lower]
            if tabla == "documento":
                sql = f"""
                    SELECT v.*, b.titulo, {paginas_select}
                    FROM vista_asociaciones_documentos v
                    LEFT JOIN bibliografia b ON v.id = b.id_documento
                    {join_paginas_metadato}
                    WHERE {columna} LIKE ?"""
            elif tabla == "bibliografia":
                sql = f"""
                    SELECT DISTINCT v.*, b.titulo, {paginas_select}
                    FROM vista_asociaciones_documentos v
                    JOIN bibliografia b ON v.id = b.id_documento
                    {join_paginas_metadato}
                    WHERE {columna} LIKE ?"""
            elif tabla == "coleccion":
                sql = f"""
                    SELECT DISTINCT v.*, b.titulo, {paginas_select}
                    FROM vista_asociaciones_documentos v
                    LEFT JOIN bibliografia b ON v.id = b.id_documento
                    {join_paginas_metadato}
                    JOIN documento_coleccion dc ON v.id = dc.id_documento
                    JOIN coleccion c ON dc.id_coleccion = c.id WHERE {columna} LIKE ?"""
            elif tabla == "grupo":
                sql = f"""
                    SELECT DISTINCT v.*, b.titulo, {paginas_select}
                    FROM vista_asociaciones_documentos v
                    LEFT JOIN bibliografia b ON v.id = b.id_documento
                    {join_paginas_metadato}
                    JOIN documento_grupo dg ON v.id = dg.id_documento
                    JOIN grupo g ON dg.id_grupo = g.id WHERE {columna} LIKE ?"""
        else:
            # Campo no válido, no devolver nada
            return []

        # Añadir paginación y orden
        sql += " ORDER BY v.nombre LIMIT ? OFFSET ?"
        params = (*params, limit, offset)

        return self._ejecutar_consulta(sql=sql, params=params)

    def count_buscar_en_estante(self, campo: str, termino: str) -> int:
        """
        Cuenta los documentos que coinciden con una búsqueda dinámica en el estante.
        """
        like_termino = f"%{termino}%"
        params = (like_termino,)

        mapa_busqueda = {
            "nombre": ("documento", "v.nombre"),
            "titulo": ("bibliografia", "b.titulo"),
            "autores": ("bibliografia", "b.autores"),
            "editorial": ("bibliografia", "b.editorial"),
            "isbn": ("bibliografia", "b.isbn"),
            "coleccion": ("coleccion", "c.nombre"),
            "grupo": ("grupo", "g.nombre"),
        }

        campo_lower = campo.lower()

        if campo_lower == "todo":
            sql = """
                SELECT COUNT(DISTINCT v.id) as total FROM vista_asociaciones_documentos v
                LEFT JOIN bibliografia b ON v.id = b.id_documento
                LEFT JOIN documento_coleccion dc ON v.id = dc.id_documento
                LEFT JOIN coleccion c ON dc.id_coleccion = c.id
                LEFT JOIN documento_grupo dg ON v.id = dg.id_documento
                LEFT JOIN grupo g ON dg.id_grupo = g.id
                WHERE v.nombre LIKE ? OR b.titulo LIKE ? OR b.autores LIKE ?
                   OR c.nombre LIKE ? OR g.nombre LIKE ?
            """
            params = (like_termino, like_termino, like_termino, like_termino, like_termino)
        elif campo_lower in mapa_busqueda:
            tabla, columna = mapa_busqueda[campo_lower]
            if tabla == "documento":
                sql = f"SELECT COUNT(v.id) as total FROM vista_asociaciones_documentos v WHERE {columna} LIKE ?"
            elif tabla == "bibliografia":
                sql = f"SELECT COUNT(DISTINCT v.id) as total FROM vista_asociaciones_documentos v JOIN bibliografia b ON v.id = b.id_documento WHERE {columna} LIKE ?"
            elif tabla == "coleccion":
                sql = f"SELECT COUNT(DISTINCT v.id) as total FROM vista_asociaciones_documentos v JOIN documento_coleccion dc ON v.id = dc.id_documento JOIN coleccion c ON dc.id_coleccion = c.id WHERE {columna} LIKE ?"
            elif tabla == "grupo":
                sql = f"SELECT COUNT(DISTINCT v.id) as total FROM vista_asociaciones_documentos v JOIN documento_grupo dg ON v.id = dg.id_documento JOIN grupo g ON dg.id_grupo = g.id WHERE {columna} LIKE ?"
        else:
            return 0

        result = self._ejecutar_consulta(sql=sql, params=params)
        return result[0]['total'] if result and result[0]['total'] is not None else 0

    # ┌────────────────────────────────────────────────────────────┐
    # │ Capitulos
    # └────────────────────────────────────────────────────────────┘

    def capitulos_documento(self, id_documento: int) -> List[Dict[str, Any]]:
        """
        Obtiene todos los capitulos que tiene le documento

        :param self: Descripción
        :param id_documento: id del documento
        :type id_documento: int
        :return: Descripción
        :rtype: List[Dict[str, Any]]
        """
        sql = "SELECT * FROM capitulo WHERE id_documento=?"
        params = (id_documento,)
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Seccion
    # └────────────────────────────────────────────────────────────┘

    def secciones_capitulos(self, id_capitulo: int) -> List[Dict[str, Any]]:
        """
        Listamos todas las secciones que tiene el capitulo

        :param self: Descripción
        :param id_capitulo: Descripción
        :type id_capitulo: int
        :return: Descripción
        :rtype: List[Dict[str, Any]]
        """
        sql = "SELECT * FROM seccion WHERE id_capitulo=?"
        params = (id_capitulo,)
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos de la clase abstracta
    # └────────────────────────────────────────────────────────────┘

    def crear_tabla(self):
        """
        Crea las tablas necesarias. Heredado de la clase DAO.
        """
        return super().crear_tabla()

    def eliminar(self, sql, params=...):
        """
        Ejecuta una sentencia de eliminación. Heredado de la clase DAO.
        """
        return super().eliminar(sql, params)

    def existe(self, sql, params=...):
        """
        Comprueba si un registro existe. Heredado de la clase DAO.
        """
        return super().existe(sql, params)

    def insertar(self, sql, params=...):
        """
        Inserta un nuevo registro. Heredado de la clase DAO.
        """
        return super().insertar(sql, params)

    def instanciar(self, sql, params=...):
        """
        Obtiene una instancia de un registro. Heredado de la clase DAO.
        """
        return super().instanciar(sql, params)

    def get_metadatos_agrupados_con_conteo(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las combinaciones de clave-valor de metadatos y cuenta
        cuántos documentos están asociados a cada una.

        Returns:
            Una lista de diccionarios, cada uno con 'clave', 'valor' y 'total'.
            Ej: [{'clave': 'PDF:Title', 'valor': 'Some Book', 'total': 5}, ...]
        """
        sql = """
            SELECT clave, valor, COUNT(id_documento) as total
            FROM metadato
            GROUP BY clave, valor
            ORDER BY clave, valor
        """
        return self._ejecutar_consulta(sql=sql, params=())

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metadatos
    # └────────────────────────────────────────────────────────────┘

    def get_claves_metadatos_con_conteo(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las claves de metadatos únicas y cuenta cuántos
        documentos están asociados a cada una.

        Returns:
            Una lista de diccionarios, cada uno con 'clave' y 'total'.
            Ej: [{'clave': 'PDF:Title', 'total': 15}, ...]
        """
        sql = """
            SELECT clave, COUNT(id_documento) as total
            FROM metadato
            GROUP BY clave
            ORDER BY clave
        """
        return self._ejecutar_consulta(sql=sql, params=())

    def get_documentos_por_clave_metadato(self, clave: str, valor: str) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos que contienen una combinación de clave y valor
        de metadato específica.

        Args:
            clave (str): La clave de metadato a buscar (ej. 'PDF:Title').
            valor (str): El valor de metadato a buscar.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        sql = """
            SELECT v.* FROM vista_asociaciones_documentos v
            JOIN metadato m ON v.id = m.id_documento
            WHERE m.clave = ? AND m.valor = ? ORDER BY v.nombre
        """
        return self._ejecutar_consulta(sql=sql, params=(clave, valor))

    # ┌────────────────────────────────────────────────────────────┐
    # │ Estadísticas Generales
    # └────────────────────────────────────────────────────────────┘

    def get_total_documentos(self) -> int:
        """
        Obtiene el número total de documentos en la base de datos.

        Returns:
            int: El número total de documentos.
        """
        sql = "SELECT COUNT(id) FROM documento"
        result = self._ejecutar_consulta(sql=sql, params=())
        return result[0]['COUNT(id)'] if result and result[0]['COUNT(id)'] is not None else 0

    def get_total_tamano_documentos(self) -> int:
        """
        Obtiene el tamaño total combinado de todos los documentos en la base de datos (en bytes).
        """
        sql = "SELECT SUM(tamano) FROM documento"
        result = self._ejecutar_consulta(sql=sql, params=())
        # Asegurarse de que el resultado no sea None si no hay documentos
        return result[0]['SUM(tamano)'] if result and result[0]['SUM(tamano)'] is not None else 0
