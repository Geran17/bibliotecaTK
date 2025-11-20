from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EtiquetaDTO:
    """
    DTO (Data Transfer Object) para la entidad Etiqueta.

    Representa una etiqueta personalizada para organizar documentos.

    Attributes:
        nombre (str): Nombre descriptivo de la etiqueta.
        id (Optional[int]): ID único de la etiqueta en la base de datos.
        descripcion (Optional[str]): Descripción detallada de la etiqueta.
        creado_en (Optional[str]): Fecha y hora de creación del registro.
        actualizado_en (Optional[str]): Fecha y hora de la última actualización.
    """

    nombre: str
    id: Optional[int] = field(default=None)
    descripcion: Optional[str] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
