from typing import Optional
from src.models.dtos.seccion_dto import SeccionDTO
from src.models.daos.seccion_dao import SeccionDAO


class Seccion(SeccionDTO):
    """
    Clase de entidad que representa una Sección de un capítulo.

    Hereda la estructura de datos de `SeccionDTO` y añade la lógica de negocio
    para interactuar con la base de datos a través de `SeccionDAO`.

    Esta clase permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    de una manera orientada a objetos.

    Attributes:
        _dao (SeccionDAO): Instancia del Data Access Object para secciones.
    """

    def __init__(
        self,
        id_capitulo: int,
        titulo: str,
        id: Optional[int] = None,
        nivel: Optional[str] = None,
        id_padre: Optional[int] = None,
        numero_pagina: Optional[int] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad Seccion.

        Args:
            id_capitulo (int): ID del capítulo al que pertenece.
            titulo (str): Título de la sección.
            id (Optional[int]): ID de la sección en la base de datos.
            nivel (Optional[str]): Nivel jerárquico (e.g., '1.1').
            id_padre (Optional[int]): ID de la sección padre.
            numero_pagina (Optional[int]): Página donde comienza la sección.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_capitulo=id_capitulo,
            titulo=titulo,
            id=id,
            nivel=nivel,
            id_padre=id_padre,
            numero_pagina=numero_pagina,
            creado_en=creado_en,
            actualizado_en=actualizado_en,
        )
        self._dao = SeccionDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (self.id_capitulo, self.titulo, self.nivel, self.id_padre, self.numero_pagina)
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Utiliza el `id` del objeto para encontrar el registro a actualizar.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (
            self.id_capitulo,
            self.titulo,
            self.nivel,
            self.id_padre,
            self.numero_pagina,
            self.id,
        )
        return self._dao.actualizar_todo(params=params)

    def eliminar(self) -> bool:
        """
        Elimina el registro correspondiente de la base de datos.

        Utiliza el `id` del objeto para encontrar el registro a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id,)
        return self._dao.eliminar(params=params)

    def instanciar(self) -> bool:
        """
        Carga los datos desde la base de datos y los asigna a los atributos del objeto.

        Utiliza el `id` del objeto para buscar el registro. Si se encuentra,
        actualiza los atributos del objeto con los valores de la base de datos.

        Returns:
            bool: True si el registro se encontró y el objeto se actualizó,
                  False en caso contrario.
        """
        params = (self.id,)
        lista = self._dao.instanciar(params=params)
        if not lista:
            return False

        data = lista[0]
        self.id_capitulo = data["id_capitulo"]
        self.titulo = data["titulo"]
        self.nivel = data["nivel"]
        self.id_padre = data["id_padre"]
        self.numero_pagina = data["numero_pagina"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe una sección con el mismo título para el mismo capítulo.

        Returns:
            bool: True si la sección existe, False en caso contrario.
        """
        params = (self.id_capitulo, self.titulo)
        return self._dao.existe(params=params)
