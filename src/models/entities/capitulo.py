from typing import Optional
from models.dtos.capitulo_dto import CapituloDTO
from models.daos.capitulo_dao import CapituloDAO


class Capitulo(CapituloDTO):
    """
    Clase de entidad que representa un Capítulo de un documento.

    Hereda la estructura de datos de `CapituloDTO` y añade la lógica de negocio
    para interactuar con la base de datos a través de `CapituloDAO`.

    Esta clase permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    de una manera orientada a objetos.

    Attributes:
        _dao (CapituloDAO): Instancia del Data Access Object para capítulos.
    """

    def __init__(
        self,
        id_documento: int,
        numero_capitulo: int,
        titulo: str,
        id: Optional[int] = None,
        pagina_inicio: Optional[int] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad Capitulo.

        Args:
            id_documento (int): ID del documento al que pertenece.
            numero_capitulo (int): Número de orden del capítulo.
            titulo (str): Título del capítulo.
            id (Optional[int]): ID del capítulo en la base de datos.
            pagina_inicio (Optional[int]): Página donde comienza el capítulo.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            numero_capitulo=numero_capitulo,
            titulo=titulo,
            id=id,
            pagina_inicio=pagina_inicio,
            creado_en=creado_en,
            actualizado_en=actualizado_en,
        )
        self._dao = CapituloDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (self.id_documento, self.numero_capitulo, self.titulo, self.pagina_inicio)
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Utiliza el `id` del objeto para encontrar el registro a actualizar.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (self.id_documento, self.numero_capitulo, self.titulo, self.pagina_inicio, self.id)
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
        self.id_documento = data["id_documento"]
        self.numero_capitulo = data["numero_capitulo"]
        self.titulo = data["titulo"]
        self.pagina_inicio = data["pagina_inicio"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existe un capítulo con el mismo número para el mismo documento.

        Returns:
            bool: True si el capítulo existe, False en caso contrario.
        """
        params = (self.id_documento, self.numero_capitulo)
        return self._dao.existe(params=params)
