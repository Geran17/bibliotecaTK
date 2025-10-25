from dataclasses import dataclass
from typing import Optional


@dataclass
class TagDTO:
    """
    DTO para representar etiquetas de documentos.

    Esta clase encapsula la información necesaria para gestionar las etiquetas
    que permiten clasificar y organizar los documentos según criterios
    definidos por el usuario.

    Attributes:
        id (Optional[int]): Identificador único de la etiqueta
        name (str): Nombre descriptivo de la etiqueta
        description (Optional[str]): Descripción detallada de la etiqueta
        created_at (Optional[str]): Fecha y hora de creación del registro
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> etiqueta = TagDTO(
        ...     name="Importante",
        ...     description="Documentos marcados como importantes"
        ... )
    """

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
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
        return f"INSERT INTO Tag(name, description)VALUES('{self.name}', COALESCE('{self.description}', NULL))"

    def to_update_all(self) -> str:
        """Genera una sentencia SQL UPDATE para todos los campos de la etiqueta.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Tag SET name = '{self.name}', description = COALESCE('{self.description}', description) WHERE id = {self.id}"

    def to_update_name(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'name'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.name is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Tag SET name = '{self.name}' WHERE id = {self.id}"

    def to_update_description(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'description'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.description is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Tag SET description = '{self.description}' WHERE id = {self.id}"

    def to_delete(self) -> str:
        """Genera una sentencia SQL DELETE para eliminar una etiqueta.

        Returns:
            str: La sentencia SQL DELETE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de eliminación.")
        return f"DELETE FROM Tag WHERE id = {self.id}"

    def to_instacie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar una etiqueta por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM Tag WHERE id = {self.id}"

    def to_instacie_by_name(self) -> str:
        """Gnera una sentencia SQL SELECT para buscar una etiqueta por su nombre.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `name` es nulo.
        """
        if self.name is None:
            raise ValueError("El nombre debe ser proporcionado para buscar por nombre.")
        return f"SELECT * FROM Tag WHERE name = '{self.name}'"

    def to_exist_name(self) -> str:
        """Genera una sentencia SQL SELECT para verificar la existencia de una etiqueta por su nombre.

        Returns:
            str: La sentencia SQL SELECT como cadena de texto.

        Raises:
            ValueError: Si el atributo `name` es nulo.
        """
        if self.name is None:
            raise ValueError("El nombre debe ser proporcionado para verificar la existencia.")
        return f"SELECT EXISTS(SELECT count() FROM Tag WHERE name = '{self.name}')"
