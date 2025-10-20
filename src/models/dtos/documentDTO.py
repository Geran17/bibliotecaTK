from dataclasses import dataclass


@dataclass
class DocumentDTO:
    """
    DTO para representar el documento
    """

    id: int
    name: str
    extension: str
    hash: str
    size: float
    is_active: bool
    created_at: str
    updated_at: str
