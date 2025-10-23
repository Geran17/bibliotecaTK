from dataclasses import dataclass
from typing import Optional


@dataclass
class BibliographyComplementaryDTO:
    """
    DTO para representar información bibliográfica complementaria.

    Esta clase encapsula los datos complementarios de una referencia bibliográfica,
    incluyendo detalles específicos como edición, idioma, volumen y ISBN.

    Attributes:
        id (Optional[int]): Identificador único del registro complementario
        id_bib (int): Identificador de la bibliografía relacionada
        number_edition (int): Número de edición del documento
        language (str): Idioma del documento
        volumen_tomo (str): Volumen o tomo del documento
        number_pagina (int): Número de páginas
        isbn (str): Número ISBN del documento
        created_at (Optional[str]): Fecha y hora de creación del registro
        updated_at (Optional[str]): Fecha y hora de última actualización

    Example:
        >>> biblio_comp = BibliographyComplementaryDTO(
        ...     id_bib=1,
        ...     number_edition=2,
        ...     language="Español",
        ...     volumen_tomo="Tomo I",
        ...     number_pagina=250,
        ...     isbn="978-0-123456-47-2"
        ... )
    """

    id: Optional[int] = None
    id_bib: int
    number_edition: Optional[int] = None
    language: Optional[str] = None
    volumen_tomo: Optional[str] = None
    number_pagina: Optional[int] = None
    isbn: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_insert(self) -> str:
        """Genera una sentencia SQL INSERT para un nuevo registro complementario.

        Utiliza los atributos del DTO para construir una consulta SQL que
        inserta un nuevo registro en la tabla `BibliographyComplementary`.
        Maneja correctamente los valores opcionales que pueden ser nulos.

        Returns:
            str: La sentencia SQL INSERT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` no es nulo.
        """
        if self.id is not None:
            raise ValueError("ID debe ser nulo para una operación de inserción.")
        return f"INSERT INTO BibliographyComplementary(id_bib, number_edition, language, volumen_tomo, number_pagina, isbn)VALUES({self.id_bib}, COALESCE({self.number_edition}, NULL), COALESCE('{self.language}', NULL), COALESCE('{self.volumen_tomo}', NULL), COALESCE({self.number_pagina}, NULL), COALESCE('{self.isbn}', NULL))"

    def to_update_all(self) -> str:
        """Genera una sentencia SQL UPDATE para todos los campos del registro.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyComplementary SET number_edition = COALESCE({self.number_edition}, number_edition), language = COALESCE('{self.language}', language), volumen_tomo = COALESCE('{self.volumen_tomo}', volumen_tomo), number_pagina = COALESCE({self.number_pagina}, number_pagina), isbn = COALESCE('{self.isbn}', isbn) WHERE id = {self.id}"

    def to_update_number_edition(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'number_edition'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyComplementary SET number_edition = {self.number_edition} WHERE id = {self.id}"

    def to_update_language(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'language'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyComplementary SET language = '{self.language}' WHERE id = {self.id}"

    def to_update_volumen_tomo(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'volumen_tomo'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyComplementary SET volumen_tomo = '{self.volumen_tomo}' WHERE id = {self.id}"

    def to_update_number_pagina(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'number_pagina'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyComplementary SET number_pagina = {self.number_pagina} WHERE id = {self.id}"

    def to_update_isbn(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'isbn'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE BibliographyComplementary SET isbn = '{self.isbn}' WHERE id = {self.id}"

    def to_delete(self) -> str:
        """Genera una sentencia SQL DELETE para eliminar un registro.

        Returns:
            str: La sentencia SQL DELETE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de eliminación.")
        return f"DELETE FROM BibliographyComplementary WHERE id = {self.id}"

    def to_instacie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM BibliographyComplementary WHERE id = {self.id}"

    def to_instacie_by_id_bib(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por 'id_bib'.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_bib` es nulo.
        """
        if self.id_bib is None:
            raise ValueError("El ID de bibliografía debe ser proporcionado para buscar.")
        return f"SELECT * FROM BibliographyComplementary WHERE id_bib = {self.id_bib}"

    def to_instacie_by_isbn(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por su ISBN.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `isbn` es nulo.
        """
        if self.isbn is None:
            raise ValueError("No se puede instanciar una referencia bibliográfica por su ISBN.")
        return f"SELECT * FROM BibliographyComplementary WHERE isbn = '{self.isbn}'"

    def to_exist_id_bib(self) -> str:
        """Genera una sentencia SQL SELECT para verificar la existencia de un registro por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_bib` es nulo.
        """
        if self.id_bib is None:
            raise ValueError(
                "No se puede verificar la existencia de un registro por su ID de bibliografía."
            )
        return f"SELECT EXISTS(SELECT count() FROM BibliographyComplementary WHERE id_bib = {self.id_bib})"
