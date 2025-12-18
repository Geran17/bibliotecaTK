from typing import Optional
from models.dtos.documento_grupo_dto import DocumentoGrupoDTO
from models.daos.documento_grupo_dao import DocumentoGrupoDAO


class DocumentoGrupo(DocumentoGrupoDTO):
    """
    Clase de entidad que representa la asociación entre un Documento y un Grupo.

    Hereda de `DocumentoGrupoDTO` y añade la lógica para interactuar
    con la base de datos a través de `DocumentoGrupoDAO`.
    """

    def __init__(
        self,
        id_documento: int,
        id_grupo: int,
        creado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad de asociación DocumentoGrupo.

        Args:
            id_documento (int): ID del documento.
            id_grupo (int): ID del grupo.
            creado_en (Optional[str]): Fecha de creación.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            id_grupo=id_grupo,
        )
        self.creado_en = creado_en
        self._dao = DocumentoGrupoDAO(ruta_db=ruta_db)

    def asociar(self) -> Optional[int]:
        """
        Crea la asociación en la base de datos.

        Returns:
            Optional[int]: El rowid de la nueva asociación, o None si falla.
        """
        params = (self.id_documento, self.id_grupo)
        return self._dao.insertar(params=params)

    def desasociar(self) -> bool:
        """
        Elimina la asociación de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id_documento, self.id_grupo)
        return self._dao.eliminar(params=params)

    def existe(self) -> bool:
        """
        Verifica si la asociación ya existe en la base de datos.

        Returns:
            bool: True si la asociación existe, False en caso contrario.
        """
        params = (self.id_documento, self.id_grupo)
        return self._dao.existe(params=params)
