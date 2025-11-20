from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocumentoCategoriaDTO:
    """
    DTO para la relación entre Documento y Categoria.

    Representa la asociación en la tabla pivote `documento_categoria`.

    Attributes:
        id_documento (int): ID del documento.
        id_categoria (int): ID de la categoría.
        creado_en (Optional[str]): Fecha de creación de la asociación.
    """

    id_documento: int
    id_categoria: int
    creado_en: Optional[str] = field(default=None, init=False)
