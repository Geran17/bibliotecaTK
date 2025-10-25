from dataclasses import dataclass
from typing import Optional


@dataclass
class ChapterDTO:
    id: Optional[int] = None
    id_doc: int
    number_chapter: int
    title: str
    page_start: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_insert(self) -> str:
        """Genera una sentencia SQL INSERT para una nueva etiqueta.

        Returns:
            str: La sentencia SQL INSERT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` no es nulo.
        """
        if self.id is not None:
            raise ValueError("ID debe ser nulo para una operación de inserción.")
        return f"INSERT INTO Chapter (id_doc, number_chapter, title, page_start)VALUES({self.id_doc}, {self.number_chapter}, '{self.title}', {self.page_start})"

    def to_update_all(self) -> str:
        """Genera una sentencia SQL UPDATE para todos los campos de la etiqueta.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Chapter SET id_doc = {self.id_doc}, number_chapter = {self.number_chapter}, title = '{self.title}', page_start = {self.page_start} WHERE id = {self.id}"

    def to_update_id_doc(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo id_doc.

        Returns:
            str: La sentencia SQL UPDATE como una cadena texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Chapter SET id_doc = {self.id_doc} WHERE id = {self.id}"

    def to_update_number_chapter(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo number_chapter.

        Returns:
            str: La sentencia SQL UPDATE como una cadena texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Chapter SET number_chapter = {self.number_chapter} WHERE id = {self.id}"

    def to_update_title(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo title.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Chapter SET title = '{self.title}' WHERE id = {self.id}"

    def to_update_page_start(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo page_start

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Chapter SET page_start = {self.page_start} WHERE id = {self.id}"

    def to_delete(self) -> str:
        """Genera una sentencia SQL DELETE para eliminar un registro.

        Returns:
            str: La sentencia SQL DELETE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de eliminación.")
        return f"DELETE FROM Chapter WHERE id = {self.id}"

    def to_instacie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM Chapter WHERE id = {self.id}"

    def to_instacie_by_id_doc(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por su ID de documento.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_doc` es nulo.
        """
        if self.id_doc is None:
            raise ValueError("El ID de documento debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM Chapter WHERE id_doc = {self.id_doc}"

    def to_exist_id_doc_title(self) -> str:
        """Genera una sentencia SQL SELECT para verificar la existencia de un registro por su ID de documento y título.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_doc` o `title` es nulo.
        """
        if self.id_doc is None or self.title is None:
            raise ValueError(
                "El ID de documento y el título deben ser proporcionados para verificar la existencia."
            )
        return f"SELECT EXISTS(SELECT count() FROM Chapter WHERE id_doc = {self.id_doc} AND title = '{self.title}')"
