from os import mkdir
from os.path import join, isdir
import json
from utilities.fileINI import FileINI
from utilities.configuracion import CONFIG_INI
from pathlib import Path
from typing import Dict, Any


class ConfiguracionController:
    def __init__(self):
        self.nombre_biblioteca = "BibliotecaTK"
        self.nombre_portada = "Portadas"
        self.iniFile = FileINI(pathINI=CONFIG_INI)
        # ----- Seciones ----
        self.section_ubiaciones = "ubicaciones"
        self.section_estilo = "estilo"
        self.section_toggle = "toggle"
        self.section_ubicaciones = "ubicaciones"
        # ----- Keys --------
        self.key_ubicacion_biblioteca = "ubicacion_biblioteca"
        self.key_ubicacion_portadas = "ubicacion_portadas"
        self.key_tema = "tema"
        self.key_estilo_citacion = "estilo_citacion"
        self.key_entorno_ui = "entorno_ui"
        self.key_panel_laterial = "panel_lateral"
        self.key_panel_archivo = "panel_archivo"
        self.key_ultima_ubicacion = "ultima_ubicacion"
        self.key_copiar_ubicacion = "copiar_ubicacion"
        self.key_mover_ubicacion = "mover_ubicacion"
        self.key_mostrar_asociaciones = "mostrar_asociaciones"
        self.key_mostrar_datos_bibliograficos = "mostrar_datos_bibliograficos"
        self.key_mostrar_operaciones = "mostrar_operaciones"
        self.key_estado_vista_documentos = "estado_vista_documentos"
        self.key_estado_vista_estante = "estado_vista_estante"
        self.key_pestana_activa_principal = "pestana_activa_principal"
        # ----- Keys Pestañas -----
        self.key_pestana_bienvenida = "pestana_bienvenida"
        self.key_pestana_visualizar = "pestana_visualizar"
        self.key_pestana_favoritos = "pestana_favoritos"
        self.key_pestana_biblioteca = "pestana_biblioteca"
        self.key_pestana_contenido = "pestana_contenido"
        self.key_pestana_metadatos = "pestana_metadatos"

        # creamos la seccion [ubicaciones]
        if not self.iniFile.section_exist(section=self.section_ubiaciones):
            self.iniFile.add_section(
                section=self.section_ubiaciones,
                comment="ubicaciones varias que la aplicacion utiliza",
            )

        if not self.iniFile.section_exist(section=self.section_estilo):
            self.iniFile.add_section(
                section=self.section_estilo,
                comment="Es el tema actual de la aplicacion",
            )

        if not self.iniFile.section_exist(section=self.section_toggle):
            self.iniFile.add_section(
                section=self.section_toggle,
                comment="Es la seccion donde podemos definir que paneles ocultar",
            )

        if not self.iniFile.section_exist(section=self.section_ubiaciones):
            self.iniFile.add_section(
                section=self.section_ubiaciones,
                comment="Es la seccion donde podemos definir que paneles ocultar",
            )

    def establecer_ubicacion_biblioteca(self, directrio: str) -> bool:
        """
        Esta funcion se encargara de establcer la ubicacion del directorio de la biblioteca
        1)  tiene que verificar si existe el directorio "BibliotecaTK" dentro del directorio
            que el usuario proporciona
        2)  si el directorio existe el en la ubicacion proporcionada, la aplicacion solo actulizar
            el archivo de configuracion

        Args:
            directorio (str): esta la la ubicacion proporcionada por el usuario

        Return:
            bool: retorna un valor booleana si se ha registrado correctamente en el archivo de
                  configuraciones
        """
        if isdir(directrio):
            # Si es un directorio vefiricamos que el nombre no se igual a "BibliotecaTK"
            folder = Path(directrio)
            if folder.name != self.nombre_biblioteca:
                try:
                    dir_biblioteca = join(directrio, self.nombre_biblioteca)
                    dir_portada = join(dir_biblioteca, self.nombre_portada)
                    mkdir(dir_biblioteca)  # creamos el directorio: biblioteca
                    mkdir(dir_portada)  # creamos el directorio: portadas
                    # si el directorio se crea con existo, establcemos en el archivo de configuraciones
                    isValue = self.iniFile.add_value(
                        section=self.section_ubiaciones,
                        key=self.key_ubicacion_biblioteca,
                        value=dir_biblioteca,
                    )
                    isValue_portada = self.iniFile.add_value(
                        section=self.section_ubiaciones,
                        key=self.key_ubicacion_portadas,
                        value=dir_portada,
                    )
                    return isValue
                except Exception as e:
                    print(
                        f"No se pudo crear el directorio, para la biblioteca: {join(directrio, self.nombre_biblioteca)}"
                    )
                    return False
            elif folder.name == self.nombre_biblioteca:
                dir_portada = join(directrio, self.nombre_portada)
                if not isdir(dir_portada):
                    mkdir(dir_portada)
                isValue = self.iniFile.add_value(
                    section=self.section_ubiaciones,
                    key=self.key_ubicacion_biblioteca,
                    value=directrio,
                )
                self.iniFile.add_value(
                    section=self.section_ubiaciones,
                    key=self.key_ubicacion_portadas,
                    value=dir_portada,
                )
                return isValue
        else:
            print(f"La ubicacion proporcionada no es un directorio: {directrio}")
            return False

    def establecer_tema(self, tema: str = "cosmo") -> bool:
        if tema != "":
            return self.iniFile.add_value(
                section=self.section_estilo, key=self.key_tema, value=tema
            )

    def obtener_tema(self) -> str:
        return self.iniFile.get_value(section=self.section_estilo, key=self.key_tema)

    def establecer_estilo_citacion(self, estilo: str) -> bool:
        if estilo:
            return self.iniFile.add_value(
                section=self.section_estilo, key=self.key_estilo_citacion, value=estilo
            )

    def obtener_estilo_citacion(self) -> str:
        return self.iniFile.get_value(section=self.section_estilo, key=self.key_estilo_citacion)

    def establecer_entorno_ui(self, entorno_ui: str) -> bool:
        entorno_normalizado = (entorno_ui or "").strip().lower()
        if entorno_normalizado == "tkinter":
            return self.iniFile.add_value(
                section=self.section_estilo,
                key=self.key_entorno_ui,
                value=entorno_normalizado,
            )
        return False

    def obtener_entorno_ui(self) -> str:
        entorno_ui = self.iniFile.get_value(section=self.section_estilo, key=self.key_entorno_ui)
        entorno_normalizado = (entorno_ui or "").strip().lower()
        if entorno_normalizado == "tkinter":
            return entorno_normalizado
        return ""

    def obtener_ubicacion_biblioteca(self) -> str:
        ubicacion_biblioteca = self.iniFile.get_value(
            section=self.section_ubiaciones, key=self.key_ubicacion_biblioteca
        )
        return ubicacion_biblioteca

    def obtener_ubicacion_portadas(self) -> str:
        ubicacion_portadas = self.iniFile.get_value(
            section=self.section_ubiaciones, key=self.key_ubicacion_portadas
        )
        return ubicacion_portadas

    def get_toogle_panel_lateral(self) -> int:
        panel_lateral = self.iniFile.get_value(
            section=self.section_toggle, key=self.key_panel_laterial
        )
        return int(panel_lateral)

    def set_toggle_panel_lateral(self, valor: int) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_toggle, key=self.key_panel_laterial, value=str(valor)
            )

    def get_toogle_panel_archivo(self) -> int:
        valor = self.iniFile.get_value(section=self.section_toggle, key=self.key_panel_archivo)
        return int(valor)

    def set_toggle_panel_archivo(self, valor: int) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_toggle, key=self.key_panel_archivo, value=str(valor)
            )

    def get_ultima_ubicacion(self) -> str:
        valor = self.iniFile.get_value(
            section=self.section_ubicaciones, key=self.key_ultima_ubicacion
        )
        return valor

    def set_ultima_ubicacion(self, valor: str) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_ubicaciones,
                key=self.key_ultima_ubicacion,
                value=str(valor),
            )

    def get_copiar_ubicacion(self) -> str:
        valor = self.iniFile.get_value(
            section=self.section_ubicaciones, key=self.key_copiar_ubicacion
        )
        return valor

    def set_copiar_ubicacion(self, valor: str) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_ubicaciones,
                key=self.key_copiar_ubicacion,
                value=str(valor),
            )

    def get_mover_ubicacion(self) -> str:
        valor = self.iniFile.get_value(
            section=self.section_ubicaciones, key=self.key_mover_ubicacion
        )
        return valor

    def set_mover_ubicacion(self, valor: str) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_ubicaciones,
                key=self.key_mover_ubicacion,
                value=str(valor),
            )

    # ┌────────────────────────────────────────────────────────────┐
    # │ Toggle para el panel de asociaciones
    # └────────────────────────────────────────────────────────────┘

    def set_mostrar_asociaciones(self, valor: str) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_toggle,
                key=self.key_mostrar_asociaciones,
                value=str(valor),
            )

    def get_mostrar_asociaciones(self) -> str:
        valor = self.iniFile.get_value(
            section=self.section_toggle, key=self.key_mostrar_asociaciones
        )
        return valor

    # ┌────────────────────────────────────────────────────────────┐
    # │ Toggle para el panel de datos bibliograficos
    # └────────────────────────────────────────────────────────────┘

    def set_mostrar_datos_bibliograficos(self, valor: str) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_toggle,
                key=self.key_mostrar_datos_bibliograficos,
                value=str(valor),
            )

    def get_mostrar_datos_bibliograficos(self) -> str:
        valor = self.iniFile.get_value(
            section=self.section_toggle, key=self.key_mostrar_datos_bibliograficos
        )
        return valor

    # ┌────────────────────────────────────────────────────────────┐
    # │ Toggle para el panel de operaciones
    # └────────────────────────────────────────────────────────────┘

    def set_mostrar_operaciones(self, valor: str) -> bool:
        if valor is not None:
            return self.iniFile.add_value(
                section=self.section_toggle,
                key=self.key_mostrar_operaciones,
                value=str(valor),
            )

    def get_mostrar_operaciones(self) -> str:
        valor = self.iniFile.get_value(
            section=self.section_toggle, key=self.key_mostrar_operaciones
        )
        return valor

    # ┌────────────────────────────────────────────────────────────┐
    # │ Visibilidad de Pestañas
    # └────────────────────────────────────────────────────────────┘

    def obtener_visibilidad_pestanas(self) -> Dict[str, bool]:
        """
        Obtiene el diccionario de visibilidad de pestañas desde la configuración.

        Returns:
            Dict[str, bool]: Un diccionario donde las claves son los nombres
                             de las pestañas y los valores son booleanos.
        """
        visibilidad = {}
        defaults = {
            "bienvenida": True,
            "visualizar": True,
            "favoritos": True,
            "biblioteca": True,
            "contenido": True,
            "metadatos": True,
        }

        for key_short, default_value in defaults.items():
            ini_key = f"pestana_{key_short}"
            value_str = self.iniFile.get_value(section=self.section_toggle, key=ini_key)
            if value_str == "":  # La clave no existe en el INI
                visibilidad[key_short] = default_value
            else:
                visibilidad[key_short] = value_str.lower() == 'true'

        return visibilidad

    def guardar_visibilidad_pestanas(self, visibilidad: Dict[str, bool]) -> None:
        """
        Guarda el diccionario de visibilidad de pestañas en el archivo de
        configuración.
        """
        for key_short, is_visible in visibilidad.items():
            ini_key = f"pestana_{key_short}"
            value_str = str(is_visible)  # Convierte True a 'True' y False a 'False'
            self.iniFile.add_value(section=self.section_toggle, key=ini_key, value=value_str)

    def guardar_estado_vista_documentos(self, estado: Dict[str, Any]) -> bool:
        if not isinstance(estado, dict):
            return False
        try:
            value = json.dumps(estado, ensure_ascii=True)
            return self.iniFile.add_value(
                section=self.section_toggle,
                key=self.key_estado_vista_documentos,
                value=value,
            )
        except Exception:
            return False

    def obtener_estado_vista_documentos(self) -> Dict[str, Any]:
        raw = self.iniFile.get_value(
            section=self.section_toggle,
            key=self.key_estado_vista_documentos,
        )
        if not raw:
            return {}
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {}

    def guardar_estado_vista_estante(self, estado: Dict[str, Any]) -> bool:
        if not isinstance(estado, dict):
            return False
        try:
            value = json.dumps(estado, ensure_ascii=True)
            return self.iniFile.add_value(
                section=self.section_toggle,
                key=self.key_estado_vista_estante,
                value=value,
            )
        except Exception:
            return False

    def obtener_estado_vista_estante(self) -> Dict[str, Any]:
        raw = self.iniFile.get_value(
            section=self.section_toggle,
            key=self.key_estado_vista_estante,
        )
        if not raw:
            return {}
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {}

    def guardar_pestana_activa_principal(self, nombre_pestana: str) -> bool:
        nombre_normalizado = (nombre_pestana or "").strip().lower()
        if not nombre_normalizado:
            return False
        return self.iniFile.add_value(
            section=self.section_toggle,
            key=self.key_pestana_activa_principal,
            value=nombre_normalizado,
        )

    def obtener_pestana_activa_principal(self) -> str:
        valor = self.iniFile.get_value(
            section=self.section_toggle,
            key=self.key_pestana_activa_principal,
        )
        return (valor or "").strip().lower()
