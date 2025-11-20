from dataclasses import dataclass
from typing import Optional


@dataclass
class ColeccionDTO:
    """
    DTO para representar las colecciones o grupos de documentos.

    Attributes:
        id (Optional[int]): Identificador único de la colección.
        nombre (str): El nombre de la colección (ej. "Libros de Programación").
        descripcion (Optional[str]): Descripción opcional de la colección.
        creado_en (Optional[str]): Fecha y hora de creación.
        actualizado_en (Optional[str]): Fecha y hora de la actualizacion.
    """

    nombre: str
    id: Optional[int] = None
    descripcion: Optional[str] = None
    creado_en: Optional[str] = None
    actualizado_en: Optional[str] = None
