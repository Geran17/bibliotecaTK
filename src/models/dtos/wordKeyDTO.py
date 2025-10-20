from dataclasses import dataclass
from typing import Optional


@dataclass
class WordKeyDTO:
    """
    DTO para representar palabras clave de documentos.

    Esta clase encapsula la información necesaria para gestionar las palabras clave
    que permiten categorizar y buscar documentos en la biblioteca según términos
    específicos.

    Attributes:
        id (Optional[int]): Identificador único de la palabra clave
        wordkey (str): Texto de la palabra clave
        description (Optional[str]): Descripción o contexto de la palabra clave
        created_at (Optional[str]): Fecha y hora de creación del registro
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> palabra_clave = WordKeyDTO(
        ...     wordkey="Python",
        ...     description="Lenguaje de programación usado en el proyecto"
        ... )
    """

    id: Optional[int] = None
    wordkey: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
