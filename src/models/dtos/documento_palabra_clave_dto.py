from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocumentoPalabraClaveDTO:
    """
    DTO para la relación entre Documento y PalabraClave.

    Representa la asociación en la tabla pivote `documento_palabra_clave`.

    Attributes:
        id_documento (int): ID del documento.
        id_palabra_clave (int): ID de la palabra clave.
        creado_en (Optional[str]): Fecha de creación de la asociación.
    """

    id_documento: int
    id_palabra_clave: int
    creado_en: Optional[str] = field(default=None, init=False)
