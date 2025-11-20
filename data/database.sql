-- =============================== --
--      DATOS DE LOS DOCUMENTOS      --
-- =============================== --

-- Tabla: documento
/*
    Tabla principal para almacenar documentos.
    Gestiona la información básica de cada documento en la biblioteca.

    Ejemplos de uso:
    INSERT INTO documento (nombre, extension, hash, tamano, esta_activo) VALUES
    ('manual_python', 'pdf', 'a1b2c3d4e5f6', 1024, 1);
    
    SELECT nombre, extension FROM documento WHERE esta_activo = 1;
*/
CREATE TABLE IF NOT EXISTS documento(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    extension TEXT NOT NULL CHECK (length(extension) <= 10),
    hash TEXT NOT NULL UNIQUE, 
    tamano INTEGER CHECK (tamano >= 0),
    esta_activo INTEGER DEFAULT 1,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: metadato
/*
    Tabla para metadatos extraídos con ExifTool.
    Almacena pares clave-valor de metadatos de los documentos.

    Ejemplos de uso:
    INSERT INTO metadato (id_documento, clave, valor) VALUES
    (1, 'Author', 'John Doe'),
    (1, 'CreationDate', '2023-10-21');
    
    SELECT clave, valor FROM metadato WHERE id_documento = 1;
*/
CREATE TABLE IF NOT EXISTS metadato(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_documento INTEGER NOT NULL,
    clave TEXT NOT NULL,
    valor TEXT NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);

-- Tabla: dato_bibliografico
/*
    Tabla para información bibliográfica principal.
    Gestiona datos bibliográficos esenciales de cada documento.

    Ejemplos de uso:
    INSERT INTO dato_bibliografico 
    (titulo, autores, ano_publicacion, editorial, id_documento) VALUES
    ('Python Programming', 'John Doe', 2023, 'TechBooks', 1);
    
    SELECT titulo, autores FROM dato_bibliografico WHERE ano_publicacion > 2020;
*/
CREATE TABLE IF NOT EXISTS dato_bibliografico(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autores TEXT NULL,
    ano_publicacion INTEGER CHECK (ano_publicacion >= 0 AND ano_publicacion <= strftime('%Y', 'now')),
    editorial TEXT NULL,
    lugar_publicacion TEXT NULL,
    id_documento INTEGER NOT NULL UNIQUE,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);

-- Tabla: dato_bibliografico_complementario
/*
    Tabla para información bibliográfica adicional.
    Almacena detalles complementarios de las referencias bibliográficas.

    Ejemplos de uso:
    INSERT INTO dato_bibliografico_complementario 
    (id_dato_bibliografico, numero_edicion, idioma, isbn) VALUES
    (1, 2, 'Español', '978-0-123456-47-2');
    
    SELECT bc.isbn, db.titulo 
    FROM dato_bibliografico_complementario bc 
    JOIN dato_bibliografico db ON bc.id_dato_bibliografico = db.id;
*/
CREATE TABLE IF NOT EXISTS dato_bibliografico_complementario(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dato_bibliografico INTEGER NOT NULL UNIQUE,
    numero_edicion INTEGER NULL CHECK (numero_edicion > 0),
    idioma TEXT NULL,
    volumen_tomo TEXT NULL,
    numero_paginas INTEGER CHECK (numero_paginas > 0),
    isbn TEXT NULL UNIQUE,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_dato_bibliografico) REFERENCES dato_bibliografico (id) ON DELETE CASCADE
);



-- Tabla: capitulo
/*
    Almacena la información de los capítulos de los documentos.
*/
CREATE TABLE IF NOT EXISTS capitulo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_documento INTEGER NOT NULL,
    numero_capitulo INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    pagina_inicio INTEGER,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);

-- Tabla: seccion
/*
    Tabla para gestionar el índice detallado de los capítulos.
    Almacena la estructura jerárquica de secciones dentro de cada capítulo.

    Ejemplos de uso:
    INSERT INTO seccion (id_capitulo, titulo, nivel, numero_pagina) VALUES
    (1, '1.1 Instalación', 1, 2),
    (1, '1.1.1 Windows', 2, 3);
    
    SELECT titulo, numero_pagina 
    FROM seccion 
    WHERE id_capitulo = 1 
    ORDER BY nivel, numero_pagina;
    
    Estructura jerárquica de índices:
    - Nivel 1: Capítulos principales (1, 2, 3)
    - Nivel 2: Subcapítulos (1.1, 1.2, 2.1)
    - Nivel 3: Secciones (1.1.1, 1.1.2)
    - Nivel 4: Subsecciones (1.1.1.1) etc.
*/
CREATE TABLE IF NOT EXISTS seccion( 
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
);

-- =================================== --
--      ORGANIZACIÓN DE DOCUMENTOS     --
-- =================================== --

-- Tabla: favorito
/*
    Marca los documentos favoritos del usuario.
*/
CREATE TABLE IF NOT EXISTS favorito(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_documento INTEGER NOT NULL UNIQUE,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_documento) REFERENCES documento (id) ON DELETE CASCADE
);

