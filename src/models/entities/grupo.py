from typing import Optional
from models.dtos.grupo_dto import GrupoDTO
from models.daos.grupo_dao import GrupoDAO


class Grupo(GrupoDTO):
    """
    Clase de entidad que representa un Grupo.

    Hereda la estructura de datos de `GrupoDTO` y añade la lógica de negocio
    para interactuar con la base de datos a través de `GrupoDAO`.

    Esta clase permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    de una manera orientada a objetos.

    Attributes:
        _dao (GrupoDAO): Instancia del Data Access Object para grupos.
    """

    def __init__(
        self,
        nombre: str,
        id: Optional[int] = None,
        descripcion: Optional[str] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad Grupo.

        Args:
            nombre (str): Nombre del grupo.
            id (Optional[int]): ID del grupo en la base de datos.
            descripcion (Optional[str]): Descripción del grupo.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            nombre=nombre,
            id=id,
            descripcion=descripcion,
        )
        # Los campos `creado_en` y `actualizado_en` no se inicializan desde el constructor
        # del DTO, por lo que se asignan aquí si es necesario.
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en
        self._dao = GrupoDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (self.nombre, self.descripcion)
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Utiliza el `id` del objeto para encontrar el registro a actualizar.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (self.nombre, self.descripcion, self.id)
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

        self.nombre = lista[0]["nombre"]
        self.descripcion = lista[0]["descripcion"]
        self.creado_en = lista[0]["creado_en"]
        self.actualizado_en = lista[0]["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe un grupo con el mismo nombre en la base de datos.

        Returns:
            bool: True si el grupo existe, False en caso contrario.
        """
        params = (self.nombre,)
        return self._dao.existe(params=params)
