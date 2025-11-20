from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocumentoEtiquetaDTO:
    """
    DTO para la relación entre Documento y Etiqueta.

    Representa la asociación en la tabla pivote `documento_etiqueta`.

    Attributes:
        id_documento (int): ID del documento.
        id_etiqueta (int): ID de la etiqueta.
        creado_en (Optional[str]): Fecha de creación de la asociación.
    """

    id_documento: int
    id_etiqueta: int
    creado_en: Optional[str] = field(default=None, init=False)
