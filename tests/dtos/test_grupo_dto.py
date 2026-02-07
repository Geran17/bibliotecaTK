import pytest
from models.dtos.grupo_dto import GrupoDTO


def test_grupo_dto_creacion_instancia_completa():
    """
    Verifica que una instancia de GrupoDTO se crea correctamente
    con todos los valores proporcionados.
    """
    # 1. Arrange: Define los datos de prueba
    nombre = "Grupo de Estudio de Python"
    descripcion = "Un grupo para aprender y discutir sobre Python."
    id_grupo = 1

    # 2. Act: Crea la instancia del DTO
    grupo_dto = GrupoDTO(nombre=nombre, descripcion=descripcion, id=id_grupo)

    # 3. Assert: Verifica que los atributos se asignaron correctamente
    assert grupo_dto.nombre == nombre
    assert grupo_dto.descripcion == descripcion
    assert grupo_dto.id == id_grupo
    # Verifica los valores por defecto que no se inicializan
    assert grupo_dto.creado_en is None
    assert grupo_dto.actualizado_en is None


def test_grupo_dto_creacion_instancia_minima():
    """
    Verifica que una instancia de GrupoDTO se crea correctamente
    solo con los campos obligatorios.
    """
    # 1. Arrange
    nombre = "Grupo de Lectura"

    # 2. Act
    grupo_dto = GrupoDTO(nombre=nombre)

    # 3. Assert
    assert grupo_dto.nombre == nombre
    assert grupo_dto.descripcion is None
    assert grupo_dto.id is None
