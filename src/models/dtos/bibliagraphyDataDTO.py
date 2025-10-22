from dataclasses import dataclass
from typing import Optional


@dataclass
class BibliographyDataDTO:
    """
    DTO para representar los datos bibliográficos de un documento.

    Esta clase encapsula toda la información bibliográfica básica de un documento,
    incluyendo título, autores, año de publicación y detalles editoriales.

    Attributes:
        id (Optional[int]): Identificador único del registro bibliográfico
        title (str): Título completo del documento
        authors (str): Nombre(s) del(los) autor(es)
        year_publication (int): Año de publicación
        editorial (str): Nombre de la editorial
        place_publication (str): Lugar de publicación (ciudad, país)
        id_doc (int): Identificador del documento asociado
        created_at (Optional[str]): Fecha de creación del registro
        updated_at (Optional[str]): Fecha de última actualización

    Example:
        >>> biblio = BibliographyDataDTO(
        ...     title="Python Programming",
        ...     authors="John Doe",
        ...     year_publication=2023,
        ...     editorial="Tech Books",
        ...     place_publication="New York, USA",
        ...     id_doc=1
        ... )
    """

    id: Optional[int] = None
    title: str
    authors: str
    year_publication: int
    editorial: str
    place_publication: str
    id_doc: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_insert(self) -> str:
        """Genera una sentencia SQL INSERT para un nuevo registro bibliográfico.

        Utiliza los atributos del DTO para construir una consulta SQL que
        inserta un nuevo registro en la tabla `BibliographyData`.

        Returns:
            str: La sentencia SQL INSERT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO no es nulo, ya que
                para una inserción se espera que la base de datos asigne
                el ID.
        """
        if self.id is not None:
            raise ValueError("ID debe ser nulo para una operación de inserción.")
        return f"INSERT INTO BibliographyData(title, authors, year_publication, editorial, place_publication, id_doc)VALUES('{self.title}', '{self.authors}', {self.year_publication}, '{self.editorial}', '{self.place_publication}', {self.id_doc})"

    def to_update_all(self) -> str:
        """Genera una sentencia SQL UPDATE para todos los campos del registro.

        Construye una consulta para actualizar todos los campos modificables de un
        registro existente en la tabla `BibliographyData`, identificado por su ID.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyData SET title = '{self.title}', authors = '{self.authors}', year_publication = {self.year_publication}, editorial = '{self.editorial}', place_publication = '{self.place_publication}' WHERE id = {self.id}"

    def to_update_title(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'title'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyData SET title = '{self.title}' WHERE id = {self.id}"

    def to_update_authors(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'authors'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyData SET authors = '{self.authors}' WHERE id = {self.id}"

    def to_update_editorial(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'editorial'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyData SET editorial = '{self.editorial}' WHERE id = {self.id}"

    def to_update_place_publication(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'place_publication'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyData SET place_publication = '{self.place_publication}' WHERE id = {self.id}"

    def to_update_year_publication(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'year_publication'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyData SET year_publication = {self.year_publication} WHERE id = {self.id}"

    def to_delete(self) -> str:
        """Genera una sentencia SQL DELETE para eliminar un registro.

        Returns:
            str: La sentencia SQL DELETE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de eliminación.")
        return f"DELETE FROM BibliographyData WHERE id = {self.id}"

    def to_instacie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` del DTO es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM BibliographyData WHERE id = {self.id}"

    def to_instacie_by_id_doc(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por 'id_doc'.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_doc` del DTO es nulo.
        """
        if self.id_doc is None:
            raise ValueError("El ID de documento debe ser proporcionado para buscar.")
        return f"SELECT * FROM BibliographyData WHERE id_doc = {self.id_doc}"
