from typing import Optional
from src.models.dtos.favorito_dto import FavoritoDTO
from src.models.daos.favorito_dao import FavoritoDAO


class Favorito(FavoritoDTO):
    """
    Clase de entidad que representa un documento Favorito.

    Hereda de `FavoritoDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `FavoritoDAO`.
    """

    def __init__(
        self,
        id_documento: int,
        id: Optional[int] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad Favorito.

        Args:
            id_documento (int): ID del documento a marcar como favorito.
            id (Optional[int]): ID del registro de favorito en la base de datos.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            id=id,
        )
        # Asignar campos no inicializados en el DTO
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

        self._dao = FavoritoDAO(ruta_db=ruta_db)

    def marcar(self) -> Optional[int]:
        """
        Marca el documento como favorito, creando un registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro de favorito, o None si falla.
        """
        params = (self.id_documento,)
        return self._dao.insertar(params=params)

    def desmarcar(self) -> bool:
        """
        Quita la marca de favorito del documento, eliminando el registro.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id_documento,)
        return self._dao.eliminar(params=params)

    def instanciar(self) -> bool:
        """
        Carga los datos del favorito desde la base de datos.

        Utiliza el `id_documento` para buscar el registro.

        Returns:
            bool: True si el registro se encontró y el objeto se actualizó, False en caso contrario.
        """
        params = (self.id_documento,)
        lista = self._dao.instanciar(params=params)
        if not lista:
            return False

        data = lista[0]
        self.id = data["id"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si el documento ya está marcado como favorito.

        Returns:
            bool: True si el documento es favorito, False en caso contrario.
        """
        params = (self.id_documento,)
        return self._dao.existe(params=params)
