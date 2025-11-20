from typing import Optional
from src.models.dtos.documento_palabra_clave_dto import DocumentoPalabraClaveDTO
from src.models.daos.documento_palabra_clave_dao import DocumentoPalabraClaveDAO


class DocumentoPalabraClave(DocumentoPalabraClaveDTO):
    """
    Clase de entidad que representa la asociación entre un Documento y una PalabraClave.

    Hereda de `DocumentoPalabraClaveDTO` y añade la lógica para interactuar
    con la base de datos a través de `DocumentoPalabraClaveDAO`.
    """

    def __init__(
        self,
        id_documento: int,
        id_palabra_clave: int,
        creado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad de asociación DocumentoPalabraClave.

        Args:
            id_documento (int): ID del documento.
            id_palabra_clave (int): ID de la palabra clave.
            creado_en (Optional[str]): Fecha de creación.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            id_palabra_clave=id_palabra_clave,
        )
        self.creado_en = creado_en
        self._dao = DocumentoPalabraClaveDAO(ruta_db=ruta_db)

    def asociar(self) -> Optional[int]:
        """
        Crea la asociación en la base de datos.

        Returns:
            Optional[int]: El rowid de la nueva asociación, o None si falla.
        """
        params = (self.id_documento, self.id_palabra_clave)
        return self._dao.insertar(params=params)

    def desasociar(self) -> bool:
        """
        Elimina la asociación de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id_documento, self.id_palabra_clave)
        return self._dao.eliminar(params=params)

    def existe(self) -> bool:
        """
        Verifica si la asociación ya existe en la base de datos.

        Returns:
            bool: True si la asociación existe, False en caso contrario.
        """
        params = (self.id_documento, self.id_palabra_clave)
        return self._dao.existe(params=params)
