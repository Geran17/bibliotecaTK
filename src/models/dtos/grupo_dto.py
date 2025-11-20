from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GrupoDTO:
    """Genera la clase DTO para la entidad Grupo.

    Attributes:
        nombre (str): Nombre descriptivo del grupo.
        id (Optional[int]): ID único del grupo en la base de datos.
        descripcion (Optional[str]): Descripción detallada del grupo.
        creado_en (Optional[str]): Fecha y hora de creación del registro.
        actualizado_en (Optional[str]): Fecha y hora de la última actualización.
    """

    nombre: str
    id: Optional[int] = field(default=None)
    descripcion: Optional[str] = field(default=None)
    creado_en: Optional[str] = field(default=None, init=False)
    actualizado_en: Optional[str] = field(default=None, init=False)
