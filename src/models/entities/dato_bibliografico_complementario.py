from typing import Optional
from src.models.dtos.dato_bibliografico_complementario_dto import (
    DatoBibliograficoComplementarioDTO,
)
from src.models.daos.dato_bibliografico_complementario_dao import (
    DatoBibliograficoComplementarioDAO,
)


class DatoBibliograficoComplementario(DatoBibliograficoComplementarioDTO):
    """
    Clase de entidad para los datos bibliográficos complementarios.

    Hereda de `DatoBibliograficoComplementarioDTO` y añade la lógica de negocio
    para interactuar con la base de datos a través de su DAO.

    Attributes:
        _dao (DatoBibliograficoComplementarioDAO): Instancia del DAO.
    """

    def __init__(
        self,
        id_dato_bibliografico: int,
        id: Optional[int] = None,
        numero_edicion: Optional[int] = None,
        idioma: Optional[str] = None,
        volumen_tomo: Optional[str] = None,
        numero_paginas: Optional[int] = None,
        isbn: Optional[str] = None,
        creado_en: Optional[str] = None,
        actualizado_en: Optional[str] = None,
        ruta_db: Optional[str] = None,
    ):
        """
        Inicializa una instancia de la entidad DatoBibliograficoComplementario.

        Args:
            id_dato_bibliografico (int): ID del dato bibliográfico principal.
            id (Optional[int]): ID del registro en la base de datos.
            numero_edicion (Optional[int]): Número de edición.
            idioma (Optional[str]): Idioma del documento.
            volumen_tomo (Optional[str]): Volumen o tomo.
            numero_paginas (Optional[int]): Número de páginas.
            isbn (Optional[str]): Código ISBN.
            creado_en (Optional[str]): Fecha de creación.
            actualizado_en (Optional[str]): Fecha de última actualización.
            ruta_db (Optional[str]): Ruta opcional a la base de datos para el DAO.
        """
        super().__init__(
            id_dato_bibliografico=id_dato_bibliografico,
            id=id,
            numero_edicion=numero_edicion,
            idioma=idioma,
            volumen_tomo=volumen_tomo,
            numero_paginas=numero_paginas,
            isbn=isbn,
        )
        # Asignar campos no inicializados en el DTO
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

        self._dao = DatoBibliograficoComplementarioDAO(ruta_db=ruta_db)

    def insertar(self) -> Optional[int]:
        """
        Guarda el estado actual del objeto como un nuevo registro en la base de datos.

        Returns:
            Optional[int]: El ID del nuevo registro insertado, o None si falla.
        """
        params = (
            self.id_dato_bibliografico,
            self.numero_edicion,
            self.idioma,
            self.volumen_tomo,
            self.numero_paginas,
            self.isbn,
        )
        return self._dao.insertar(params=params)

    def actualizar(self) -> bool:
        """
        Actualiza el registro en la base de datos con el estado actual del objeto.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        params = (
            self.id_dato_bibliografico,
            self.numero_edicion,
            self.idioma,
            self.volumen_tomo,
            self.numero_paginas,
            self.isbn,
            self.id,
        )
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
        self.id_dato_bibliografico = data["id_dato_bibliografico"]
        self.numero_edicion = data["numero_edicion"]
        self.idioma = data["idioma"]
        self.volumen_tomo = data["volumen_tomo"]
        self.numero_paginas = data["numero_paginas"]
        self.isbn = data["isbn"]
        self.creado_en = data["creado_en"]
        self.actualizado_en = data["actualizado_en"]
        return True

    def existe(self) -> bool:
        """
        Verifica si ya existen datos complementarios para el dato bibliográfico asociado.

        Returns:
            bool: True si los datos existen, False en caso contrario.
        """
        params = (self.id_dato_bibliografico,)
        return self._dao.existe(params=params)
