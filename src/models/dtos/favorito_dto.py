from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FavoritoDTO:
    """
    DTO (Data Transfer Object) para la entidad Favorito.

    Representa la marca de un documento como favorito.

    Attributes:
        id_documento (int): ID del documento marcado como favorito.
        id (Optional[int]): ID único del registro de favorito.
        creado_en (Optional[str]): Fecha de creación del registro.
        actualizado_en (Optional[str]): Fecha de la última actualización.
    """

    id_documento: int
    id: Optional[int] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
