from typing import Optional
from models.dtos.etiqueta_dto import EtiquetaDTO
from models.daos.etiqueta_dao import EtiquetaDAO


class Etiqueta(EtiquetaDTO):
    """
    Clase de entidad que representa una Etiqueta.

    Hereda de `EtiquetaDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `EtiquetaDAO`.

    Attributes:
        _dao (EtiquetaDAO): Instancia del DAO para etiquetas.
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
        Inicializa una instancia de la entidad Etiqueta.

        Args:
            nombre (str): Nombre de la etiqueta.
            id (Optional[int]): ID de la etiqueta en la base de datos.
            descripcion (Optional[str]): Descripción de la etiqueta.
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

        self._dao = EtiquetaDAO(ruta_db=ruta_db)
        # creamos la tabla
        self._dao.crear_tabla()

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

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (self.nombre, self.descripcion, self.id)
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
        self.descripcion = data["descripcion"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe una etiqueta con el mismo nombre.

        Returns:
            bool: True si la etiqueta existe, False en caso contrario.
        """
        params = (self.nombre,)
        return self._dao.existe(params=params)
