from typing import Optional
from models.dtos.documento_dto import DocumentoDTO
from models.daos.documento_dao import DocumentoDAO


class Documento(DocumentoDTO):
    """
    Clase de entidad que representa un Documento.

    Hereda la estructura de datos de `DocumentoDTO` y añade la lógica de negocio
    para interactuar con la base de datos a través de `DocumentoDAO`.

    Esta clase permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    de una manera orientada a objetos.

    Attributes:
        _dao (DocumentoDAO): Instancia del Data Access Object para documentos.
    """

    def __init__(
        self,
        nombre: str,
        extension: str,
        hash: str,
        tamano: int,
        id: Optional[int] = None,
        esta_activo: bool = True,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad Documento.

        Args:
            nombre (str): Nombre del documento.
            extension (str): Extensión del archivo.
            hash (str): Hash único del archivo.
            tamano (int): Tamaño del archivo en bytes.
            id (Optional[int]): ID del documento en la base de datos.
            esta_activo (bool): Estado del documento.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            nombre=nombre,
            extension=extension,
            hash=hash,
            tamano=tamano,
            id=id,
            esta_activo=esta_activo,
            creado_en=creado_en,
            actualizado_en=actualizado_en,
        )
        self._dao = DocumentoDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (self.nombre, self.extension, self.hash, self.tamano, self.esta_activo)
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Utiliza el `id` del objeto para encontrar el registro a actualizar.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (self.nombre, self.extension, self.hash, self.tamano, self.esta_activo, self.id)
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
        self.extension = lista[0]["extension"]
        self.hash = lista[0]["hash"]
        self.actualizado_en = lista[0]['actualizado_en']
        self.creado_en = lista[0]['creado_en']
        self.tamano = lista[0]["tamano"]
        self.esta_activo = bool(lista[0]["esta_activo"])
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe un documento con el mismo hash en la base de datos.

        Returns:
            bool: True si el documento existe, False en caso contrario.
        """
        params = (self.hash,)
        return self._dao.existe(params=params)
