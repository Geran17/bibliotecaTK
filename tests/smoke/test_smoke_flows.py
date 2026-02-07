import csv
from pathlib import Path

from models.controllers.controlar_importacion_csv import ControlarImportacionCSV
from models.daos.database_dao import DataBaseDAO
from models.entities.coleccion import Coleccion
from models.entities.consulta import Consulta
from models.entities.documento import Documento
from models.entities.documento_coleccion import DocumentoColeccion
from models.entities.favorito import Favorito
from utilities.auxiliar import abrir_documento_desde_biblioteca, generar_ruta_documento
from utilities.configuracion import DIRECTORIO_TEMPORAL


def _crear_db(ruta_db: str):
    DataBaseDAO(ruta_db=ruta_db).crear_base_de_datos()


def test_smoke_buscar_favoritos_asociaciones(tmp_path):
    ruta_db = str(tmp_path / "smoke.sqlite3")
    _crear_db(ruta_db)

    documento = Documento(
        nombre="manual_smoke",
        extension="pdf",
        hash="hash_smoke_001",
        tamano=123,
        ruta_db=ruta_db,
    )
    id_documento = documento.insertar()
    assert id_documento is not None

    coleccion = Coleccion(nombre="Coleccion Smoke", ruta_db=ruta_db)
    id_coleccion = coleccion.insertar()
    assert id_coleccion is not None

    asociacion = DocumentoColeccion(
        id_documento=id_documento,
        id_coleccion=id_coleccion,
        ruta_db=ruta_db,
    )
    assert asociacion.asociar() is not None

    favorito = Favorito(id_documento=id_documento, ruta_db=ruta_db)
    assert favorito.marcar() is not None

    consulta = Consulta(ruta_db=ruta_db)
    resultados_nombre = consulta.buscar_documentos_por_nombre(campo="Todo", buscar="manual_smoke")
    assert any(doc["id"] == id_documento for doc in resultados_nombre)

    resultados_coleccion = consulta.get_documentos_por_coleccion(id_coleccion=id_coleccion)
    assert any(doc["id"] == id_documento for doc in resultados_coleccion)

    favoritos = consulta.get_documentos_favoritos()
    assert any(doc["id"] == id_documento for doc in favoritos)


def test_smoke_abrir_documento_desde_biblioteca(tmp_path, monkeypatch):
    ruta_biblioteca = str(tmp_path / "BibliotecaTK")
    Path(ruta_biblioteca).mkdir(parents=True, exist_ok=True)

    id_documento = 7
    nombre = "abrir_smoke"
    extension = "txt"
    ruta_documento = generar_ruta_documento(
        ruta_biblioteca=ruta_biblioteca,
        nombre_documento=f"{nombre}.{extension}",
        id_documento=id_documento,
    )
    Path(ruta_documento).write_text("contenido smoke", encoding="utf-8")

    opened = {"ok": False}

    def _fake_open(ruta_origen: str, pagina=None):
        opened["ok"] = True

    monkeypatch.setattr("utilities.auxiliar.abrir_archivo", _fake_open)

    ok, error = abrir_documento_desde_biblioteca(
        id_documento=id_documento,
        nombre_documento=nombre,
        extension_documento=extension,
        ruta_biblioteca=ruta_biblioteca,
    )
    assert ok is True
    assert error == ""
    assert opened["ok"] is True
    assert Path(DIRECTORIO_TEMPORAL, f"{nombre}.{extension}").exists()


def test_smoke_importacion_csv(tmp_path):
    ruta_db = str(tmp_path / "smoke_csv.sqlite3")
    _crear_db(ruta_db)

    documento = Documento(
        nombre="doc_csv_smoke",
        extension="pdf",
        hash="hash_smoke_csv",
        tamano=321,
        ruta_db=ruta_db,
    )
    id_documento = documento.insertar()
    assert id_documento is not None

    archivo_capitulos = tmp_path / "capitulos_smoke.csv"
    with open(archivo_capitulos, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["numero_capitulo", "titulo", "pagina_inicio"])
        writer.writerow(["1", "Introduccion Smoke", "1"])

    controlador = ControlarImportacionCSV(ruta_db=ruta_db)
    registros, errores = controlador.importar_capitulos_csv(
        ruta_archivo=str(archivo_capitulos),
        id_documento=id_documento,
    )
    assert registros == 1
    assert errores == []
