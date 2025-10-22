from dataclasses import dataclass
from typing import Optional


@dataclass
class MetaDataDTO:
    """
    DTO para representar metadatos de documentos.

    Esta clase encapsula la información de metadatos extraída de los documentos
    usando herramientas como ExifTool. Almacena pares de clave-valor que
    describen características específicas del documento.

    Attributes:
        id (Optional[int]): Identificador único del metadato
        id_doc (int): Identificador del documento al que pertenece
        key_data (str): Clave o nombre del metadato
        value_data (str): Valor del metadato
        created_at (str): Fecha y hora de creación del registro
        updated_at (str): Fecha y hora de última modificación

    Example:
        >>> metadato = MetaDataDTO(
        ...     id_doc=1,
        ...     key_data="Author",
        ...     value_data="John Doe",
        ...     created_at="2023-10-21 10:00:00",
        ...     updated_at="2023-10-21 10:00:00"
        ... )
    """

    id: Optional[int] = None
    id_doc: int
    key_data: str
    value_data: str
    created_at: str
    updated_at: str
