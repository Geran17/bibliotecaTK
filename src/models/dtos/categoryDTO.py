from dataclasses import dataclasss
from typing import Optional


class CategoryDTO:
    """
    DTO para representar categorías de documentos.

    Esta clase encapsula la información necesaria para gestionar las categorías
    que permiten clasificar y organizar los documentos en la biblioteca según
    su temática o propósito.

    Attributes:
        id (Optional[int]): Identificador único de la categoría
        name (str): Nombre descriptivo de la categoría
        description (Optional[str]): Descripción detallada de la categoría
        created_at (Optional[str]): Fecha y hora de creación de la categoría
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> categoria = CategoryDTO(
        ...     name="Documentos Técnicos",
        ...     description="Categoría para manuales y documentación técnica"
        ... )
    """

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
