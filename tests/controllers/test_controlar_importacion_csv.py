import pytest
import csv
from models.controllers.controlar_importacion_csv import ControlarImportacionCSV
from models.daos.documento_dao import DocumentoDAO
from models.daos.capitulo_dao import CapituloDAO


class TestControlarImportacionCSV:
    """Tests para el controlador de importación CSV."""

    @pytest.fixture
    def controlador(self, tmp_path):
        """Fixture que proporciona un controlador con BD temporal en archivo."""
        ruta_db = tmp_path / "importacion_csv.sqlite3"
        ruta_db_str = str(ruta_db)
        documento_dao = DocumentoDAO(ruta_db=ruta_db_str)
        capitulo_dao = CapituloDAO(ruta_db=ruta_db_str)
        documento_dao.insertar(params=("doc_test", "pdf", "hash_doc_test", 100, 1))
        capitulo_dao.insertar(
            sql="""
            INSERT INTO capitulo (id_documento, numero_capitulo, titulo, pagina_inicio)
            VALUES (?, ?, ?, ?)
            """,
            params=(1, 1, "Capitulo Base", 1),
        )
        return ControlarImportacionCSV(ruta_db=ruta_db_str)

    @pytest.fixture
    def archivo_capitulos_valido(self, tmp_path):
        """Crea un archivo CSV válido de capítulos."""
        archivo = tmp_path / "capitulos.csv"
        datos = [
            ['numero_capitulo', 'titulo', 'pagina_inicio'],
            ['1', 'Introducción', '1'],
            ['2', 'Marco Teórico', '15'],
            ['3', 'Metodología', '45'],
        ]
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(datos)
        return str(archivo)

    @pytest.fixture
    def archivo_secciones_valido(self, tmp_path):
        """Crea un archivo CSV válido de secciones."""
        archivo = tmp_path / "secciones.csv"
        datos = [
            ['titulo', 'nivel', 'numero_pagina', 'id_padre'],
            ['Antecedentes', '1.1', '15', ''],
            ['Estado del arte', '1.2', '20', ''],
            ['Planteamiento de hipótesis', '2.1', '45', ''],
            ['Variables independientes', '2.1.1', '46', 'Planteamiento de hipótesis'],
        ]
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(datos)
        return str(archivo)

    @pytest.fixture
    def archivo_capitulos_incompleto(self, tmp_path):
        """Crea un archivo CSV con datos incompletos."""
        archivo = tmp_path / "capitulos_incompleto.csv"
        datos = [
            ['numero_capitulo', 'titulo', 'pagina_inicio'],
            ['1', '', '1'],  # Título vacío
            ['2', 'Marco Teórico', '15'],
            ['', 'Metodología', '45'],  # número_capitulo vacío
        ]
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(datos)
        return str(archivo)

    @pytest.fixture
    def archivo_capitulos_invalido(self, tmp_path):
        """Crea un archivo CSV con formato inválido."""
        archivo = tmp_path / "capitulos_invalido.csv"
        datos = [
            ['titulo', 'pagina_inicio'],  # Falta 'numero_capitulo' (requerido)
            ['Introducción', '1'],
        ]
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(datos)
        return str(archivo)

    def test_importar_capitulos_valido(self, controlador, archivo_capitulos_valido):
        """Test de importación válida de capítulos."""
        registros, errores = controlador.importar_capitulos_csv(
            archivo_capitulos_valido, id_documento=1
        )

        assert registros == 3
        assert len(errores) == 0

    def test_importar_capitulos_con_errores(self, controlador, archivo_capitulos_incompleto):
        """Test de importación con errores de validación."""
        registros, errores = controlador.importar_capitulos_csv(
            archivo_capitulos_incompleto, id_documento=1
        )

        assert registros == 1  # Solo una fila válida
        assert len(errores) > 0
        assert any(
            'título está vacío' in error or 'titulo está vacío' in error for error in errores
        )

    def test_importar_capitulos_archivo_no_existe(self, controlador):
        """Test cuando el archivo no existe."""
        registros, errores = controlador.importar_capitulos_csv(
            '/ruta/inexistente/archivo.csv', id_documento=1
        )

        assert registros == 0
        assert len(errores) > 0
        assert 'no existe' in errores[0].lower()

    def test_importar_capitulos_archivo_invalido(self, controlador, archivo_capitulos_invalido):
        """Test cuando faltan columnas requeridas."""
        registros, errores = controlador.importar_capitulos_csv(
            archivo_capitulos_invalido, id_documento=1
        )

        assert registros == 0
        assert len(errores) > 0

    def test_importar_secciones_valido(self, controlador, archivo_secciones_valido):
        """Test de importación válida de secciones."""
        registros, errores = controlador.importar_secciones_csv(
            archivo_secciones_valido, id_capitulo=1
        )

        assert registros == 4
        assert len(errores) == 0

    def test_limpiar_errores(self, controlador, archivo_capitulos_valido):
        """Test de limpieza de errores."""
        controlador.importar_capitulos_csv(archivo_capitulos_valido, 1)
        errores_antes = controlador.obtener_errores()

        controlador.limpiar_errores()
        errores_despues = controlador.obtener_errores()

        assert len(errores_antes) == 0
        assert len(errores_despues) == 0

    def test_obtener_errores(self, controlador, archivo_capitulos_incompleto):
        """Test para obtener la lista de errores."""
        controlador.importar_capitulos_csv(archivo_capitulos_incompleto, 1)
        errores = controlador.obtener_errores()

        assert len(errores) > 0
        assert all(isinstance(e, str) for e in errores)
