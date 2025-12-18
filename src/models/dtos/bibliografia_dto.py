from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BibliografiaDTO:
    """
    DTO unificado para representar los datos bibliográficos de un documento.

    Representa la información de la tabla consolidada `bibliografia`.

    Attributes:
        id_documento (int): Identificador del documento asociado.
        titulo (str): Título completo del documento.
        id (Optional[int]): ID del registro en la tabla `bibliografia`.
        autores (Optional[str]): Nombre(s) del(los) autor(es).
        ano_publicacion (Optional[int]): Año de publicación.
        editorial (Optional[str]): Nombre de la editorial.
        lugar_publicacion (Optional[str]): Lugar de publicación (ciudad, país).
        numero_edicion (Optional[int]): Número de edición del documento.
        idioma (Optional[str]): Idioma del documento.
        volumen_tomo (Optional[str]): Volumen o tomo.
        numero_paginas (Optional[int]): Cantidad total de páginas.
        isbn (Optional[str]): ISBN del documento.
        creado_en (Optional[str]): Fecha de creación del registro principal.
        actualizado_en (Optional[str]): Fecha de última actualización del registro principal.
    """

    id_documento: int
    titulo: str
    id: Optional[int] = field(default=None)
    autores: Optional[str] = field(default=None)
    ano_publicacion: Optional[int] = field(default=None)
    editorial: Optional[str] = field(default=None)
    lugar_publicacion: Optional[str] = field(default=None)
    numero_edicion: Optional[int] = field(default=None)
    idioma: Optional[str] = field(default=None)
    volumen_tomo: Optional[str] = field(default=None)
    numero_paginas: Optional[int] = field(default=None)
    isbn: Optional[str] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
