from typing import Optional
from models.dtos.metadato_dto import MetadatoDTO
from models.daos.metadato_dao import MetadatoDAO


class Metadato(MetadatoDTO):
    """
    Clase de entidad que representa un Metadato de un documento.

    Hereda de `MetadatoDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `MetadatoDAO`.

    Attributes:
        _dao (MetadatoDAO): Instancia del DAO para metadatos.
    """

    def __init__(
        self,
        id_documento: int,
        clave: str,
        valor: str,
        id: Optional[int] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad Metadato.

        Args:
            id_documento (int): ID del documento al que pertenece.
            clave (str): La clave del metadato.
            valor (str): El valor del metadato.
            id (Optional[int]): ID del metadato en la base de datos.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            clave=clave,
            valor=valor,
            id=id,
        )
        # Asignar campos no inicializados en el DTO
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

        self._dao = MetadatoDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (self.id_documento, self.clave, self.valor)
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (self.id_documento, self.clave, self.valor, self.id)
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
        self.id_documento = data["id_documento"]
        self.clave = data["clave"]
        self.valor = data["valor"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe un metadato con la misma clave para el mismo documento.

        Returns:
            bool: True si el metadato existe, False en caso contrario.
        """
        params = (self.id_documento, self.clave)
        return self._dao.existe(params=params)
