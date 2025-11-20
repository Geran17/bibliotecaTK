from typing import Optional
from src.models.dtos.documento_etiqueta_dto import DocumentoEtiquetaDTO
from src.models.daos.documento_etiqueta_dao import DocumentoEtiquetaDAO


class DocumentoEtiqueta(DocumentoEtiquetaDTO):
    """
    Clase de entidad que representa la asociación entre un Documento y una Etiqueta.

    Hereda de `DocumentoEtiquetaDTO` y añade la lógica para interactuar
    con la base de datos a través de `DocumentoEtiquetaDAO`.
    """

    def __init__(
        self,
        id_documento: int,
        id_etiqueta: int,
        creado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad de asociación DocumentoEtiqueta.

        Args:
            id_documento (int): ID del documento.
            id_etiqueta (int): ID de la etiqueta.
            creado_en (Optional[str]): Fecha de creación.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            id_etiqueta=id_etiqueta,
        )
        self.creado_en = creado_en
        self._dao = DocumentoEtiquetaDAO(ruta_db=ruta_db)

    def asociar(self) -> Optional[int]:
        """
        Crea la asociación en la base de datos.

        Returns:
            Optional[int]: El rowid de la nueva asociación, o None si falla.
        """
        params = (self.id_documento, self.id_etiqueta)
        return self._dao.insertar(params=params)

    def desasociar(self) -> bool:
        """
        Elimina la asociación de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id_documento, self.id_etiqueta)
        return self._dao.eliminar(params=params)

    def existe(self) -> bool:
        """
        Verifica si la asociación ya existe en la base de datos.

        Returns:
            bool: True si la asociación existe, False en caso contrario.
        """
        params = (self.id_documento, self.id_etiqueta)
        return self._dao.existe(params=params)
