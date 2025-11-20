import pytest
import sqlite3
from src.models.daos.coleccion_dao import ColeccionDAO
from src.models.dtos.coleccion_dto import ColeccionDTO
from src.models.daos.connection_sqlite import Database

# --- Fixtures ---


@pytest.fixture
def coleccion_dao_en_memoria():
    """
    Fixture que crea un ColeccionDAO con una base de datos en memoria.
    Se asegura de que la tabla 'coleccion' esté creada y limpia para cada test.
    """
    Database.resetear()
    # El __init__ de DAO llama a crear_tabla()
    dao = ColeccionDAO(ruta_db=":memory:")
    yield dao
    dao._db.cerrar()
    Database.resetear()


@pytest.fixture
def coleccion_dao_con_datos(coleccion_dao_en_memoria):
    """
    Fixture que proporciona un ColeccionDAO con datos de prueba pre-insertados.
    """
    dao = coleccion_dao_en_memoria
    colecciones = [
        ColeccionDTO(nombre='Novelas Clásicas', descripcion='Libros de literatura clásica.'),
        ColeccionDTO(
            nombre='Ciencia Ficción', descripcion='Viajes espaciales y futuros distópicos.'
        ),
        ColeccionDTO(nombre='Ensayos Filosóficos', descripcion=None),
    ]
    for col in colecciones:
        dao.insertar(data=col)
    yield dao


# --- Tests ---


def test_crear_tabla(coleccion_dao_en_memoria):
    """
    Verifica que la tabla 'coleccion' y su índice se crean correctamente.
    """
    dao = coleccion_dao_en_memoria
    try:
        cursor = dao._cursor()
        # Verificar tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coleccion';")
        assert cursor.fetchone() is not None, "La tabla 'coleccion' no fue creada."
        # Verificar índice
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_coleccion_nombre';"
        )
        assert cursor.fetchone() is not None, "El índice 'idx_coleccion_nombre' no fue creado."
    except sqlite3.Error as e:
        pytest.fail(f"Ocurrió un error de base de datos: {e}")


def test_insertar_coleccion(coleccion_dao_en_memoria):
    """
    Verifica que se puede insertar una nueva colección correctamente.
    """
    dao = coleccion_dao_en_memoria
    data = ColeccionDTO(nombre='Poesía', descripcion='Colección de poemas.')

    nuevo_id = dao.insertar(data=data)

    assert nuevo_id is not None
    assert isinstance(nuevo_id, int)

    # Verificar que el dato se insertó
    resultado = dao.instanciar(params=(nuevo_id,))
    assert len(resultado) == 1
    assert resultado[0]['nombre'] == 'Poesía'
    assert resultado[0]['descripcion'] == 'Colección de poemas.'


def test_insertar_nombre_duplicado_falla(coleccion_dao_con_datos):
    """
    Verifica que la inserción falla si se intenta usar un nombre duplicado.
    """
    dao = coleccion_dao_con_datos
    data = ColeccionDTO(nombre='Ciencia Ficción', descripcion='Otra descripción.')

    id_fallido = dao.insertar(data=data)

    assert id_fallido is None, "La inserción con nombre duplicado debería devolver None."


def test_eliminar_coleccion(coleccion_dao_con_datos):
    """
    Verifica que se puede eliminar una colección existente.
    """
    dao = coleccion_dao_con_datos
    id_a_eliminar = 1  # 'Novelas Clásicas'

    exito = dao.eliminar(id_coleccion=id_a_eliminar)
    assert exito is True

    # Verificar que ya no existe
    resultado = dao.instanciar(params=(id_a_eliminar,))
    assert len(resultado) == 0


def test_eliminar_coleccion_inexistente(coleccion_dao_con_datos):
    """
    Verifica que eliminar una colección inexistente no causa error y devuelve False.
    """
    dao = coleccion_dao_con_datos
    id_inexistente = 999

    exito = dao.eliminar(id_coleccion=id_inexistente)
    assert exito is False


def test_instanciar_por_id(coleccion_dao_con_datos):
    """
    Verifica que se puede obtener una colección por su ID.
    """
    dao = coleccion_dao_con_datos
    resultado = dao.instanciar(params=(2,))  # 'Ciencia Ficción'

    assert len(resultado) == 1
    assert resultado[0]['id'] == 2
    assert resultado[0]['nombre'] == 'Ciencia Ficción'


def test_listar_todos(coleccion_dao_con_datos):
    """
    Verifica que se pueden obtener todas las colecciones.
    """
    dao = coleccion_dao_con_datos
    resultados = dao.listar_todos()

    assert len(resultados) == 3
    assert resultados[0]['nombre'] == 'Novelas Clásicas'
    assert resultados[2]['nombre'] == 'Ensayos Filosóficos'


def test_actualizar(coleccion_dao_con_datos):
    """
    Verifica que se puede actualizar una colección existente.
    """
    dao = coleccion_dao_con_datos
    id_a_actualizar = 1
    nombre_nuevo = "Clásicos de la Literatura"
    desc_nueva = "Una selección de los mejores libros."

    exito = dao.actualizar(
        id_coleccion=id_a_actualizar, nombre=nombre_nuevo, descripcion=desc_nueva
    )
    assert exito is True

    # Verificar los datos actualizados
    resultado = dao.instanciar(params=(id_a_actualizar,))
    assert len(resultado) == 1
    coleccion_actualizada = resultado[0]
    assert coleccion_actualizada['nombre'] == nombre_nuevo
    assert coleccion_actualizada['descripcion'] == desc_nueva


def test_existe_por_nombre(coleccion_dao_con_datos):
    """
    Verifica que el método existe() funciona para un nombre existente.
    """
    dao = coleccion_dao_con_datos
    assert dao.existe(nombre='Ciencia Ficción') is True


def test_no_existe_por_nombre(coleccion_dao_con_datos):
    """
    Verifica que el método existe() funciona para un nombre inexistente.
    """
    dao = coleccion_dao_con_datos
    assert dao.existe(nombre='Terror Gótico') is False
