from typing import Optional
from models.dtos.categoria_dto import CategoriaDTO
from models.daos.categoria_dao import CategoriaDAO


class Categoria(CategoriaDTO):
    """
    Clase de entidad que representa una Categoria.

    Hereda de `CategoriaDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `CategoriaDAO`.

    Attributes:
        _dao (CategoriaDAO): Instancia del DAO para categorías.
    """

    def __init__(
        self,
        nombre: str,
        id: Optional[int] = None,
        id_padre: Optional[int] = None,
        descripcion: Optional[str] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad Categoria.

        Args:
            nombre (str): Nombre de la categoría.
            id (Optional[int]): ID de la categoría en la base de datos.
            id_padre (Optional[int]): ID de la categoría padre.
            descripcion (Optional[str]): Descripción de la categoría.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            nombre=nombre,
            id=id,
            id_padre=id_padre,
            descripcion=descripcion,
        )
        # Asignar campos no inicializados en el DTO
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

        self._dao = CategoriaDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (self.nombre, self.id_padre, self.descripcion)
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (self.nombre, self.id_padre, self.descripcion, self.id)
        return self._dao.actualizar_todo(params=params)

    def eliminar(self) -> bool:
        """
        Elimina el registro correspondiente de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        params = (self.id,)
        return self._dao.eliminar(params=params)

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
        self.id_padre = data["id_padre"]
        self.descripcion = data["descripcion"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe una categoría con el mismo nombre.

        Returns:
            bool: True si la categoría existe, False en caso contrario.
        """
        params = (self.nombre,)
        return self._dao.existe(params=params)
