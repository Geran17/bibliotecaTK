import pytest
from src.models.entities.coleccion import Coleccion
from src.models.daos.connection_sqlite import Database
from src.models.daos.coleccion_dao import ColeccionDAO
from src.models.dtos.coleccion_dto import ColeccionDTO

# --- Fixtures ---


@pytest.fixture
def setup_db():
    """
    Fixture que prepara y limpia la base de datos en memoria para cada test.
    """
    Database.resetear()
    # Instanciar el DAO crea la tabla automáticamente
    ColeccionDAO(ruta_db=":memory:")
    yield
    Database.resetear()


# --- Tests para la Entidad Coleccion ---


def test_coleccion_init(setup_db):
    """
    Verifica que la entidad Coleccion se inicializa correctamente.
    """
    col = Coleccion(
        nombre="Mi Colección", descripcion="Una descripción de prueba", ruta_db=":memory:"
    )
    assert col.nombre == "Mi Colección"
    assert col.descripcion == "Una descripción de prueba"
    assert isinstance(col._dao, ColeccionDAO)


def test_insertar_coleccion(setup_db):
    """
    Verifica que el método insertar() guarda la colección en la BD.
    """
    col = Coleccion(
        nombre="Fantasía Épica", descripcion="Libros de dragones y magia", ruta_db=":memory:"
    )

    nuevo_id = col.insertar()

    assert nuevo_id is not None
    assert isinstance(nuevo_id, int)

    # Verificar directamente en la BD
    dao = ColeccionDAO(ruta_db=":memory:")
    resultado = dao.instanciar(params=(nuevo_id,))
    assert len(resultado) == 1
    assert resultado[0]['nombre'] == "Fantasía Épica"


def test_existe_coleccion(setup_db):
    """
    Verifica que el método existe() detecta correctamente una colección por su nombre.
    """
    # Colección a insertar
    col1 = Coleccion(nombre="Historia Antigua", ruta_db=":memory:")
    col1.insertar()

    # Colección con el mismo nombre para comprobar
    col2 = Coleccion(nombre="Historia Antigua", ruta_db=":memory:")
    assert col2.existe() is True

    # Colección con nombre diferente
    col3 = Coleccion(nombre="Biografías", ruta_db=":memory:")
    assert col3.existe() is False


def test_eliminar_coleccion(setup_db):
    """
    Verifica que el método eliminar() borra la colección de la BD.
    """
    col = Coleccion(nombre="A Borrar", ruta_db=":memory:")
    col.id = col.insertar()  # Asignamos el ID después de insertar

    assert col.id is not None

    exito = col.eliminar()
    assert exito is True

    # Verificar que ya no existe en la BD
    dao = ColeccionDAO(ruta_db=":memory:")
    resultado = dao.instanciar(params=(col.id,))
    assert len(resultado) == 0


def test_actualizar_coleccion(setup_db):
    """
    Verifica que el método actualizar() modifica la colección en la BD.
    """
    col = Coleccion(nombre="Original", descripcion="Desc Original", ruta_db=":memory:")
    col.id = col.insertar()

    # Modificar el objeto
    col.nombre = "Actualizado"
    col.descripcion = "Desc Actualizada"

    exito = col.actualizar()
    assert exito is True

    # Verificar los cambios en la BD
    dao = ColeccionDAO(ruta_db=":memory:")
    resultado = dao.instanciar(params=(col.id,))
    assert len(resultado) == 1
    col_actualizada = resultado[0]
    assert col_actualizada['nombre'] == "Actualizado"
    assert col_actualizada['descripcion'] == "Desc Actualizada"


def test_instanciar_coleccion(setup_db):
    """
    Verifica que el método instanciar() carga los datos de la BD en el objeto.
    """
    # Insertar una colección de prueba directamente con el DAO
    dao = ColeccionDAO(ruta_db=":memory:")
    dto = ColeccionDTO(nombre="Ciencia", descripcion="Libros científicos")
    id_prueba = dao.insertar(data=dto)

    # Crear una entidad solo con el ID
    col = Coleccion(nombre="", id=id_prueba, ruta_db=":memory:")

    exito = col.instanciar()
    assert exito is True

    # Verificar que los atributos del objeto se han actualizado
    assert col.nombre == "Ciencia"
    assert col.descripcion == "Libros científicos"
    assert col.creado_en is not None


def test_instanciar_coleccion_no_existente(setup_db):
    """
    Verifica que instanciar() devuelve False si el ID no existe.
    """
    col = Coleccion(nombre="", id=999, ruta_db=":memory:")
    exito = col.instanciar()
    assert exito is False
