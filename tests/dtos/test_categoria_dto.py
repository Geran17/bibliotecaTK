import pytest
from models.dtos.categoria_dto import CategoriaDTO


def test_categoria_dto_creacion_instancia_completa():
    """
    Verifica que una instancia de CategoriaDTO se crea correctamente
    con todos los valores proporcionados.
    """
    # 1. Arrange: Define los datos de prueba
    nombre = "Programación"
    descripcion = "Categoría para libros y documentos sobre programación."
    id_padre = 5
    id_categoria = 1

    # 2. Act: Crea la instancia del DTO
    categoria_dto = CategoriaDTO(
        nombre=nombre, descripcion=descripcion, id_padre=id_padre, id=id_categoria
    )

    # 3. Assert: Verifica que los atributos se asignaron correctamente
    assert categoria_dto.nombre == nombre
    assert categoria_dto.descripcion == descripcion
    assert categoria_dto.id_padre == id_padre
    assert categoria_dto.id == id_categoria
    # Verifica los valores por defecto que no se inicializan
    assert categoria_dto.creado_en is None
    assert categoria_dto.actualizado_en is None


def test_categoria_dto_creacion_instancia_minima():
    """
    Verifica que una instancia de CategoriaDTO se crea correctamente
    solo con los campos obligatorios.
    """
    # 1. Arrange
    nombre = "Ciencia Ficción"

    # 2. Act
    categoria_dto = CategoriaDTO(nombre=nombre)

    # 3. Assert
    assert categoria_dto.nombre == nombre
    assert categoria_dto.descripcion is None
    assert categoria_dto.id_padre is None
    assert categoria_dto.id is None
