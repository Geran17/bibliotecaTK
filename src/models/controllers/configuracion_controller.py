from os import mkdir
from os.path import join, isdir
from utilities.fileINI import FileINI
from utilities.configuracion import CONFIG_INI
from pathlib import Path


class ConfiguracionController:
    def __init__(self):
        self.nombre_biblioteca = "BibliotecaTK"
        self.iniFile = FileINI(pathINI=CONFIG_INI)
        # ----- Seciones ----
        self.section_ubiaciones = "ubicaciones"
        self.section_estilo = "estilo"
        self.section_toggle = "toggle"
        self.section_ubicaciones = "ubicaciones"
        # ----- Keys --------
        self.key_ubicacion_biblioteca = "ubicacion_biblioteca"
        self.key_tema = "tema"
        self.key_panel_laterial = "panel_lateral"
        self.key_panel_archivo = "panel_archivo"
        self.key_ultima_ubicacion = "ultima_ubicacion"
        self.key_copiar_ubicacion = "copiar_ubicacion"
        self.key_mover_ubicacion = "mover_ubicacion"

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
                    mkdir(join(directrio, self.nombre_biblioteca))
                    # si el directorio se crea con existo, establcemos en el archivo de configuraciones
                    isValue = self.iniFile.add_value(
                        section=self.section_ubiaciones,
                        key=self.key_ubicacion_biblioteca,
                        value=join(directrio, self.nombre_biblioteca),
                    )
                    return isValue
                except Exception as e:
                    print(
                        f"No se pudo crear el directorio, para la biblioteca: {join(directrio, self.nombre_biblioteca)}"
                    )
                    return False
            elif folder.name == self.nombre_biblioteca:
                isValue = self.iniFile.add_value(
                    section=self.section_ubiaciones,
                    key=self.key_ubicacion_biblioteca,
                    value=directrio,
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

    def obtener_ubicacion_biblioteca(self) -> str:
        ubicacion_biblioteca = self.iniFile.get_value(
            section=self.section_ubiaciones, key=self.key_ubicacion_biblioteca
        )
        return ubicacion_biblioteca

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
