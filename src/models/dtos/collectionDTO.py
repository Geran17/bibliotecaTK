from dataclasses import dataclass
from typing import Optional


@dataclass
class CollectionDTO:
    """
    DTO para representar una colección de documentos.

    Esta clase encapsula la información necesaria para gestionar colecciones
    de documentos en la biblioteca. Las colecciones permiten organizar
    documentos según criterios definidos por el usuario.

    Attributes:
        id (Optional[int]): Identificador único de la colección en la base de datos
        name (str): Nombre descriptivo de la colección
        description (Optional[str]): Descripción detallada de la colección
        created_at (Optional[str]): Fecha y hora de creación de la colección
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> collection = CollectionDTO(
        ...     name="Documentos Académicos",
        ...     description="Colección de papers y documentos de investigación"
        ... )
    """

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
