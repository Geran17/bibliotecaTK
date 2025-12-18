from dataclasses import dataclass


@dataclass
class DataBaseDTO:
    """
    DTO para la configuración de la base de datos.
    """

    # ┌────────────────────────────────────────────────────────────┐
    # │ Tablas
    # └────────────────────────────────────────────────────────────┘

    sql_table_documento = """CREATE TABLE IF NOT EXISTS documento(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    extension TEXT NOT NULL CHECK (length(extension) <= 10),
    hash TEXT NOT NULL UNIQUE, 
    tamano INTEGER CHECK (tamano >= 0),
    esta_activo INTEGER DEFAULT 1,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);"""
    sql_table_metadato = """CREATE TABLE IF NOT EXISTS metadato(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_documento INTEGER NOT NULL,
    clave TEXT NOT NULL,
    valor TEXT NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);"""
    sql_table_bibliografia = """CREATE TABLE IF NOT EXISTS bibliografia(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autores TEXT NULL,
    ano_publicacion INTEGER CHECK (ano_publicacion >= 0),
    editorial TEXT NULL,
    lugar_publicacion TEXT NULL,
    numero_edicion TEXT NULL,
    idioma TEXT NULL,
    volumen_tomo TEXT NULL,
    numero_paginas INTEGER CHECK (numero_paginas > 0),
    isbn TEXT NULL UNIQUE,
    id_documento INTEGER NOT NULL UNIQUE,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);"""
    sql_table_capitulo = """CREATE TABLE IF NOT EXISTS capitulo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_documento INTEGER NOT NULL,
    numero_capitulo INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    pagina_inicio INTEGER,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);"""
    sql_table_seccion = """CREATE TABLE IF NOT EXISTS seccion( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_capitulo INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    nivel TEXT NULL,
    id_padre INTEGER NULL,
    numero_pagina INTEGER,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_capitulo) REFERENCES capitulo (id) ON DELETE CASCADE,
    FOREIGN KEY (id_padre) REFERENCES seccion (id) ON DELETE CASCADE
);"""
    sql_table_favorito = """CREATE TABLE IF NOT EXISTS favorito(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_documento INTEGER NOT NULL UNIQUE,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);"""
    sql_table_categoria = """CREATE TABLE IF NOT EXISTS categoria(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_padre INTEGER NULL,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_padre) REFERENCES categoria(id) ON DELETE CASCADE
);"""
    sql_table_grupo = """CREATE TABLE IF NOT EXISTS grupo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);"""
    sql_table_coleccion = """CREATE TABLE IF NOT EXISTS coleccion(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);"""
    sql_table_palabra_clave = """CREATE TABLE IF NOT EXISTS palabra_clave(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palabra TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);"""
    sql_table_etiqueta = """CREATE TABLE IF NOT EXISTS etiqueta(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);"""

    # ┌────────────────────────────────────────────────────────────┐
    # │ Tablas Pivote
    # └────────────────────────────────────────────────────────────┘

    sql_table_documento_palabra_clave = """CREATE TABLE IF NOT EXISTS documento_palabra_clave(
    id_documento INTEGER NOT NULL,
    id_palabra_clave INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_palabra_clave),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_palabra_clave) REFERENCES palabra_clave(id) ON DELETE CASCADE
);"""
    sql_table_documento_categoria = """CREATE TABLE IF NOT EXISTS documento_categoria(
    id_documento INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_categoria),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id) ON DELETE CASCADE
);"""
    sql_table_documento_coleccion = """CREATE TABLE IF NOT EXISTS documento_coleccion(
    id_documento INTEGER NOT NULL,
    id_coleccion INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_coleccion),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_coleccion) REFERENCES coleccion(id) ON DELETE CASCADE
);"""
    sql_table_documento_grupo = """CREATE TABLE IF NOT EXISTS documento_grupo(
    id_documento INTEGER NOT NULL,
    id_grupo INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_grupo),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_grupo) REFERENCES grupo(id) ON DELETE CASCADE
);"""
    sql_table_documento_etiqueta = """CREATE TABLE IF NOT EXISTS documento_etiqueta(
    id_documento INTEGER NOT NULL,
    id_etiqueta INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_etiqueta),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_etiqueta) REFERENCES etiqueta(id) ON DELETE CASCADE
);"""

    # ┌────────────────────────────────────────────────────────────┐
    # │ Vistas
    # └────────────────────────────────────────────────────────────┘

    sql_view_documento_asociaciones = """CREATE VIEW IF NOT EXISTS vista_documento_asociaciones AS
SELECT
    d.id AS id_documento,
    d.nombre AS nombre_documento,
    MAX(CASE WHEN b.id IS NOT NULL THEN 1 ELSE 0 END) AS tiene_dato_bibliografico,
    MAX(CASE WHEN m.id IS NOT NULL THEN 1 ELSE 0 END) AS tiene_metadato,
    MAX(CASE WHEN c.id IS NOT NULL THEN 1 ELSE 0 END) AS tiene_capitulos,
    MAX(CASE WHEN dc.id_documento IS NOT NULL THEN 1 ELSE 0 END) AS tiene_coleccion,
    MAX(CASE WHEN dg.id_documento IS NOT NULL THEN 1 ELSE 0 END) AS tiene_grupo,
    MAX(CASE WHEN dca.id_documento IS NOT NULL THEN 1 ELSE 0 END) AS tiene_categoria,
    MAX(CASE WHEN de.id_documento IS NOT NULL THEN 1 ELSE 0 END) AS tiene_etiqueta,
    MAX(CASE WHEN dpc.id_documento IS NOT NULL THEN 1 ELSE 0 END) AS tiene_palabra_clave,
    MAX(CASE WHEN f.id IS NOT NULL THEN 1 ELSE 0 END) AS es_favorito
FROM
    documento d
LEFT JOIN bibliografia b ON d.id = b.id_documento
LEFT JOIN metadato m ON d.id = m.id_documento
LEFT JOIN capitulo c ON d.id = c.id_documento
LEFT JOIN documento_coleccion dc ON d.id = dc.id_documento
LEFT JOIN documento_grupo dg ON d.id = dg.id_documento
LEFT JOIN documento_categoria dca ON d.id = dca.id_documento
LEFT JOIN documento_etiqueta de ON d.id = de.id_documento
LEFT JOIN documento_palabra_clave dpc ON d.id = dpc.id_documento
LEFT JOIN favorito f ON d.id = f.id_documento
GROUP BY d.id, d.nombre;"""

    sql_view_asociaciones_documentos = """CREATE VIEW IF NOT EXISTS vista_asociaciones_documentos AS
SELECT
    d.id,
    d.nombre,
    d.extension,
    d.hash,
    d.tamano,
    d.esta_activo,
    d.creado_en,
    d.actualizado_en,
    vda.es_favorito,
    vda.tiene_capitulos,
    vda.tiene_categoria,
    vda.tiene_coleccion,
    vda.tiene_dato_bibliografico,
    vda.tiene_etiqueta,
    vda.tiene_grupo,
    vda.tiene_metadato,
    vda.tiene_palabra_clave
FROM documento d
INNER JOIN vista_documento_asociaciones vda ON d.id = vda.id_documento;"""

    # ┌────────────────────────────────────────────────────────────┐
    # │ Disparadores
    # └────────────────────────────────────────────────────────────┘

    sql_triggers = [
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_documento AFTER UPDATE ON documento BEGIN UPDATE documento SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_metadato AFTER UPDATE ON metadato BEGIN UPDATE metadato SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_bibliografia AFTER UPDATE ON bibliografia BEGIN UPDATE bibliografia SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_capitulo AFTER UPDATE ON capitulo BEGIN UPDATE capitulo SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_seccion AFTER UPDATE ON seccion BEGIN UPDATE seccion SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_favorito AFTER UPDATE ON favorito BEGIN UPDATE favorito SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_categoria AFTER UPDATE ON categoria BEGIN UPDATE categoria SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_coleccion AFTER UPDATE ON coleccion BEGIN UPDATE coleccion SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_grupo AFTER UPDATE ON grupo BEGIN UPDATE grupo SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_palabra_clave AFTER UPDATE ON palabra_clave BEGIN UPDATE palabra_clave SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
        "CREATE TRIGGER IF NOT EXISTS trig_actualizar_etiqueta AFTER UPDATE ON etiqueta BEGIN UPDATE etiqueta SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;",
    ]

    # ┌────────────────────────────────────────────────────────────┐
    # │ Índices
    # └────────────────────────────────────────────────────────────┘

    sql_indexes = [
        "CREATE INDEX IF NOT EXISTS idx_documento_hash ON documento(hash);",
        "CREATE INDEX IF NOT EXISTS idx_documento_extension ON documento(extension);",
        "CREATE INDEX IF NOT EXISTS idx_documento_nombre ON documento(nombre);",
        "CREATE INDEX IF NOT EXISTS idx_bibliografia_titulo ON bibliografia(titulo);",
        "CREATE INDEX IF NOT EXISTS idx_bibliografia_ano ON bibliografia(ano_publicacion);",
        "CREATE INDEX IF NOT EXISTS idx_metadato_documento ON metadato(id_documento);",
        "CREATE INDEX IF NOT EXISTS idx_favorito_documento ON favorito(id_documento);",
        "CREATE INDEX IF NOT EXISTS idx_categoria_nombre ON categoria(nombre);",
        "CREATE INDEX IF NOT EXISTS idx_coleccion_nombre ON coleccion(nombre);",
        "CREATE INDEX IF NOT EXISTS idx_grupo_nombre ON grupo(nombre);",
        "CREATE INDEX IF NOT EXISTS idx_etiqueta_nombre ON etiqueta(nombre);",
        "CREATE INDEX IF NOT EXISTS idx_palabra_clave_palabra ON palabra_clave(palabra);",
        "CREATE INDEX IF NOT EXISTS idx_capitulo_documento ON capitulo(id_documento);",
        "CREATE INDEX IF NOT EXISTS idx_capitulo_numero ON capitulo(numero_capitulo);",
        "CREATE INDEX IF NOT EXISTS idx_seccion_capitulo ON seccion(id_capitulo);",
        "CREATE INDEX IF NOT EXISTS idx_seccion_nivel ON seccion(nivel);",
        "CREATE INDEX IF NOT EXISTS idx_documento_grupo_documento ON documento_grupo(id_documento);",
        "CREATE INDEX IF NOT EXISTS idx_documento_grupo_grupo ON documento_grupo(id_grupo);",
    ]
