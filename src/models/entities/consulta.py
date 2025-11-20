from models.entities.coleccion import Coleccion
from models.entities.grupo import Grupo
from models.entities.etiqueta import Etiqueta
from models.entities.palabra_clave import PalabraClave
from models.entities.categoria import Categoria
from models.daos.consulta_dao import ConsultaDAO
from typing import List


class Consulta:
    def __init__(self, ruta_db: str = None):
        self.ruta_db = ruta_db

    # ┌────────────────────────────────────────────────────────────┐
    # │ Colecciones
    # └────────────────────────────────────────────────────────────┘

    def get_colecciones(self) -> List[Coleccion]:
        lista = []
        dao = ConsultaDAO(ruta_db=self.ruta_db)
        lista_colecciones = dao.get_colecciones()
        if lista_colecciones:
            for dato in lista_colecciones:
                coleccion = Coleccion(
                    id=int(dato['id']),
                    nombre=dato['nombre'],
                    descripcion=dato['descripcion'],
                    creado_en=dato['creado_en'],
                    actualizado_en=dato['actualizado_en'],
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
