from typing import Optional
from models.dtos.documento_coleccion_dto import DocumentoColeccionDTO
from models.daos.documento_coleccion_dao import DocumentoColeccionDAO


class DocumentoColeccion(DocumentoColeccionDTO):
    """
    Clase de entidad que representa la asociación entre un Documento y una Coleccion.

    Hereda de `DocumentoColeccionDTO` y añade la lógica para interactuar
    con la base de datos a través de `DocumentoColeccionDAO`.
    """

    def __init__(
        self,
        id_documento: int,
        id_coleccion: int,
        creado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad de asociación DocumentoColeccion.

        Args:
            id_documento (int): ID del documento.
            id_coleccion (int): ID de la colección.
            creado_en (Optional[str]): Fecha de creación.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            id_coleccion=id_coleccion,
        )
        self.creado_en = creado_en
        self._dao = DocumentoColeccionDAO(ruta_db=ruta_db)

    def asociar(self) -> Optional[int]:
        """
        Crea la asociación en la base de datos.

        Returns:
            Optional[int]: El rowid de la nueva asociación, o None si falla.
        """
        params = (self.id_documento, self.id_coleccion)
        return self._dao.insertar(params=params)

    def desasociar(self) -> bool:
        """
        Elimina la asociación de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id_documento, self.id_coleccion)
        return self._dao.eliminar(params=params)

    def existe(self) -> bool:
        """
        Verifica si la asociación ya existe en la base de datos.

        Returns:
            bool: True si la asociación existe, False en caso contrario.
        """
        params = (self.id_documento, self.id_coleccion)
        return self._dao.existe(params=params)
