from dataclasses import dataclass
from typing import Optional


@dataclass
class CapituloDTO:
    """
    DTO para representar los capítulos de un documento.

    Attributes:
        id (Optional[int]): Identificador único del capítulo.
        id_documento (int): ID del documento al que pertenece el capítulo.
        numero_capitulo (int): Número de orden del capítulo.
        titulo (str): Título del capítulo.
        pagina_inicio (Optional[int]): Página donde comienza el capítulo.
        creado_en (Optional[str]): Fecha de creación del registro.
        actualizado_en (Optional[str]): Fecha de última actualización.
    """

    id_documento: int
    numero_capitulo: int
    titulo: str
    id: Optional[int] = None
    pagina_inicio: Optional[int] = None
    creado_en: Optional[str] = None
    actualizado_en: Optional[str] = None
