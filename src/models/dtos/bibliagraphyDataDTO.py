from dataclasses import dataclass
from typing import Optional


@dataclass
class BibliographyDataDTO:
    """
    DTO para representar los datos bibliográficos de un documento.

    Esta clase encapsula toda la información bibliográfica básica de un documento,
    incluyendo título, autores, año de publicación y detalles editoriales.

    Attributes:
        id (Optional[int]): Identificador único del registro bibliográfico
        title (str): Título completo del documento
        authors (str): Nombre(s) del(los) autor(es)
        year_publication (int): Año de publicación
        editorial (str): Nombre de la editorial
        place_publication (str): Lugar de publicación (ciudad, país)
        id_doc (int): Identificador del documento asociado
        created_at (Optional[str]): Fecha de creación del registro
        updated_at (Optional[str]): Fecha de última actualización

    Example:
        >>> biblio = BibliographyDataDTO(
        ...     title="Python Programming",
        ...     authors="John Doe",
        ...     year_publication=2023,
        ...     editorial="Tech Books",
        ...     place_publication="New York, USA",
        ...     id_doc=1
        ... )
    """

    id: Optional[int] = None
    title: str
    authors: str
    year_publication: int
    editorial: str
    place_publication: str
    id_doc: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
