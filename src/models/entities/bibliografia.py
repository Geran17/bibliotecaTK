from typing import Optional
from models.dtos.bibliografia_dto import BibliografiaDTO
from models.daos.bibliografia_dao import BibliografiaDAO


class Bibliografia(BibliografiaDTO):
    """
    Clase de entidad que representa los datos bibliográficos de un documento.

    Hereda de `BibliografiaDTO` y añade la lógica de negocio para interactuar
    con la base de datos a través de `BibliografiaDAO`.

    Attributes:
        _dao (BibliografiaDAO): Instancia del DAO para datos bibliográficos.
    """

    def __init__(
        self,
        id_documento: int,
        titulo: str,
        id: Optional[int] = None,
        autores: Optional[str] = None,
        ano_publicacion: Optional[int] = None,
        editorial: Optional[str] = None,
        lugar_publicacion: Optional[str] = None,
        numero_edicion: Optional[str] = None,
        idioma: Optional[str] = None,
        volumen_tomo: Optional[str] = None,
        numero_paginas: Optional[int] = None,
        isbn: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad DatoBibliografico.

        Args:
            titulo (str): Título del documento.
            id_documento (int): ID del documento asociado.
            id (Optional[int]): ID del registro en la base de datos.
            autores (Optional[str]): Autores del documento.
            ano_publicacion (Optional[int]): Año de publicación.
            editorial (Optional[str]): Editorial del documento.
            lugar_publicacion (Optional[str]): Lugar de publicación.
            numero_edicion (Optional[str]): Número de edición.
            idioma (Optional[str]): Idioma del documento.
            volumen_tomo (Optional[str]): Volumen o tomo.
            numero_paginas (Optional[int]): Cantidad de páginas.
            isbn (Optional[str]): ISBN del documento.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_documento=id_documento,
            titulo=titulo,
            id=id,
            autores=autores,
            ano_publicacion=ano_publicacion,
            editorial=editorial,
            lugar_publicacion=lugar_publicacion,
            numero_edicion=numero_edicion,
            idioma=idioma,
            volumen_tomo=volumen_tomo,
            numero_paginas=numero_paginas,
            isbn=isbn,
        )

        self._dao = BibliografiaDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (
            self.titulo,
            self.autores,
            self.ano_publicacion,
            self.editorial,
            self.lugar_publicacion,
            self.numero_edicion,
            self.idioma,
            self.volumen_tomo,
            self.numero_paginas,
            self.isbn,
            self.id_documento,
        )
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (
            self.titulo,
            self.autores,
            self.ano_publicacion,
            self.editorial,
            self.lugar_publicacion,
            self.numero_edicion,
            self.idioma,
            self.volumen_tomo,
            self.numero_paginas,
            self.isbn,
            self.id_documento,  # Usado en el WHERE
        )
        return self._dao.actualizar(params=params)

    def eliminar(self) -> bool:
        """
        Elimina el registro correspondiente de la base de datos.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        return self._dao.eliminar(id_documento=self.id_documento)

    def instanciar(self) -> bool:
        """
        Carga los datos desde la base de datos y los asigna a los atributos del objeto.

        Utiliza el `id_documento` del objeto para buscar el registro.

        Returns:
            bool: True si el registro se encontró y el objeto se actualizó, False en caso contrario.
        """
        params = (self.id_documento,)
        lista = self._dao.instanciar(params=params)
        if not lista:
            return False

        data = lista[0]
        self.id = data["id"]
        self.titulo = data["titulo"]
        self.autores = data["autores"]
        self.ano_publicacion = data["ano_publicacion"]
        self.editorial = data["editorial"]
        self.lugar_publicacion = data["lugar_publicacion"]
        self.numero_edicion = data["numero_edicion"]
        self.idioma = data["idioma"]
        self.volumen_tomo = data["volumen_tomo"]
        self.numero_paginas = data["numero_paginas"]
        self.isbn = data["isbn"]
        self.id_documento = data["id_documento"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existen datos bibliográficos para el documento asociado.

        Returns:
            bool: True si los datos existen, False en caso contrario.
        """
        params = (self.id_documento,)
        return self._dao.existe(params=params)
