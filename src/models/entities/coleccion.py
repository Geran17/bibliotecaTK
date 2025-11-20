from typing import Optional, List
from models.dtos.coleccion_dto import ColeccionDTO
from models.daos.coleccion_dao import ColeccionDAO


class Coleccion(ColeccionDTO):
    """
    Clase de entidad que representa una Coleccion.

    Hereda de `ColeccionDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `ColeccionDAO`.

    Attributes:
        _dao (ColeccionDAO): Instancia del DAO para colecciones.
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
        Inicializa una instancia de la entidad Coleccion.

        Args:
            nombre (str): Nombre de la colección.
            id (Optional[int]): ID de la colección en la base de datos.
            descripcion (Optional[str]): Descripción de la colección.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            nombre=nombre,
            id=id,
            descripcion=descripcion,
        )
        # Asignar campos no inicializados en el DTO
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

        self._dao = ColeccionDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        return self._dao.insertar(data=self)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        return self._dao.actualizar(
            id_coleccion=self.id, nombre=self.nombre, descripcion=self.descripcion
        )

    def eliminar(self) -> bool:
        """
        Elimina el registro correspondiente de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        return self._dao.eliminar(id_coleccion=self.id)

    def instanciar(self) -> bool:
        """
        Carga los datos desde la base de datos y los asigna a los atributos del objeto.

        Utiliza el `id` del objeto para buscar el registro.

        Returns:
            bool: True si el registro se encontró y el objeto se actualizó, False en caso contrario.
        """
        params = (self.id,)
        lista = self._dao.instanciar(params=params)
        if not lista:
            return False

        data = lista[0]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data.get("actualizado_en")
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe una colección con el mismo nombre.

        Returns:
            bool: True si la colección existe, False en caso contrario.
        """
        return self._dao.existe(nombre=self.nombre)
