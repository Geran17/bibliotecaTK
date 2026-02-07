import csv
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from models.daos.capitulo_dao import CapituloDAO
from models.daos.seccion_dao import SeccionDAO
from models.entities.capitulo import Capitulo
from models.entities.seccion import Seccion

logger = logging.getLogger(__name__)


class ControlarImportacionCSV:
    """Controlador para importar capítulos y secciones desde archivos CSV.

    Maneja la importación masiva de capítulos y secciones desde archivos CSV,
    con validación de datos y manejo de errores.
    """

    def __init__(self, ruta_db: Optional[str] = None):
        """
        Inicializa el controlador de importación CSV.

        Args:
            ruta_db: Ruta opcional a la base de datos.
        """
        self.capitulo_dao = CapituloDAO(ruta_db)
        self.seccion_dao = SeccionDAO(ruta_db)
        self.ruta_db = ruta_db
        self.errores: List[str] = []
        self.registros_importados = 0

    def importar_capitulos_csv(self, ruta_archivo: str, id_documento: int) -> Tuple[int, List[str]]:
        """
        Importa capítulos desde un archivo CSV.

        El archivo CSV debe tener las siguientes columnas:
        - numero_capitulo (requerido): Número del capítulo
        - titulo (requerido): Título del capítulo
        - pagina_inicio (opcional): Página de inicio

        Args:
            ruta_archivo: Ruta al archivo CSV
            id_documento: ID del documento a asociar los capítulos

        Returns:
            Tupla con (número de registros importados, lista de errores)
        """
        self.errores = []
        self.registros_importados = 0

        try:
            ruta_path = Path(ruta_archivo)
            if not ruta_path.exists():
                raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")

            if not ruta_path.suffix.lower() == '.csv':
                raise ValueError("El archivo debe ser un CSV válido")

            with open(ruta_path, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)

                if not lector.fieldnames:
                    raise ValueError("El archivo CSV está vacío")

                campos_requeridos = {'numero_capitulo', 'titulo'}
                if not campos_requeridos.issubset(set(lector.fieldnames)):
                    raise ValueError(
                        f"El CSV debe contener las columnas: {', '.join(campos_requeridos)}"
                    )

                for num_fila, fila in enumerate(
                    lector, start=2
                ):  # start=2 porque la fila 1 es encabezado
                    try:
                        numero_capitulo = fila.get('numero_capitulo', '').strip()
                        titulo = fila.get('titulo', '').strip()
                        pagina_inicio = fila.get('pagina_inicio', '').strip()

                        # Validar campos requeridos
                        if not numero_capitulo:
                            self.errores.append(f"Fila {num_fila}: numero_capitulo está vacío")
                            continue

                        if not titulo:
                            self.errores.append(f"Fila {num_fila}: titulo está vacío")
                            continue

                        # Convertir tipos de datos
                        try:
                            numero_capitulo = int(numero_capitulo)
                        except ValueError:
                            self.errores.append(
                                f"Fila {num_fila}: numero_capitulo debe ser un número entero"
                            )
                            continue

                        pagina_inicio_int = None
                        if pagina_inicio:
                            try:
                                pagina_inicio_int = int(pagina_inicio)
                            except ValueError:
                                self.errores.append(
                                    f"Fila {num_fila}: pagina_inicio debe ser un número entero"
                                )
                                continue

                        # Crear y guardar capítulo
                        capitulo = Capitulo(
                            id_documento=id_documento,
                            numero_capitulo=numero_capitulo,
                            titulo=titulo,
                            pagina_inicio=pagina_inicio_int,
                            ruta_db=self.ruta_db,
                        )

                        # Insertar en base de datos
                        sql = """
                        INSERT INTO capitulo (id_documento, numero_capitulo, titulo, pagina_inicio)
                        VALUES (?, ?, ?, ?)
                        """
                        params = (id_documento, numero_capitulo, titulo, pagina_inicio_int)
                        self.capitulo_dao.insertar(sql, params)
                        self.registros_importados += 1

                        logger.info(f"Capítulo importado: {titulo} (Fila {num_fila})")

                    except Exception as e:
                        self.errores.append(f"Fila {num_fila}: {str(e)}")
                        logger.error(f"Error en fila {num_fila}: {str(e)}")
                        continue

            logger.info(f"Importación completada: {self.registros_importados} capítulos importados")

        except FileNotFoundError as e:
            self.errores.append(f"Error: {str(e)}")
            logger.error(f"Archivo no encontrado: {e}")
        except ValueError as e:
            self.errores.append(f"Error de validación: {str(e)}")
            logger.error(f"Error de validación: {e}")
        except Exception as e:
            self.errores.append(f"Error inesperado: {str(e)}")
            logger.error(f"Error inesperado: {e}")

        return self.registros_importados, self.errores

    def importar_secciones_csv(self, ruta_archivo: str, id_capitulo: int) -> Tuple[int, List[str]]:
        """
        Importa secciones desde un archivo CSV.

        El archivo CSV debe tener las siguientes columnas:
        - titulo (requerido): Título de la sección
        - nivel (opcional): Nivel jerárquico de la sección
        - numero_pagina (opcional): Número de página
        - id_padre (opcional): ID de la sección padre

        Args:
            ruta_archivo: Ruta al archivo CSV
            id_capitulo: ID del capítulo a asociar las secciones

        Returns:
            Tupla con (número de registros importados, lista de errores)
        """
        self.errores = []
        self.registros_importados = 0

        try:
            ruta_path = Path(ruta_archivo)
            if not ruta_path.exists():
                raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")

            if not ruta_path.suffix.lower() == '.csv':
                raise ValueError("El archivo debe ser un CSV válido")

            with open(ruta_path, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)

                if not lector.fieldnames:
                    raise ValueError("El archivo CSV está vacío")

                campos_requeridos = {'titulo'}
                if not campos_requeridos.issubset(set(lector.fieldnames)):
                    raise ValueError(f"El CSV debe contener al menos la columna: titulo")

                # Diccionario temporal para mapear títulos con IDs insertados
                titulos_a_ids: Dict[str, int] = {}

                for num_fila, fila in enumerate(lector, start=2):
                    try:
                        titulo = fila.get('titulo', '').strip()
                        nivel = fila.get('nivel', '').strip() or None
                        numero_pagina = fila.get('numero_pagina', '').strip()
                        id_padre_str = fila.get('id_padre', '').strip()

                        # Validar campo requerido
                        if not titulo:
                            self.errores.append(f"Fila {num_fila}: titulo está vacío")
                            continue

                        # Convertir tipos de datos
                        numero_pagina_int = None
                        if numero_pagina:
                            try:
                                numero_pagina_int = int(numero_pagina)
                            except ValueError:
                                self.errores.append(
                                    f"Fila {num_fila}: numero_pagina debe ser un número entero"
                                )
                                continue

                        # Procesar id_padre
                        id_padre = None
                        if id_padre_str:
                            # Si es un número, usarlo directamente
                            if id_padre_str.isdigit():
                                id_padre = int(id_padre_str)
                            else:
                                # Si es un título, buscarlo en el diccionario
                                id_padre = titulos_a_ids.get(id_padre_str)
                                if not id_padre:
                                    self.errores.append(
                                        f"Fila {num_fila}: Sección padre '{id_padre_str}' no encontrada"
                                    )
                                    continue

                        # Crear y guardar sección
                        sql = """
                        INSERT INTO seccion (id_capitulo, titulo, nivel, id_padre, numero_pagina)
                        VALUES (?, ?, ?, ?, ?)
                        """
                        params = (id_capitulo, titulo, nivel, id_padre, numero_pagina_int)
                        id_insertado = self.seccion_dao.insertar(sql, params)

                        # Guardar mapeo de título a ID
                        if id_insertado:
                            titulos_a_ids[titulo] = id_insertado

                        self.registros_importados += 1
                        logger.info(f"Sección importada: {titulo} (Fila {num_fila})")

                    except Exception as e:
                        self.errores.append(f"Fila {num_fila}: {str(e)}")
                        logger.error(f"Error en fila {num_fila}: {str(e)}")
                        continue

            logger.info(f"Importación completada: {self.registros_importados} secciones importadas")

        except FileNotFoundError as e:
            self.errores.append(f"Error: {str(e)}")
            logger.error(f"Archivo no encontrado: {e}")
        except ValueError as e:
            self.errores.append(f"Error de validación: {str(e)}")
            logger.error(f"Error de validación: {e}")
        except Exception as e:
            self.errores.append(f"Error inesperado: {str(e)}")
            logger.error(f"Error inesperado: {e}")

        return self.registros_importados, self.errores

    def obtener_errores(self) -> List[str]:
        """Retorna la lista de errores de la última importación."""
        return self.errores

    def limpiar_errores(self) -> None:
        """Limpia la lista de errores."""
        self.errores = []
