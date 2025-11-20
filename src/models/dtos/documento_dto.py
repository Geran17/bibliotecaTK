from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentoDTO:
    """
    DTO para representar documentos en la biblioteca.

    Esta clase encapsula toda la información necesaria para gestionar documentos
    en el sistema, incluyendo sus metadatos y estado.

    Attributes:
        id (Optional[int]): Identificador único del documento
        nombre (str): Nombre del documento
        extension (str): Extensión del archivo (pdf, doc, etc.)
        hash (str): Hash único del archivo para verificar integridad
        tamano (int): Tamaño del archivo en bytes
        esta_activo (bool): Estado del documento (activo/inactivo)
        creado_en (Optional[str]): Fecha y hora de creación del documento
        actualizado_en (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> documento = DocumentoDTO(
        ...     nombre="manual_usuario",
        ...     extension="pdf",
        ...     hash="abc123def456",
        ...     tamano=1024,
        ...     esta_activo=True
        ... )
    """

    nombre: str
    extension: str
    hash: str
    tamano: int
    id: Optional[int] = None
    esta_activo: bool = True
    creado_en: Optional[str] = None
    actualizado_en: Optional[str] = None
