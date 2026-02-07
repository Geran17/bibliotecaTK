import pytest
import sqlite3
from typing import List, Dict, Any, Optional

from models.daos.dao import DAO

# --- Implementación Concreta para Pruebas ---


class MockDAO(DAO):
    """
    Una implementación concreta de DAO para probar la funcionalidad de la clase base.
    Utiliza una tabla simple llamada 'mock_table'.
    """

    def crear_tabla(self):
        """Crea una tabla de prueba 'mock_table'."""
        sql = """
        CREATE TABLE IF NOT EXISTS mock_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            valor INTEGER
        )
        """
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as e:
            print(f"Error al crear mock_table: {e}")
            con.rollback()
            raise

    # --- Métodos abstractos implementados ---

    def insertar(self, sql: str = None, params: tuple = ()) -> Optional[int]:
        """Implementación para insertar en 'mock_table'."""
        if sql is None:
            sql = "INSERT INTO mock_table (nombre, valor) VALUES (?, ?)"
        return self._ejecutar_insertar(sql, params)

    def eliminar(self, sql: str = None, params: tuple = ()) -> bool:
        """Implementación mínima para cumplir con la abstracción."""
        if sql is None:
            sql = "DELETE FROM mock_table WHERE id = ?"
        try:
            con = self._conectar()
            cursor = con.cursor()
            cursor.execute(sql, params)
            con.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            con.rollback()
            return False

    def instanciar(self, sql: str = None, params: tuple = ()) -> List[Dict[str, Any]]:
        """Implementación para consultar 'mock_table'."""
        if sql is None:
            sql = "SELECT * FROM mock_table"
        return self._ejecutar_consulta(sql, params)

    def existe(self, sql: str = None, params: tuple = ()) -> bool:
        """Implementación mínima para cumplir con la abstracción."""
        if sql is None:
            sql = "SELECT 1 FROM mock_table WHERE nombre = ?"
        return len(self._ejecutar_consulta(sql, params)) > 0


# --- Fixtures ---


@pytest.fixture
def mock_dao_en_memoria(tmp_path):
    """
    Fixture que crea un MockDAO con una base de datos temporal en archivo.
    """
    ruta_db = tmp_path / "mock.sqlite3"
    dao = MockDAO(ruta_db=str(ruta_db))
    yield dao


# --- Tests para la clase base DAO ---


def test_dao_init_crea_tabla(mock_dao_en_memoria):
    """
    Verifica que el constructor de DAO llama a `crear_tabla` y la tabla existe.
    """
    dao = mock_dao_en_memoria
    cursor = dao._cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mock_table';")
    assert (
        cursor.fetchone() is not None
    ), "La tabla 'mock_table' debería haber sido creada por el constructor."


def test_ejecutar_insertar_funciona(mock_dao_en_memoria):
    """
    Verifica que el método protegido `_ejecutar_insertar` inserta datos y devuelve un ID.
    """
    dao = mock_dao_en_memoria
    nuevo_id = dao.insertar(params=('test_nombre', 100))

    assert nuevo_id is not None
    assert isinstance(nuevo_id, int)

    # Comprobar con una consulta directa
    cursor = dao._cursor()
    cursor.execute("SELECT * FROM mock_table WHERE id = ?", (nuevo_id,))
    fila = cursor.fetchone()
    assert fila['nombre'] == 'test_nombre'
    assert fila['valor'] == 100


def test_ejecutar_insertar_falla_y_hace_rollback(mock_dao_en_memoria):
    """
    Verifica que `_ejecutar_insertar` devuelve None y hace rollback en caso de error.
    """
    dao = mock_dao_en_memoria
    dao.insertar(params=('nombre_unico', 1))

    # Intentar insertar un nombre duplicado, lo que viola la restricción UNIQUE
    id_fallido = dao.insertar(params=('nombre_unico', 2))

    assert id_fallido is None, "La inserción fallida debería devolver None."


def test_ejecutar_consulta_funciona(mock_dao_en_memoria):
    """
    Verifica que el método protegido `_ejecutar_consulta` devuelve una lista de diccionarios.
    """
    dao = mock_dao_en_memoria
    dao.insertar(params=('item1', 10))
    dao.insertar(params=('item2', 20))

    resultados = dao.instanciar()

    assert isinstance(resultados, list)
    assert len(resultados) == 2
    assert isinstance(resultados[0], dict)
    assert resultados[1]['nombre'] == 'item2'
    assert resultados[1]['valor'] == 20
