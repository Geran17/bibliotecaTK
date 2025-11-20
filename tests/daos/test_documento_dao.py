import pytest
import sqlite3
from src.models.daos.documento_dao import DocumentoDAO
from src.models.daos.connection_sqlite import Database

# --- Fixtures ---


@pytest.fixture
def documento_dao_en_memoria():
    """
    Fixture que crea un DocumentoDAO con una base de datos en memoria.
    Se asegura de que la tabla 'documento' esté creada y limpia para cada test.
    """
    Database.resetear()
    # El __init__ de DAO llama a crear_tabla()
    dao = DocumentoDAO(ruta_db=":memory:")
    yield dao
    dao._db.cerrar()
    Database.resetear()


@pytest.fixture
def documento_dao_con_datos(documento_dao_en_memoria):
    """
    Fixture que proporciona un DocumentoDAO con datos de prueba pre-insertados.
    """
    dao = documento_dao_en_memoria
    documentos = [
        ('manual_python', 'pdf', 'hash123', 1024, 1),
        ('tesis_grado', 'docx', 'hash456', 2048, 1),
        ('notas_reunion', 'txt', 'hash789', 512, 0),
    ]
    for doc in documentos:
        dao.insertar(params=doc)
    yield dao


# --- Tests ---


def test_crear_tabla(documento_dao_en_memoria):
    """
    Verifica que la tabla 'documento' se crea correctamente al instanciar el DAO.
    """
    dao = documento_dao_en_memoria
    try:
        cursor = dao._cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documento';")
        assert cursor.fetchone() is not None, "La tabla 'documento' no fue creada."
    except sqlite3.Error as e:
        pytest.fail(f"Ocurrió un error de base de datos: {e}")


def test_insertar_documento(documento_dao_en_memoria):
    """
    Verifica que se puede insertar un nuevo documento correctamente.
    """
    dao = documento_dao_en_memoria
    params = ('libro_cocina', 'pdf', 'hash_cocina', 3072, 1)

    nuevo_id = dao.insertar(params=params)

    assert nuevo_id is not None
    assert isinstance(nuevo_id, int)

    # Verificar que el dato se insertó
    resultado = dao.instanciar(params=(nuevo_id,))
    assert len(resultado) == 1
    assert resultado[0]['nombre'] == 'libro_cocina'
    assert resultado[0]['hash'] == 'hash_cocina'


def test_insertar_hash_duplicado_falla(documento_dao_con_datos):
    """
    Verifica que la inserción falla si se intenta usar un hash duplicado.
    """
    dao = documento_dao_con_datos
    params = ('otro_manual', 'pdf', 'hash123', 4096, 1)  # hash123 ya existe

    # El método DAO está diseñado para capturar la excepción y devolver None.
    # Por lo tanto, verificamos que el resultado sea None.
    id_fallido = dao.insertar(params=params)

    assert id_fallido is None, "La inserción con hash duplicado debería devolver None."


def test_eliminar_documento(documento_dao_con_datos):
    """
    Verifica que se puede eliminar un documento existente.
    """
    dao = documento_dao_con_datos
    id_a_eliminar = 1  # 'manual_python'

    exito = dao.eliminar(params=(id_a_eliminar,))
    assert exito is True

    # Verificar que ya no existe
    resultado = dao.instanciar(params=(id_a_eliminar,))
    assert len(resultado) == 0


def test_eliminar_documento_inexistente(documento_dao_con_datos):
    """
    Verifica que eliminar un documento inexistente no causa error y devuelve False.
    """
    dao = documento_dao_con_datos
    id_inexistente = 999

    exito = dao.eliminar(params=(id_inexistente,))
    assert exito is False


def test_instanciar_por_id(documento_dao_con_datos):
    """
    Verifica que se puede obtener un documento por su ID.
    """
    dao = documento_dao_con_datos
    resultado = dao.instanciar(params=(2,))  # 'tesis_grado'

    assert len(resultado) == 1
    assert resultado[0]['id'] == 2
    assert resultado[0]['nombre'] == 'tesis_grado'


def test_instanciar_todos(documento_dao_con_datos):
    """
    Verifica que se pueden obtener todos los documentos.
    """
    dao = documento_dao_con_datos
    sql = "SELECT * FROM documento"
    resultados = dao.instanciar(sql=sql)

    assert len(resultados) == 3


def test_instanciar_por_hash(documento_dao_con_datos):
    """
    Verifica que se puede obtener un documento por su hash.
    """
    dao = documento_dao_con_datos
    resultado = dao.instanciar_por_hash('hash789')  # 'notas_reunion'

    assert len(resultado) == 1
    assert resultado[0]['id'] == 3
    assert resultado[0]['nombre'] == 'notas_reunion'


def test_actualizar_todo(documento_dao_con_datos):
    """
    Verifica que se pueden actualizar todos los campos de un documento.
    """
    dao = documento_dao_con_datos
    id_a_actualizar = 1
    params = ('manual_python_v2', 'pdf', 'hash123_updated', 1500, 0, id_a_actualizar)

    exito = dao.actualizar_todo(params=params)
    assert exito is True

    # Verificar los datos actualizados
    resultado = dao.instanciar(params=(id_a_actualizar,))
    assert len(resultado) == 1
    doc_actualizado = resultado[0]
    assert doc_actualizado['nombre'] == 'manual_python_v2'
    assert doc_actualizado['hash'] == 'hash123_updated'
    assert doc_actualizado['tamano'] == 1500
    assert doc_actualizado['esta_activo'] == 0


def test_existe_por_hash(documento_dao_con_datos):
    """
    Verifica que el método existe() funciona para un hash existente.
    """
    dao = documento_dao_con_datos
    assert dao.existe(params=('hash456',)) is True


def test_no_existe_por_hash(documento_dao_con_datos):
    """
    Verifica que el método existe() funciona para un hash inexistente.
    """
    dao = documento_dao_con_datos
    assert dao.existe(params=('hash_inexistente',)) is False
