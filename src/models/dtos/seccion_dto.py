from dataclasses import dataclass
from typing import Optional


@dataclass
class SeccionDTO:
    """
    DTO para representar las secciones de un capítulo.

    Attributes:
        id (Optional[int]): Identificador único de la sección.
        id_capitulo (int): ID del capítulo al que pertenece la sección.
        titulo (str): Título de la sección.
        nivel (Optional[str]): Nivel jerárquico de la sección (e.g., '1.1', '1.1.1').
        id_padre (Optional[int]): ID de la sección padre (para jerarquías).
        numero_pagina (Optional[int]): Página donde comienza la sección.
        creado_en (Optional[str]): Fecha de creación del registro.
        actualizado_en (Optional[str]): Fecha de última actualización.
    """

    id_capitulo: int
    titulo: str
    id: Optional[int] = None
    nivel: Optional[str] = None
    id_padre: Optional[int] = None
    numero_pagina: Optional[int] = None
    creado_en: Optional[str] = None
    actualizado_en: Optional[str] = None
