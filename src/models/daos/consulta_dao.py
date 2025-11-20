from models.daos.dao import DAO
from typing import List, Dict, Any


class ConsultaDAO(DAO):
    def __init__(self, ruta_db=None):
        super().__init__(ruta_db)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Colecciones
    # └────────────────────────────────────────────────────────────┘

    def get_colecciones(self) -> List[Dict[str, Any]]:
        params = ()
        sql = "SELECT * FROM coleccion"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Grupos
    # └────────────────────────────────────────────────────────────┘

    def get_grupos(self) -> List[Dict[str, Any]]:
        params = ()
        sql = "SELECT * FROM grupo"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Etiquetas
    # └────────────────────────────────────────────────────────────┘

    def get_etiquetas(self) -> List[Dict[str, Any]]:
        params = ()
        sql = "SELECT * FROM etiqueta"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Palabras Clave
    # └────────────────────────────────────────────────────────────┘
    def get_palabras_clave(self) -> List[Dict[str, Any]]:
        params = ()
        sql = "SELECT * FROM palabra_clave"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Categorias
    # └────────────────────────────────────────────────────────────┘

    def get_categorias(self) -> List[Dict[str, Any]]:
        params = ()
        sql = "SELECT * FROM categoria"
        return self._ejecutar_consulta(sql=sql, params=params)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Metodos de la clase abstracta
    # └────────────────────────────────────────────────────────────┘

    def crear_tabla(self):
        return super().crear_tabla()

    def eliminar(self, sql, params=...):
        return super().eliminar(sql, params)

    def existe(self, sql, params=...):
        return super().existe(sql, params)

    def insertar(self, sql, params=...):
        return super().insertar(sql, params)

    def instanciar(self, sql, params=...):
        return super().instanciar(sql, params)
