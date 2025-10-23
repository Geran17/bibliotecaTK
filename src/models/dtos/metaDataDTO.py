from dataclasses import dataclass
from typing import Optional


@dataclass
class MetaDataDTO:
    """
    DTO para representar metadatos de documentos.

    Esta clase encapsula la información de metadatos extraída de los documentos
    usando herramientas como ExifTool. Almacena pares de clave-valor que
    describen características específicas del documento.

    Attributes:
        id (Optional[int]): Identificador único del metadato
        id_doc (int): Identificador del documento al que pertenece
        key_data (str): Clave o nombre del metadato
        value_data (str): Valor del metadato
        created_at (str): Fecha y hora de creación del registro
        updated_at (str): Fecha y hora de última modificación

    Example:
        >>> metadato = MetaDataDTO(
        ...     id_doc=1,
        ...     key_data="Author",
        ...     value_data="John Doe",
        ...     created_at="2023-10-21 10:00:00",
        ...     updated_at="2023-10-21 10:00:00"
        ... )
    """

    id: Optional[int] = None
    id_doc: int
    key_data: str
    value_data: str
    created_at: str
    updated_at: str

    def to_insert(self) -> str:
        """Genera una sentencia SQL INSERT para un nuevo registro de metadato.

        Returns:
            str: La sentencia SQL INSERT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` no es nulo.
        """
        if self.id is not None:
            raise ValueError("ID debe ser nulo para una operación de inserción.")
        return f"INSERT INTO MetaData(id_doc, key_data, value_data)VALUES({self.id_doc}, '{self.key_data}', '{self.value_data}',)"

    def to_update_all(self) -> str:
        """Genera una sentencia SQL UPDATE para todos los campos del registro.

        Returns:
            str: La sentencia SQL UPDATE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de actualización.")
        return f"UPDATE MetaData SET key_data = '{self.key_data}', value_data = '{self.value_data}' WHERE id = {self.id}"

    def to_exist_id_doc(self) -> str:
        """Genera una sentencia SQL SELECT para verificar la existencia de un registro por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_doc` es nulo.
        """
        if self.id_doc is None:
            raise ValueError("El ID de documento debe ser proporcionado para buscar.")
        return f"SELECT EXISTS(SELECT count() FROM MetaData WHERE id_doc = {self.id_doc})"

    def to_delete(self) -> str:
        """Genera una sentencia SQL DELETE para eliminar un registro.

        Returns:
            str: La sentencia SQL DELETE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de eliminación.")
        return f"DELETE FROM MetaData WHERE id = {self.id}"

    def to_instacie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM MetaData WHERE id = {self.id}"

    def to_instacie_by_id_doc(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro por su ID de documento.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_doc` es nulo.
        """
        if self.id_doc is None:
            raise ValueError("El ID de documento debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM MetaData WHERE id_doc = {self.id_doc}"
