from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PalabraClaveDTO:
    """
    DTO (Data Transfer Object) para la entidad PalabraClave.

    Representa una palabra clave para facilitar la búsqueda de documentos.

    Attributes:
        palabra (str): Texto de la palabra clave.
        id (Optional[int]): ID único de la palabra clave en la base de datos.
        descripcion (Optional[str]): Descripción o contexto de la palabra clave.
        creado_en (Optional[str]): Fecha y hora de creación del registro.
        actualizado_en (Optional[str]): Fecha y hora de la última actualización.
    """

    palabra: str
    id: Optional[int] = field(default=None)
    descripcion: Optional[str] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
