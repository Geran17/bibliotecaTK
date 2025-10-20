from dataclasses import dataclass
from typing import Optional


class FavoriteDTO:
    """
    DTO para representar documentos marcados como favoritos.

    Esta clase encapsula la información necesaria para gestionar los documentos
    marcados como favoritos por el usuario. Permite un acceso rápido a los
    documentos más importantes o frecuentemente consultados.

    Attributes:
        id (Optional[int]): Identificador único del registro favorito
        id_doc (int): Identificador del documento marcado como favorito
        created_at (Optional[str]): Fecha y hora en que se marcó como favorito
        updated_at (Optional[str]): Fecha y hora de última actualización

    Example:
        >>> favorito = FavoriteDTO(
        ...     id_doc=1,
        ... )
    """

    id: Optional[int] = None
    id_doc: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
