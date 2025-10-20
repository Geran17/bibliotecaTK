from dataclasses import dataclass


@dataclass
class BibliographyDataDTO:
    """
    DTO para representar la bibliographyData
    """

    id: int
    title: str
    authors: str
    year_publication: int
    editorial: str
    place_publication: str
    id_doc: int
