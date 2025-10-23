from dataclasses import dataclass
from typing import Optional


@dataclass
class FavoriteDTO:
    """
    DTO para representar documentos marcados como favoritos.

    Esta clase encapsula la información necesaria para gestionar los documentos
    marcados como favoritos por el usuario. Permite un acceso rápido a los
    documentos más importantes o frecuentemente consultados.

    Attributes:
        id (Optional[int]): Identificador único del registro favorito
        id_doc (int): Identificador del documento marcado como favorito
        created_at (Optional[str]): Fecha y hora en que se marcó como favorito
        updated_at (Optional[str]): Fecha y hora de última actualización

    Example:
        >>> favorito = FavoriteDTO(
        ...     id_doc=1,
        ... )
    """

    id: Optional[int] = None
    id_doc: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_insert(self) -> str:
        """Genera una sentencia SQL INSERT para un nuevo registro favorito.

        Returns:
            str: La sentencia SQL INSERT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` no es nulo.
        """
        if self.id is not None:
            raise ValueError("ID debe ser nulo para una operación de inserción.")
        return f"INSERT INTO Favorite(id_doc)VALUES({self.id_doc})"

    def to_delete(self) -> str:
        """Genera una sentencia SQL DELETE para eliminar un registro favorito.

        Returns:
            str: La sentencia SQL DELETE como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("ID no puede ser nulo para una operación de eliminación.")
        return f"DELETE FROM Favorite WHERE id = {self.id}"

    def to_instacie_by_id(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro favorito por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id` es nulo.
        """
        if self.id is None:
            raise ValueError("El ID debe ser proporcionado para buscar por ID.")
        return f"SELECT * FROM Favorite WHERE id = {self.id}"

    def to_instacie_by_id_doc(self) -> str:
        """Genera una sentencia SQL SELECT para buscar un registro favorito por su ID de documento.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto.

        Raises:
            ValueError: Si el atributo `id_doc` es nulo.
        """
        if self.id_doc is None:
            raise ValueError("El ID de documento debe ser proporcionado para buscar.")
        return f"SELECT * FROM Favorite WHERE id_doc = {self.id_doc}"

    def to_exist_id_doc(self) -> str:
        """Genera una sentencia SQL SELECT para verificar la existencia de un registro favorito por su ID.

        Returns:
            str: La sentencia SQL SELECT como una cadena de texto

        ValueError:
            Si el atributo `id_doc` es nulo.
        """
        if self.id_doc is None:
            raise ValueError(
                "No se puede verificar la existencia de un registro por su ID de documento."
            )
        return f"SELECT EXISTS(SELECT count() FROM Favorite WHERE id_doc = {self.id_doc})"
