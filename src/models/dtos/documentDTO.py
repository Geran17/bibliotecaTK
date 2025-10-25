from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentDTO:
    """
    DTO para representar documentos en la biblioteca.

    Esta clase encapsula toda la información necesaria para gestionar documentos
    en el sistema, incluyendo sus metadatos y estado.

    Attributes:
        id (Optional[int]): Identificador único del documento
        name (str): Nombre del documento
        extension (str): Extensión del archivo (pdf, doc, etc.)
        hash (str): Hash único del archivo para verificar integridad
        size (float): Tamaño del archivo en bytes
        is_active (bool): Estado del documento (activo/inactivo)
        created_at (Optional[str]): Fecha y hora de creación del documento
        updated_at (Optional[str]): Fecha y hora de última modificación

    Example:
        >>> documento = DocumentDTO(
        ...     name="manual_usuario",
        ...     extension="pdf",
        ...     hash="abc123def456",
        ...     size=1024.5,
        ...     is_active=True
        ... )
    """

    name: str
    extension: str
    hash: str
    size: float
    id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_update_all(self) -> str:
        """Genera una sentencia SQL UPDATE para todos los campos del documento.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Document SET name = '{self.name}', extension = '{self.extension}', hash = '{self.hash}', size = {self.size}, is_active = {self.is_active} WHERE id = {self.id}"

    def to_update_name(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'name'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Document SET name = '{self.name}' WHERE id = {self.id}"

    def to_update_extension(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'extension'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Document SET extension = '{self.extension}' WHERE id = {self.id}"

    def to_update_hash(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'hash'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Document SET hash = '{self.hash}' WHERE id = {self.id}"

    def to_update_size(self) -> str:
        """Genera una sentencia SQL UPDATE para el campo 'size'.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE Document SET size = {self.size} WHERE id = {self.id}"

    def to_exist_hash(self) -> str:
        """Genera una sentencia SQL SELECT para verificar la existencia de un documento por su hash.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        ValueError:
            Si el atributo `hash` es nulo.
        """
        if self.hash is None:
            raise ValueError("El hash debe ser proporcionado para verificar la existencia.")
        return f"SELECT EXISTS(SELECT count() FROM Document WHERE hash = '{self.hash}')"

    def to_instancie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un documento por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM Document WHERE id = {self.id}"

    def to_instancie_by_hash(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un documento por su hash.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `hash` es nulo.
        """
        if self.hash is None:
            raise ValueError("El hash debe ser proporcionado para buscar por hash.")
        return f"SELECT * FROM Document WHERE hash = '{self.hash}'"
