from typing import Optional
from src.models.dtos.dato_bibliografico_dto import DatoBibliograficoDTO
from src.models.daos.dato_bibliografico_dao import DatoBibliograficoDAO


class DatoBibliografico(DatoBibliograficoDTO):
    """
    Clase de entidad que representa los Datos Bibliográficos de un documento.

    Hereda de `DatoBibliograficoDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `DatoBibliograficoDAO`.

    Attributes:
        _dao (DatoBibliograficoDAO): Instancia del DAO para datos bibliográficos.
    """

    def __init__(
        self,
        titulo: str,
        id_documento: int,
        id: Optional[int] = None,
        autores: Optional[str] = None,
        ano_publicacion: Optional[int] = None,
        editorial: Optional[str] = None,
        lugar_publicacion: Optional[str] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad DatoBibliografico.

        Args:
            titulo (str): Título del documento.
            id_documento (int): ID del documento asociado.
            id (Optional[int]): ID del registro en la base de datos.
            autores (Optional[str]): Autores del documento.
            ano_publicacion (Optional[int]): Año de publicación.
            editorial (Optional[str]): Editorial del documento.
            lugar_publicacion (Optional[str]): Lugar de publicación.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            titulo=titulo,
            id_documento=id_documento,
            id=id,
            autores=autores,
            ano_publicacion=ano_publicacion,
            editorial=editorial,
            lugar_publicacion=lugar_publicacion,
        )
        # Asignar campos no inicializados en el DTO
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

        self._dao = DatoBibliograficoDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (
            self.titulo,
            self.autores,
            self.ano_publicacion,
            self.editorial,
            self.lugar_publicacion,
            self.id_documento,
        )
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (
            self.titulo,
            self.autores,
            self.ano_publicacion,
            self.editorial,
            self.lugar_publicacion,
            self.id_documento,
            self.id,
        )
        return self._dao.actualizar_todo(params=params)

    def eliminar(self) -> bool:
        """
        Elimina el registro correspondiente de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id,)
        return self._dao.eliminar(params=params)

    def instanciar(self) -> bool:
        """
        Carga los datos desde la base de datos y los asigna a los atributos del objeto.

        Utiliza el `id` del objeto para buscar el registro.

        Returns:
            bool: True si el registro se encontró y el objeto se actualizó, False en caso contrario.
        """
        params = (self.id,)
        lista = self._dao.instanciar(params=params)
        if not lista:
            return False

        data = lista[0]
        self.titulo = data["titulo"]
        self.autores = data["autores"]
        self.ano_publicacion = data["ano_publicacion"]
        self.editorial = data["editorial"]
        self.lugar_publicacion = data["lugar_publicacion"]
        self.id_documento = data["id_documento"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existen datos bibliográficos para el documento asociado.

        Returns:
            bool: True si los datos existen, False en caso contrario.
        """
        params = (self.id_documento,)
        return self._dao.existe(params=params)
