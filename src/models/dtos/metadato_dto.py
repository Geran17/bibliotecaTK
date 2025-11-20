from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MetadatoDTO:
    """
    DTO (Data Transfer Object) para la entidad Metadato.

    Representa un par clave-valor de metadatos asociados a un documento.

    Attributes:
        id_documento (int): ID del documento al que pertenece el metadato.
        clave (str): La clave del metadato (ej. 'Author', 'CreationDate').
        valor (str): El valor del metadato.
        id (Optional[int]): ID único del metadato en la base de datos.
        creado_en (Optional[str]): Fecha y hora de creación del registro.
        actualizado_en (Optional[str]): Fecha y hora de la última actualización.
    """

    id_documento: int
    clave: str
    valor: str
    id: Optional[int] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
