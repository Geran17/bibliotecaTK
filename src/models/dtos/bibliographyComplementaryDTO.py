from dataclasses import dataclass


@dataclass
class BibliographyComplementaryDTO:
    """
    DTO para representar el BibliographyComplementary
    """

    id: int
    id_bib: int
    number_edition: int
    language: str
    volumen_tomo: str
    number_pagina: int
    isbn: str
