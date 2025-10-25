from dataclasses import dataclass
from typing import Optional


@dataclass
class WordKeyDTO:
    """
    DTO para representar palabras clave de documentos.

    Esta clase encapsula la información necesaria para gestionar las palabras clave
    que permiten categorizar y buscar documentos en la biblioteca según términos
    específicos.

    Attributes:
        id (Optional[int]): Identificador único de la palabra clave
        wordkey (str): Texto de la palabra clave
        description (Optional[str]): Descripción o contexto de la palabra clave
        created_at (Optional[str]): Fecha y hora de creación del registro
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> palabra_clave = WordKeyDTO(
        ...     wordkey="Python",
        ...     description="Lenguaje de programación usado en el proyecto"
        ... )
    """

    id: Optional[int] = None
    wordkey: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_insert(self) -> str:
        """Genera una sentencia SQL INSERT para una nueva palabra clave.

        Returns:
            str: La sentencia SQL INSERT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` no es nulo.
        """
        if self.id is not None:
            raise ValueError("ID debe ser nulo para una operación de inserción.")
        return f"INSERT INTO WordKey(wordkey, description)VALUES('{self.wordkey}', COALESCE('{self.description}', NULL))"

    def to_update_all(self) -> str:
        """Genera una sentencia SQL UPDATE para todos los campos de la palabra clave.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE WordKey SET wordkey = '{self.wordkey}', description = COALESCE('{self.description}', description) WHERE id = {self.id}"

    def to_update_wordkey(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'wordkey'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE WordKey SET wordkey = '{self.wordkey}' WHERE id = {self.id}"

    def to_update_description(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'description'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE WordKey SET description = '{self.description}' WHERE id = {self.id}"

    def to_delete(self) -> str:
        """Genera una sentencia SQL DELETE para eliminar una palabra clave.

        Returns:
            str: La sentencia SQL DELETE para eliminar la palabra clave.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de eliminación.")
        return f"DELETE FROM WordKey WHERE id = {self.id}"

    def to_instacie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar una palabra clave por su ID.

        Returns:
            str: La sentencia SQL SELECT para obtener una palabra clave por su ID.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM WordKey WHERE id = {self.id}"

    def to_instacie_by_wordkey(self) -> str:
        """Genera una sentencia SQL SELECT para buscar una palabra clave por su texto.

        Returns:
            str: La sentencia SQL SELECT para obtener una palabra clave por su texto.

        Raises:
            ValueError: Si el atributo `wordkey` es nulo.
        """
        if self.wordkey is None:
            raise ValueError(
                "El texto de la palabra clave debe ser proporcionado para buscar por texto."
            )
        return f"SELECT * FROM WordKey WHERE wordkey = '{self.wordkey}'"

    def to_exist_wordkey(self) -> str:
        """Genera una sentencia SQL SELECT para verificar la existencia de una palabra clave por su texto.

        Returns:
            str: La sentencia SQL SELECT como cadena de texto.

        Raises:
            ValueError: Si el atributo `wordkey` es nulo.
        """
        if self.wordkey is None:
            raise ValueError(
                "El texto de la palabra clave debe ser proporcionado para verificar la existencia."
            )
        return f"SELECT EXISTS(SELECT count() FROM WordKey WHERE wordkey = '{self.wordkey}')"
