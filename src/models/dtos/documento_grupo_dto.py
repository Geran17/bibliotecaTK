from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocumentoGrupoDTO:
    """
    DTO para la relación entre Documento y Grupo.

    Representa la asociación en la tabla pivote `documento_grupo`.

    Attributes:
        id_documento (int): ID del documento.
        id_grupo (int): ID del grupo.
        creado_en (Optional[str]): Fecha de creación de la asociación.
    """

    id_documento: int
    id_grupo: int
    creado_en: Optional[str] = field(default=None, init=False)
