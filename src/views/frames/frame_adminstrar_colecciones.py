"""Compatibilidad retroactiva.

Use `views.frames.frame_administrar_colecciones` en código nuevo.
"""

from views.frames.frame_administrar_colecciones import AdministrarColecciones

__all__ = ["AdministrarColecciones"]
