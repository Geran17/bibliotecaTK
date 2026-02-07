import pytest
from models.dtos.documento_dto import DocumentoDTO


def test_documento_dto_creacion_instancia():
    """
    Verifica que una instancia de DocumentoDTO se crea correctamente
    con los valores proporcionados y los valores por defecto.
    """
    # 1. Arrange: Define los datos de prueba
    nombre = "mi_documento.pdf"
    extension = "pdf"
    hash_val = "a1b2c3d4e5"
    tamano = 1024

    # 2. Act: Crea la instancia del DTO
    doc_dto = DocumentoDTO(
        nombre=nombre,
        extension=extension,
        hash=hash_val,
        tamano=tamano,
    )

    # 3. Assert: Verifica que los atributos se asignaron correctamente
    assert doc_dto.nombre == nombre
    assert doc_dto.extension == extension
    assert doc_dto.hash == hash_val
    assert doc_dto.tamano == tamano
    # Verifica los valores por defecto
    assert doc_dto.id is None
    assert doc_dto.esta_activo is True
    assert doc_dto.creado_en is None
    assert doc_dto.actualizado_en is None
