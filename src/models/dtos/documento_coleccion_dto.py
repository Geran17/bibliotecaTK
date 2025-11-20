from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocumentoColeccionDTO:
    """
    DTO para la relación entre Documento y Coleccion.

    Representa la asociación en la tabla pivote `documento_coleccion`.

    Attributes:
        id_documento (int): ID del documento.
        id_coleccion (int): ID de la colección.
        creado_en (Optional[str]): Fecha de creación de la asociación.
    """

    id_documento: int
    id_coleccion: int
    creado_en: Optional[str] = field(default=None, init=False)