-- Tabla: categoria
/*
    Organiza los documentos por categorías temáticas.
*/
CREATE TABLE IF NOT EXISTS categoria(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_padre INTEGER NULL,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Grupo
/*
    Almacena la informacion de los grupos
*/
CREATE TABLE IF NOT EXISTS grupo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- Tabla: coleccion
/*
    Agrupa documentos en colecciones personalizadas por el usuario.
*/
CREATE TABLE IF NOT EXISTS coleccion(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: palabra_clave
/*
    Asocia palabras clave a los documentos para facilitar la búsqueda.
*/
CREATE TABLE IF NOT EXISTS palabra_clave(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palabra TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: etiqueta
/*
    Tabla para gestión de etiquetas.
    Permite organizar documentos mediante etiquetas personalizadas.

    Ejemplos de uso:
    INSERT INTO etiqueta (nombre, descripcion) VALUES
    ('Importante', 'Documentos prioritarios'),
    ('Python', 'Relacionado con Python');
*/
CREATE TABLE IF NOT EXISTS etiqueta(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================= --
--      TABLAS PIVOTE      --
-- ======================= --

CREATE TABLE IF NOT EXISTS documento_palabra_clave(
    id_documento INTEGER NOT NULL,
    id_palabra_clave INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_palabra_clave),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_palabra_clave) REFERENCES palabra_clave(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS documento_categoria(
    id_documento INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_categoria),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS documento_coleccion(
    id_documento INTEGER NOT NULL,
    id_coleccion INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_coleccion),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_coleccion) REFERENCES coleccion(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS documento_grupo(
    id_documento INTEGER NOT NULL,
    id_grupo INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_grupo),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_grupo) REFERENCES grupo(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS documento_etiqueta(
    id_documento INTEGER NOT NULL,
    id_etiqueta INTEGER NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_documento, id_etiqueta),
    FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_etiqueta) REFERENCES etiqueta(id) ON DELETE CASCADE
);

-- =================== --
--    DISPARADORES     --
-- =================== --

-- Triggers para actualizar el campo 'actualizado_en'
CREATE TRIGGER IF NOT EXISTS trig_actualizar_documento AFTER UPDATE ON documento BEGIN UPDATE documento SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_metadato AFTER UPDATE ON metadato BEGIN UPDATE metadato SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_dato_bibliografico AFTER UPDATE ON dato_bibliografico BEGIN UPDATE dato_bibliografico SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_dato_bib_comp AFTER UPDATE ON dato_bibliografico_complementario BEGIN UPDATE dato_bibliografico_complementario SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_capitulo AFTER UPDATE ON capitulo BEGIN UPDATE capitulo SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_seccion AFTER UPDATE ON seccion BEGIN UPDATE seccion SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_favorito AFTER UPDATE ON favorito BEGIN UPDATE favorito SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_categoria AFTER UPDATE ON categoria BEGIN UPDATE categoria SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_coleccion AFTER UPDATE ON coleccion BEGIN UPDATE coleccion SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_grupo AFTER UPDATE ON grupo BEGIN UPDATE grupo SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_palabra_clave AFTER UPDATE ON palabra_clave BEGIN UPDATE palabra_clave SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;
CREATE TRIGGER IF NOT EXISTS trig_actualizar_etiqueta AFTER UPDATE ON etiqueta BEGIN UPDATE etiqueta SET actualizado_en = CURRENT_TIMESTAMP WHERE id = NEW.id; END;

-- Trigger para validar extensiones de archivo permitidas
CREATE TRIGGER IF NOT EXISTS trig_validar_extension_documento
BEFORE INSERT ON documento
BEGIN
    SELECT CASE
        WHEN NEW.extension NOT IN ('pdf', 'doc', 'docx', 'txt', 'epub', 'mobi')
        THEN RAISE(ABORT, 'Extensión de archivo no válida. Use pdf, doc, docx, txt, epub o mobi.')
    END;
END;

-- =============== --
--      ÍNDICES    --
-- =============== --

CREATE INDEX IF NOT EXISTS idx_documento_hash ON documento(hash);
CREATE INDEX IF NOT EXISTS idx_documento_extension ON documento(extension);
CREATE INDEX IF NOT EXISTS idx_documento_nombre ON documento(nombre);
CREATE INDEX IF NOT EXISTS idx_dato_bibliografico_titulo ON dato_bibliografico(titulo);
CREATE INDEX IF NOT EXISTS idx_dato_bibliografico_ano ON dato_bibliografico(ano_publicacion);
CREATE INDEX IF NOT EXISTS idx_metadato_documento ON metadato(id_documento);
CREATE INDEX IF NOT EXISTS idx_favorito_documento ON favorito(id_documento);
CREATE INDEX IF NOT EXISTS idx_categoria_nombre ON categoria(nombre);
CREATE INDEX IF NOT EXISTS idx_coleccion_nombre ON coleccion(nombre);
CREATE INDEX IF NOT EXISTS idx_grupo_nombre ON grupo(nombre);
CREATE INDEX IF NOT EXISTS idx_etiqueta_nombre ON etiqueta(nombre);
CREATE INDEX IF NOT EXISTS idx_palabra_clave_palabra ON palabra_clave(palabra);
CREATE INDEX IF NOT EXISTS idx_capitulo_documento ON capitulo(id_documento);
CREATE INDEX IF NOT EXISTS idx_capitulo_numero ON capitulo(numero_capitulo);
CREATE INDEX IF NOT EXISTS idx_seccion_capitulo ON seccion(id_capitulo);
CREATE INDEX IF NOT EXISTS idx_seccion_nivel ON seccion(nivel);
CREATE INDEX IF NOT EXISTS idx_documento_grupo_documento ON documento_grupo(id_documento);
CREATE INDEX IF NOT EXISTS idx_documento_grupo_grupo ON documento_grupo(id_grupo);