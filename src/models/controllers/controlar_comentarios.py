import json
from datetime import datetime
from os.path import join, exists, dirname
from typing import Any, Dict, Optional
import os

from utilities.configuracion import RUTA_DATA


class ControlarComentarios:
    def __init__(self, ruta_archivo: Optional[str] = None):
        self.ruta_archivo = ruta_archivo or join(RUTA_DATA, "comentarios.json")

    def obtener_comentario(self, id_documento: int) -> str:
        id_normalizado = self._normalizar_id(id_documento)
        if id_normalizado is None:
            return ""

        data = self._leer_archivo()
        comentario = data.get("comentarios", {}).get(id_normalizado)
        if isinstance(comentario, dict):
            texto = comentario.get("texto", "")
            return str(texto) if texto is not None else ""
        if isinstance(comentario, str):
            return comentario
        return ""

    def obtener_comentarios(self) -> Dict[str, Any]:
        data = self._leer_archivo()
        comentarios = data.get("comentarios", {})
        return comentarios if isinstance(comentarios, dict) else {}

    def guardar_comentario(self, id_documento: int, texto: str) -> bool:
        id_normalizado = self._normalizar_id(id_documento)
        if id_normalizado is None:
            return False

        texto_normalizado = (texto or "").strip()
        data = self._leer_archivo()
        comentarios = data.get("comentarios", {})
        if not isinstance(comentarios, dict):
            comentarios = {}

        if texto_normalizado:
            comentarios[id_normalizado] = {
                "texto": texto_normalizado,
                "actualizado_en": datetime.now().isoformat(timespec="seconds"),
            }
        else:
            comentarios.pop(id_normalizado, None)

        data["comentarios"] = comentarios
        return self._guardar_archivo(data)

    def _leer_archivo(self) -> Dict[str, Any]:
        if not exists(self.ruta_archivo):
            return {"comentarios": {}}

        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception:
            return {"comentarios": {}}

        if not isinstance(data, dict):
            return {"comentarios": {}}

        comentarios = data.get("comentarios", {})
        if not isinstance(comentarios, dict):
            comentarios = {}

        return {"comentarios": comentarios}

    def _guardar_archivo(self, data: Dict[str, Any]) -> bool:
        try:
            os.makedirs(dirname(self.ruta_archivo), exist_ok=True)
            with open(self.ruta_archivo, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def _normalizar_id(self, id_documento: int) -> Optional[str]:
        try:
            return str(int(id_documento))
        except (TypeError, ValueError):
            return None
