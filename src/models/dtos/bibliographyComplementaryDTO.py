from dataclasses import dataclass
from typing import Optional


@dataclass
class BibliographyComplementaryDTO:
    """
    DTO para representar información bibliográfica complementaria.

    Esta clase encapsula los datos complementarios de una referencia bibliográfica,
    incluyendo detalles específicos como edición, idioma, volumen y ISBN.

    Attributes:
        id (Optional[int]): Identificador único del registro complementario
        id_bib (int): Identificador de la bibliografía relacionada
        number_edition (int): Número de edición del documento
        language (str): Idioma del documento
        volumen_tomo (str): Volumen o tomo del documento
        number_pagina (int): Número de páginas
        isbn (str): Número ISBN del documento
        created_at (Optional[str]): Fecha y hora de creación del registro
        updated_at (Optional[str]): Fecha y hora de última actualización

    Example:
        >>> biblio_comp = BibliographyComplementaryDTO(
        ...     id_bib=1,
        ...     number_edition=2,
        ...     language="Español",
        ...     volumen_tomo="Tomo I",
        ...     number_pagina=250,
        ...     isbn="978-0-123456-47-2"
        ... )
    """

    id: Optional[int] = None
    id_bib: int
    number_edition: Optional[int] = None
    language: Optional[str] = None
    volumen_tomo: Optional[str] = None
    number_pagina: Optional[int] = None
    isbn: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
