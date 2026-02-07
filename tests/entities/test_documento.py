import pytest
from models.entities.documento import Documento
from models.daos.documento_dao import DocumentoDAO

# --- Fixtures ---


@pytest.fixture
def ruta_db(tmp_path):
    """
    Fixture que prepara la ruta de base de datos temporal para cada test.
    """
    return str(tmp_path / "documento_entidad.sqlite3")


# --- Tests para la Entidad Documento ---


def test_documento_init(ruta_db):
    """
    Verifica que la entidad Documento se inicializa correctamente.
    """
    doc = Documento(
        nombre="test.pdf", extension="pdf", hash="hash_init", tamano=100, ruta_db=ruta_db
    )
    assert doc.nombre == "test.pdf"
    assert doc.hash == "hash_init"
    assert isinstance(doc._dao, DocumentoDAO)


def test_insertar_documento(ruta_db):
    """
    Verifica que el método insertar() guarda el documento en la BD y asigna el ID.
    """
    doc = Documento(
        nombre="manual.pdf", extension="pdf", hash="hash_insertar", tamano=1024, ruta_db=ruta_db
    )

    nuevo_id = doc.insertar()

    assert nuevo_id is not None
    assert isinstance(nuevo_id, int)

    # Verificar directamente en la BD
    dao = DocumentoDAO(ruta_db=ruta_db)
    resultado = dao.instanciar(params=(nuevo_id,))
    assert len(resultado) == 1
    assert resultado[0]['hash'] == "hash_insertar"


def test_existe_documento(ruta_db):
    """
    Verifica que el método existe() detecta correctamente un documento por su hash.
    """
    # Documento a insertar
    doc1 = Documento("doc1.txt", "txt", "hash_existente", 500, ruta_db=ruta_db)
    doc1.insertar()

    # Documento con el mismo hash para comprobar
    doc2 = Documento("doc2.txt", "txt", "hash_existente", 600, ruta_db=ruta_db)
    assert doc2.existe() is True

    # Documento con hash diferente
    doc3 = Documento("doc3.txt", "txt", "hash_nuevo", 700, ruta_db=ruta_db)
    assert doc3.existe() is False


def test_eliminar_documento(ruta_db):
    """
    Verifica que el método eliminar() borra el documento de la BD.
    """
    doc = Documento("a_borrar.doc", "doc", "hash_borrar", 1234, ruta_db=ruta_db)
    doc.id = doc.insertar()  # Asignamos el ID después de insertar

    assert doc.id is not None

    exito = doc.eliminar()
    assert exito is True

    # Verificar que ya no existe en la BD
    dao = DocumentoDAO(ruta_db=ruta_db)
    resultado = dao.instanciar(params=(doc.id,))
    assert len(resultado) == 0


def test_actualizar_documento(ruta_db):
    """
    Verifica que el método actualizar() modifica el documento en la BD.
    """
    doc = Documento("original.pdf", "pdf", "hash_original", 2000, ruta_db=ruta_db)
    doc.id = doc.insertar()

    # Modificar el objeto
    doc.nombre = "actualizado.pdf"
    doc.tamano = 2500

    exito = doc.actualizar()
    assert exito is True

    # Verificar los cambios en la BD
    dao = DocumentoDAO(ruta_db=ruta_db)
    resultado = dao.instanciar(params=(doc.id,))
    assert len(resultado) == 1
    doc_actualizado = resultado[0]
    assert doc_actualizado['nombre'] == "actualizado.pdf"
    assert doc_actualizado['tamano'] == 2500


def test_instanciar_documento(ruta_db):
    """
    Verifica que el método instanciar() carga los datos de la BD en el objeto.
    """
    # Insertar un documento de prueba directamente con el DAO
    dao = DocumentoDAO(ruta_db=ruta_db)
    id_prueba = dao.insertar(params=("prueba.txt", "txt", "hash_instanciar", 999, 1))

    # Crear una entidad solo con el ID
    doc = Documento(
        nombre="", extension="", hash="", tamano=0, id=id_prueba, ruta_db=ruta_db  # Datos vacíos
    )

    exito = doc.instanciar()
    assert exito is True

    # Verificar que los atributos del objeto se han actualizado
    assert doc.nombre == "prueba.txt"
    assert doc.hash == "hash_instanciar"
    assert doc.tamano == 999
    assert doc.esta_activo is True


def test_instanciar_documento_no_existente(ruta_db):
    """
    Verifica que instanciar() devuelve False si el ID no existe.
    """
    doc = Documento("", "", "", 0, id=999, ruta_db=ruta_db)
    exito = doc.instanciar()
    assert exito is False
