from typing import Optional
from models.dtos.documento_etiqueta_dto import DocumentoEtiquetaDTO
from models.daos.documento_etiqueta_dao import DocumentoEtiquetaDAO


class DocumentoEtiqueta(DocumentoEtiquetaDTO):
    """
    Clase de entidad que representa la asociación entre un Documento y una Etiqueta.

    Hereda de `DocumentoEtiquetaDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `DocumentoEtiquetaDAO`.

    Attributes:
        _dao (DocumentoEtiquetaDAO): Instancia del DAO para la asociación.
    """

    def __init__(
        self,
        id_documento: int,
        id_etiqueta: int,
        id: Optional[int] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad de asociación DocumentoEtiqueta.

        Args:
            id_documento (int): ID del documento.
            id_etiqueta (int): ID de la etiqueta.
            id (Optional[int]): ID de la asociación en la base de datos.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            id_etiqueta=id_etiqueta,
        )
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en
        self._dao = DocumentoEtiquetaDAO(ruta_db=ruta_db)
        self._dao.crear_tabla()

    def asociar(self) -> Optional[int]:
        """
        Crea un nuevo registro de asociación en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro, o None si falla.
        """
        params = (self.id_documento, self.id_etiqueta)
        return self._dao.insertar(params=params)

    def desasociar(self) -> bool:
        """
        Elimina el registro de asociación de la base de datos.

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
