import pytest
from models.dtos.capitulo_dto import CapituloDTO


def test_capitulo_dto_creacion_instancia_completa():
    """
    Verifica que una instancia de CapituloDTO se crea correctamente
    con todos los valores proporcionados.
    """
    # 1. Arrange: Define los datos de prueba
    id_documento = 1
    numero_capitulo = 5
    titulo = "El Comienzo de la Aventura"
    id_capitulo = 101
    pagina_inicio = 15

    # 2. Act: Crea la instancia del DTO
    capitulo_dto = CapituloDTO(
        id_documento=id_documento,
        numero_capitulo=numero_capitulo,
        titulo=titulo,
        id=id_capitulo,
        pagina_inicio=pagina_inicio,
    )

    # 3. Assert: Verifica que los atributos se asignaron correctamente
    assert capitulo_dto.id_documento == id_documento
    assert capitulo_dto.numero_capitulo == numero_capitulo
    assert capitulo_dto.titulo == titulo
    assert capitulo_dto.id == id_capitulo
    assert capitulo_dto.pagina_inicio == pagina_inicio
    assert capitulo_dto.creado_en is None
    assert capitulo_dto.actualizado_en is None


def test_capitulo_dto_creacion_instancia_minima():
    """
    Verifica que una instancia de CapituloDTO se crea correctamente
    solo con los campos obligatorios.
    """
    # 1. Arrange, 2. Act
    capitulo_dto = CapituloDTO(id_documento=2, numero_capitulo=1, titulo="Introducción")

    # 3. Assert
    assert capitulo_dto.id is None
    assert capitulo_dto.pagina_inicio is None
