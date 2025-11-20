from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatoBibliograficoComplementarioDTO:
    """
    DTO para la información bibliográfica complementaria de un documento.

    Encapsula detalles adicionales como edición, idioma, ISBN, etc.

    Attributes:
        id_dato_bibliografico (int): ID del dato bibliográfico principal relacionado.
        id (Optional[int]): ID único del registro complementario.
        numero_edicion (Optional[int]): Número de edición del documento.
        idioma (Optional[str]): Idioma del documento.
        volumen_tomo (Optional[str]): Volumen o tomo del documento.
        numero_paginas (Optional[int]): Número total de páginas.
        isbn (Optional[str]): Número ISBN del documento.
        creado_en (Optional[str]): Fecha y hora de creación del registro.
        actualizado_en (Optional[str]): Fecha y hora de última actualización.
    """

    id_dato_bibliografico: int
    id: Optional[int] = field(default=None)
    numero_edicion: Optional[int] = field(default=None)
    idioma: Optional[str] = field(default=None)
    volumen_tomo: Optional[str] = field(default=None)
    numero_paginas: Optional[int] = field(default=None)
    isbn: Optional[str] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
