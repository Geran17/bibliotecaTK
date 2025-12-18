from models.entities.coleccion import Coleccion
from models.entities.grupo import Grupo
from models.entities.etiqueta import Etiqueta
from models.entities.palabra_clave import PalabraClave
from models.entities.categoria import Categoria
from models.entities.documento import Documento
from models.daos.consulta_dao import ConsultaDAO
from models.entities.capitulo import Capitulo
from models.entities.seccion import Seccion
from typing import List, Dict, Any


class Consulta:
    def __init__(self, ruta_db: str = None):
        self.ruta_db = ruta_db

    # ┌────────────────────────────────────────────────────────────┐
    # │ Colecciones
    # └────────────────────────────────────────────────────────────┘

    def get_colecciones(self) -> List[Coleccion]:
        """
        Obtiene una lista de todas las entidades Coleccion.

        Utiliza ConsultaDAO para obtener los datos y los mapea a objetos Coleccion.

        Returns:
            Una lista de objetos Coleccion.
        """
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_colecciones = dao.get_colecciones()
        if lista_colecciones:
            for dato in lista_colecciones:
                coleccion = Coleccion(
                    id=dato['id'],
                    nombre=dato['nombre'],
                    descripcion=dato['descripcion'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato.get('actualizado_en'),
                )
                lista.append(coleccion)
        return lista

    def find_colecciones(self, nombre: str) -> List[Coleccion]:
        """
        Busca colecciones por nombre.

        Args:
            nombre (str): El nombre de la colección a buscar.

        Returns:
            Una lista de objetos Coleccion que coinciden con el nombre.
        """
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_colecciones = dao.find_colecciones(nombre=nombre)
        if lista_colecciones:
            for dato in lista_colecciones:
                coleccion = Coleccion(
                    id=dato["id"],
                    nombre=dato["nombre"],
                    descripcion=dato["descripcion"],
                )
                lista.append(coleccion)
        return lista

    # ┌────────────────────────────────────────────────────────────┐
    # │ Grupos
    # └────────────────────────────────────────────────────────────┘

    def get_grupos(self) -> List[Grupo]:
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_grupos = dao.get_grupos()
        if lista_grupos:
            for dato in lista_grupos:
                grupo = Grupo(
                    id=int(dato['id']),
                    nombre=dato['nombre'],
                    descripcion=dato['descripcion'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato['actualizado_en'],
                )
                lista.append(grupo)
        return lista

    def find_grupos(self, nombre: str) -> List[Grupo]:
        """
        Busca grupos por nombre.

        Args:
            nombre (str): El nombre del grupo a buscar.

        Returns:
            Una lista de objetos Grupo que coinciden con el nombre.
        """
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_grupos = dao.find_grupos(nombre=nombre)
        if lista_grupos:
            for dato in lista_grupos:
                grupo = Grupo(
                    id=int(dato["id"]),
                    nombre=dato["nombre"],
                    descripcion=dato["descripcion"],
                )
                lista.append(grupo)
        return lista

    # ┌────────────────────────────────────────────────────────────┐
    # │ Etiquetas
    # └────────────────────────────────────────────────────────────┘

    def get_etiquetas(self) -> List[Etiqueta]:
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_etiquetas = dao.get_etiquetas()
        if lista_etiquetas:
            for dato in lista_etiquetas:
                etiqueta = Etiqueta(
                    id=int(dato['id']),
                    nombre=dato['nombre'],
                    descripcion=dato['descripcion'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato['actualizado_en'],
                )
                lista.append(etiqueta)
        return lista

    def find_etiquetas(self, nombre: str) -> List[Etiqueta]:
        """
        Busca etiquetas por nombre.

        Args:
            nombre (str): El nombre de la etiqueta a buscar.

        Returns:
            Una lista de objetos Etiqueta que coinciden con el nombre.
        """
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_etiquetas = dao.find_etiquetas(nombre=nombre)
        if lista_etiquetas:
            for dato in lista_etiquetas:
                etiqueta = Etiqueta(
                    id=int(dato["id"]),
                    nombre=dato["nombre"],
                    descripcion=dato["descripcion"],
                )
                lista.append(etiqueta)
        return lista

    # ┌────────────────────────────────────────────────────────────┐
    # │ Palabras Clave
    # └────────────────────────────────────────────────────────────┘

    def get_palabras_clave(self) -> List[PalabraClave]:
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_palabras_clave = dao.get_palabras_clave()
        if lista_palabras_clave:
            for dato in lista_palabras_clave:
                palabra_clave = PalabraClave(
                    id=int(dato['id']),
                    palabra=dato['palabra'],
                    descripcion=dato['descripcion'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato['actualizado_en'],
                )
                lista.append(palabra_clave)
        return lista

    def find_palabras_clave(self, nombre: str) -> List[PalabraClave]:
        """
        Busca palabras clave por su texto.

        Args:
            nombre (str): El texto de la palabra clave a buscar.

        Returns:
            Una lista de objetos PalabraClave que coinciden con el texto.
        """
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_palabras_clave = dao.find_palabra_clave(nombre=nombre)
        if lista_palabras_clave:
            for dato in lista_palabras_clave:
                palabra_clave = PalabraClave(
                    id=int(dato["id"]),
                    palabra=dato["palabra"],
                    descripcion=dato["descripcion"],
                )
                lista.append(palabra_clave)
        return lista

    # ┌────────────────────────────────────────────────────────────┐
    # │ Categorias
    # └────────────────────────────────────────────────────────────┘

    def get_categorias(self) -> List[Categoria]:
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_categorias = dao.get_categorias()
        if lista_categorias:
            for dato in lista_categorias:
                categoria = Categoria(
                    id=int(dato['id']),
                    nombre=dato['nombre'],
                    id_padre=dato['id_padre'],
                    descripcion=dato['descripcion'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato['actualizado_en'],
                )
                lista.append(categoria)
        return lista

    def find_categorias(self, nombre: str) -> List[Categoria]:
        """
        Busca categorías por nombre.

        Args:
            nombre (str): El nombre de la categoría a buscar.

        Returns:
            Una lista de objetos Categoria que coinciden con el nombre.
        """
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_categorias = dao.find_categoria(nombre=nombre)
        if lista_categorias:
            for dato in lista_categorias:
                categoria = Categoria(
                    id=int(dato["id"]),
                    nombre=dato["nombre"],
                    id_padre=dato["id_padre"],
                    descripcion=dato["descripcion"],
                )
                lista.append(categoria)
        return lista

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
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # Asumimos que ConsultaDAO tendrá un método correspondiente.
        return dao.get_documentos_por_coleccion(id_coleccion=id_coleccion)

    def get_documentos_por_grupo(self, id_grupo: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a un grupo específico.

        Args:
            id_grupo (int): El ID del grupo.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # Asumimos que ConsultaDAO tendrá un método correspondiente.
        return dao.get_documentos_por_grupo(id_grupo=id_grupo)

    def get_documentos_por_categoria(self, id_categoria: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a una categoría específica.

        Args:
            id_categoria (int): El ID de la categoría.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # Asumimos que ConsultaDAO tendrá un método correspondiente.
        return dao.get_documentos_por_categoria(id_categoria=id_categoria)

    def get_documentos_por_etiqueta(self, id_etiqueta: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a una etiqueta específica.

        Args:
            id_etiqueta (int): El ID de la etiqueta.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # Asumimos que ConsultaDAO tendrá un método correspondiente.
        return dao.get_documentos_por_etiqueta(id_etiqueta=id_etiqueta)

    def get_documentos_por_palabra_clave(self, id_palabra_clave: int) -> List[Dict[str, Any]]:
        """
        Obtiene los documentos asociados a una palabra clave específica.

        Args:
            id_palabra_clave (int): El ID de la palabra clave.

        Returns:
            Una lista de diccionarios que representan los documentos.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # Asumimos que ConsultaDAO tendrá un método correspondiente.
        return dao.get_documentos_por_palabra_clave(id_palabra_clave=id_palabra_clave)

    def buscar_documentos(self, campo: str, buscar: str) -> List[Dict[str, Any]]:
        """
        Busca documentos basándose en un campo y un término de búsqueda.

        Args:
            campo (str): El campo en el que se realizará la búsqueda.
            buscar (str): El término a buscar.

        Returns:
            Una lista de diccionarios que representan los documentos encontrados.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.buscar_documentos(campo=campo, buscar=buscar)

    def buscar_documentos_por_nombre(self, campo: str, buscar: str) -> List[Dict[str, any]]:
        """
        Busca documentos de forma segura, principalmente por nombre.

        Args:
            campo (str): El campo de búsqueda ('Todo' o 'Nombre').
            buscar (str): El término a buscar.

        Returns:
            Una lista de diccionarios con los documentos encontrados.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # Asumimos que ConsultaDAO tendrá un método correspondiente.
        return dao.buscar_documentos_por_nombre(campo=campo, buscar=buscar)

    def existe_asociaciones(self, id_documento: int) -> List[Dict[str, Any]]:
        """
        Comprueba si un documento tiene asociaciones existentes.

        Args:
            id_documento (int): El ID del documento a comprobar.

        Returns:
            Una lista de diccionarios con las asociaciones del documento.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.existe_asociaciones(id_documento=id_documento)

    def get_documentos_favoritos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los documentos marcados como favoritos.

        Returns:
            Una lista de diccionarios que representan los documentos favoritos.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.get_documentos_favoritos()

    def get_todos_documentos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los documentos de la biblioteca.

        Returns:
            Una lista de diccionarios que representan todos los documentos.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.get_todos_documentos()

    def buscar_en_bibliografia(self, campo: str, termino: str) -> List[Dict[str, Any]]:
        """
        Busca en los datos bibliográficos de los documentos.

        Args:
            campo (str): Campo por el cual buscar (titulo, autores, etc.).
            termino (str): Término de búsqueda.

        Returns:
            Lista de diccionarios con los resultados.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # El DAO se encarga de la lógica de la consulta SQL
        return dao.buscar_en_bibliografia(campo=campo, termino=termino)

    def buscar_en_contenido(self, termino: str) -> List[Dict[str, Any]]:
        """
        Busca en los títulos de capítulos y secciones de los documentos.

        Args:
            termino (str): Término de búsqueda.

        Returns:
            Lista de diccionarios con los resultados.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        # El DAO se encarga de la lógica de la consulta SQL
        return dao.buscar_en_contenido(termino=termino)

    def buscar_en_estante(self, campo: str, termino: str) -> List[Dict[str, Any]]:
        """
        Busca documentos de forma dinámica para la vista de "Estante".

        Args:
            campo (str): Campo por el cual buscar (Nombre, Título, Colección, etc.).
            termino (str): Término de búsqueda.

        Returns:
            Lista de diccionarios con los documentos encontrados.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.buscar_en_estante(campo=campo, termino=termino)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Capitulos
    # └────────────────────────────────────────────────────────────┘

    def capitulos_documento(self, id_documento: int) -> List[Capitulo]:
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_capitulos = dao.capitulos_documento(id_documento=id_documento)
        if lista_capitulos:
            for dato in lista_capitulos:
                capitulo = Capitulo(
                    id_documento=dato['id_documento'],
                    numero_capitulo=dato['numero_capitulo'],
                    titulo=dato['titulo'],
                    id=dato['id'],
                    pagina_inicio=dato['pagina_inicio'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato['actualizado_en'],
                )
                lista.append(capitulo)
        return lista

    # ┌────────────────────────────────────────────────────────────┐
    # │ Secciones
    # └────────────────────────────────────────────────────────────┘

    def secciones_capitulo(self, id_capitulo: int) -> List[Seccion]:
        """Lista la secciones que tiene un capitulo"""
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_secciones = dao.secciones_capitulos(id_capitulo=id_capitulo)
        if lista_secciones:
            for dato in lista_secciones:
                seccion = Seccion(
                    id_capitulo=dato['id_capitulo'],
                    titulo=dato['titulo'],
                    id=dato['id'],
                    nivel=dato['nivel'],
                    id_padre=dato['id_padre'],
                    numero_pagina=dato['numero_pagina'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato['actualizado_en'],
                )
                lista.append(seccion)
        return lista

    def get_metadatos_agrupados_con_conteo(self) -> List[Dict[str, Any]]:
        """
        Obtiene un listado de todas las combinaciones clave-valor de metadatos
        junto con el número de documentos asociados a cada una.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con 'clave', 'valor' y 'total'.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.get_metadatos_agrupados_con_conteo()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metadatos
    # └────────────────────────────────────────────────────────────┘

    def get_claves_metadatos_con_conteo(self) -> List[Dict[str, Any]]:
        """
        Obtiene un listado de todas las claves de metadatos únicas junto
        con el número de documentos asociados a cada una.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con 'clave' y 'total'.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.get_claves_metadatos_con_conteo()

    def get_documentos_por_clave_metadato(self, clave: str, valor: str) -> List[Dict[str, Any]]:
        """
        Busca y devuelve todos los documentos que contienen una combinación
        de clave y valor de metadato específica.

        Args:
            clave (str): La clave de metadato a buscar (ej. 'PDF:Title').
            valor (str): El valor de metadato a buscar.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios que representan
                                  los documentos encontrados.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.get_documentos_por_clave_metadato(clave=clave, valor=valor)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Estadísticas Generales
    # └────────────────────────────────────────────────────────────┘

    def get_total_documentos(self) -> int:
        """
        Obtiene el número total de documentos en la biblioteca.

        Returns:
            int: El número total de documentos.
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.get_total_documentos()

    def get_total_tamano_documentos(self) -> int:
        """
        Obtiene el tamaño total combinado de todos los documentos en la biblioteca (en bytes).
        """
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        return dao.get_total_tamano_documentos()
