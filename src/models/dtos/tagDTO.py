from dataclasses import dataclass
from typing import Optional


@dataclass
class TagDTO:
    """
    DTO para representar etiquetas de documentos.

    Esta clase encapsula la información necesaria para gestionar las etiquetas
    que permiten clasificar y organizar los documentos según criterios
    definidos por el usuario.

    Attributes:
        id (Optional[int]): Identificador único de la etiqueta
        name (str): Nombre descriptivo de la etiqueta
        description (Optional[str]): Descripción detallada de la etiqueta
        created_at (Optional[str]): Fecha y hora de creación del registro
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> etiqueta = TagDTO(
        ...     name="Importante",
        ...     description="Documentos marcados como importantes"
        ... )
    """

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
