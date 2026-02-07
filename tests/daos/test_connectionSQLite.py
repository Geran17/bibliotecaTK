import pytest
from models.daos.connection_sqlite import Database


@pytest.fixture
def db_en_memoria():
    """
    Fixture que crea una base de datos SQLite en memoria para cada prueba.
    Cierra la conexión después de que la prueba finaliza.
    """
    Database.resetear()
    db = Database(ruta_db=":memory:")
    yield db
    db.cerrar()
    Database.resetear()


@pytest.fixture
def db_con_tabla_libros(db_en_memoria):
    """
    Fixture que crea una base de datos con la tabla libros ya creada.
    """
    cursor = db_en_memoria.obtener_cursor()
    cursor.execute(
        '''
        CREATE TABLE libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            año INTEGER
        )
    '''
    )
    db_en_memoria.obtener_conexion().commit()
    return db_en_memoria


def test_singleton_retorna_misma_instancia(db_en_memoria):
    """Verifica que el Singleton retorna la misma instancia"""
    db2 = Database(ruta_db=":memory:")
    assert db_en_memoria is db2


def test_obtener_conexion(db_en_memoria):
    """Verifica que se puede obtener una conexión válida"""
    conn = db_en_memoria.obtener_conexion()
    assert conn is not None


def test_obtener_cursor(db_en_memoria):
    """Verifica que se puede obtener un cursor válido"""
    cursor = db_en_memoria.obtener_cursor()
    assert cursor is not None


def test_foreign_keys_activadas(db_en_memoria):
    """Verifica que las foreign keys están habilitadas"""
    cursor = db_en_memoria.obtener_cursor()
    cursor.execute("PRAGMA foreign_keys")
    resultado = cursor.fetchone()
    assert resultado[0] == 1


def test_row_factory_configurado(db_en_memoria):
    """Verifica que row_factory permite acceso por nombre de columna"""
    import sqlite3

    conn = db_en_memoria.obtener_conexion()
    assert conn.row_factory == sqlite3.Row


def test_insertar_y_consultar_datos(db_con_tabla_libros):
    """Verifica que se pueden insertar y consultar datos"""
    cursor = db_con_tabla_libros.obtener_cursor()

    # Insertar datos
    cursor.execute(
        "INSERT INTO libros (titulo, autor, año) VALUES (?, ?, ?)",
        ("El Quijote", "Cervantes", 1605),
    )
    db_con_tabla_libros.obtener_conexion().commit()

    # Consultar datos
    cursor.execute("SELECT * FROM libros WHERE titulo = ?", ("El Quijote",))
    libro = cursor.fetchone()

    assert libro is not None
    assert libro['titulo'] == "El Quijote"
    assert libro['autor'] == "Cervantes"
    assert libro['año'] == 1605


def test_acceso_por_nombre_columna(db_con_tabla_libros):
    """Verifica que se puede acceder a las columnas por nombre"""
    cursor = db_con_tabla_libros.obtener_cursor()

    cursor.execute(
        "INSERT INTO libros (titulo, autor, año) VALUES (?, ?, ?)",
        ("Cien años de soledad", "García Márquez", 1967),
    )
    db_con_tabla_libros.obtener_conexion().commit()

    cursor.execute("SELECT * FROM libros")
    libro = cursor.fetchone()

    assert libro['titulo'] == "Cien años de soledad"
    assert libro['autor'] == "García Márquez"
    assert libro['año'] == 1967


def test_cerrar_conexion(db_en_memoria):
    """Verifica que al cerrar la conexión se puede reabrir correctamente."""
    db_en_memoria.cerrar()
    conn = db_en_memoria.obtener_conexion()
    assert conn is not None


def test_multiples_consultas(db_con_tabla_libros):
    """Verifica que se pueden hacer múltiples consultas"""
    cursor = db_con_tabla_libros.obtener_cursor()

    # Insertar varios libros
    libros = [
        ("Libro 1", "Autor 1", 2020),
        ("Libro 2", "Autor 2", 2021),
        ("Libro 3", "Autor 3", 2022),
    ]

    cursor.executemany("INSERT INTO libros (titulo, autor, año) VALUES (?, ?, ?)", libros)
    db_con_tabla_libros.obtener_conexion().commit()

    # Consultar todos
    cursor.execute("SELECT * FROM libros")
    resultados = cursor.fetchall()

    assert len(resultados) == 3
    assert resultados[0]['titulo'] == "Libro 1"
    assert resultados[2]['año'] == 2022
