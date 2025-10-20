from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentDTO:
    """
    DTO para representar documentos en la biblioteca.

    Esta clase encapsula toda la información necesaria para gestionar documentos
    en el sistema, incluyendo sus metadatos y estado.

    Attributes:
        id (Optional[int]): Identificador único del documento
        name (str): Nombre del documento
        extension (str): Extensión del archivo (pdf, doc, etc.)
        hash (str): Hash único del archivo para verificar integridad
        size (float): Tamaño del archivo en bytes
        is_active (bool): Estado del documento (activo/inactivo)
        created_at (Optional[str]): Fecha y hora de creación del documento
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> documento = DocumentDTO(
        ...     name="manual_usuario",
        ...     extension="pdf",
        ...     hash="abc123def456",
        ...     size=1024.5,
        ...     is_active=True
        ... )
    """

    id: Optional[int] = None
    name: str
    extension: str
    hash: str
    size: float
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
