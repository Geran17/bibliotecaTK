from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatoBibliograficoDTO:
    """
    DTO para representar los datos bibliográficos de un documento.

    Encapsula la información bibliográfica básica como título, autores, año, etc.

    Attributes:
        titulo (str): Título completo del documento.
        id_documento (int): Identificador del documento asociado.
        id (Optional[int]): ID único del registro bibliográfico.
        autores (Optional[str]): Nombre(s) del(los) autor(es).
        ano_publicacion (Optional[int]): Año de publicación.
        editorial (Optional[str]): Nombre de la editorial.
        lugar_publicacion (Optional[str]): Lugar de publicación (ciudad, país).
        creado_en (Optional[str]): Fecha de creación del registro.
        actualizado_en (Optional[str]): Fecha de última actualización.
    """

    titulo: str
    id_documento: int
    id: Optional[int] = field(default=None)
    autores: Optional[str] = field(default=None)
    ano_publicacion: Optional[int] = field(default=None)
    editorial: Optional[str] = field(default=None)
    lugar_publicacion: Optional[str] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
