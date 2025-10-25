import unittest
import sys
import os

# Añadir el directorio raíz del proyecto al path para poder importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models.dtos.documentDTO import DocumentDTO


class TestDocumentDTO(unittest.TestCase):

    def setUp(self):
        """Configura los objetos DTO para ser usados en los tests."""
        self.doc_with_id = DocumentDTO(
            id=1,
            name="manual_python",
            extension="pdf",
            hash="abc123def456",
            size=1024.5,
            is_active=True,
        )
        self.doc_without_id = DocumentDTO(
            name="new_manual", extension="docx", hash="fedcba654321", size=2048.0, is_active=False
        )

    def test_initialization(self):
        """Prueba la inicialización correcta de los atributos del DTO."""
        self.assertEqual(self.doc_with_id.id, 1)
        self.assertEqual(self.doc_with_id.name, "manual_python")
        self.assertEqual(self.doc_with_id.extension, "pdf")
        self.assertEqual(self.doc_with_id.hash, "abc123def456")
        self.assertEqual(self.doc_with_id.size, 1024.5)
        self.assertTrue(self.doc_with_id.is_active)
        self.assertIsNone(self.doc_without_id.id)

    def test_to_update_all(self):
        """Prueba la generación de la sentencia SQL UPDATE para todos los campos."""
        expected_sql = "UPDATE Document SET name = 'manual_python', extension = 'pdf', hash = 'abc123def456', size = 1024.5, is_active = True WHERE id = 1"
        self.assertEqual(self.doc_with_id.to_update_all(), expected_sql)

    def test_to_update_all_raises_error_if_id_is_none(self):
        """Prueba que to_update_all lanza un ValueError si el id es nulo."""
        with self.assertRaises(ValueError):
            self.doc_without_id.to_update_all()

    def test_to_update_name(self):
        """Prueba la generación de la sentencia SQL UPDATE para el nombre."""
        expected_sql = "UPDATE Document SET name = 'manual_python' WHERE id = 1"
        self.assertEqual(self.doc_with_id.to_update_name(), expected_sql)
        with self.assertRaises(ValueError):
            self.doc_without_id.to_update_name()

    def test_to_update_extension(self):
        """Prueba la generación de la sentencia SQL UPDATE para la extensión."""
        expected_sql = "UPDATE Document SET extension = 'pdf' WHERE id = 1"
        self.assertEqual(self.doc_with_id.to_update_extension(), expected_sql)
        with self.assertRaises(ValueError):
            self.doc_without_id.to_update_extension()

    def test_to_update_hash(self):
        """Prueba la generación de la sentencia SQL UPDATE para el hash."""
        expected_sql = "UPDATE Document SET hash = 'abc123def456' WHERE id = 1"
        self.assertEqual(self.doc_with_id.to_update_hash(), expected_sql)
        with self.assertRaises(ValueError):
            self.doc_without_id.to_update_hash()

    def test_to_update_size(self):
        """Prueba la generación de la sentencia SQL UPDATE para el tamaño."""
        expected_sql = "UPDATE Document SET size = 1024.5 WHERE id = 1"
        self.assertEqual(self.doc_with_id.to_update_size(), expected_sql)
        with self.assertRaises(ValueError):
            self.doc_without_id.to_update_size()

    def test_to_exist_hash(self):
        """Prueba la generación de la sentencia SQL para verificar la existencia por hash."""
        expected_sql = "SELECT EXISTS(SELECT count() FROM Document WHERE hash = 'abc123def456')"
        self.assertEqual(self.doc_with_id.to_exist_hash(), expected_sql)

    def test_to_exist_hash_raises_error_if_hash_is_none(self):
        """Prueba que to_exist_hash lanza un ValueError si el hash es nulo."""
        doc = DocumentDTO(id=1, name="test", extension="txt", hash=None, size=100)
        with self.assertRaises(ValueError):
            doc.to_exist_hash()

    def test_to_instancie_by_id(self):
        """Prueba la generación de la sentencia SQL para obtener un registro por ID."""
        expected_sql = "SELECT * FROM Document WHERE id = 1"
        self.assertEqual(self.doc_with_id.to_instancie_by_id(), expected_sql)

    def test_to_instancie_by_id_raises_error_if_id_is_none(self):
        """Prueba que to_instancie_by_id lanza un ValueError si el id es nulo."""
        with self.assertRaises(ValueError):
            self.doc_without_id.to_instancie_by_id()

    def test_to_instancie_by_hash(self):
        """Prueba la generación de la sentencia SQL para obtener un registro por hash."""
        expected_sql = "SELECT * FROM Document WHERE hash = 'abc123def456'"
        self.assertEqual(self.doc_with_id.to_instancie_by_hash(), expected_sql)

    def test_to_instancie_by_hash_raises_error_if_hash_is_none(self):
        """Prueba que to_instancie_by_hash lanza un ValueError si el hash es nulo."""
        doc = DocumentDTO(id=1, name="test", extension="txt", hash=None, size=100)
        with self.assertRaises(ValueError):
            doc.to_instancie_by_hash()


if __name__ == '__main__':
    unittest.main(verbosity=2)
