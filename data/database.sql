-- Datos de los Documentos --
-- ----------------------- --

-- Tabla de Documentos
/*
    Tabla principal para almacenar documentos.
    Gestiona la información básica de cada documento en la biblioteca.

    Ejemplos de uso:
    INSERT INTO Document (name, extension, hash, size, is_active) VALUES
    ('manual_python', 'pdf', 'a1b2c3d4e5f6', 1024, 1);
    
    SELECT name, extension FROM Document WHERE is_active = 1;
*/
CREATE TABLE IF NOT EXISTS Document(
    id INTEGER,
    name TEXT NOT NULL,
    extension TEXT NOT NULL CHECK (length(extension) <= 10),
    hash TEXT NOT NULL UNIQUE, 
    size INTEGER CHECK (size >= 0),
    is_active INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT)
);

-- Table MetaData
/*
    Tabla para metadatos extraídos con ExifTool.
    Almacena pares clave-valor de metadatos de los documentos.

    Ejemplos de uso:
    INSERT INTO MetaData (id_doc, key_data, value_data) VALUES
    (1, 'Author', 'John Doe'),
    (1, 'CreationDate', '2023-10-21');
    
    SELECT key_data, value_data FROM MetaData WHERE id_doc = 1;
*/
CREATE TABLE IF NOT EXISTS MetaData(
    id INTEGER,
    id_doc INTEGER,
    key_data TEXT NOT NULL,
    value_data TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY (id_doc) REFERENCES Document (id) ON DELETE CASCADE
);

-- Tabla BibliographyData
/*
    Tabla para información bibliográfica principal.
    Gestiona datos bibliográficos esenciales de cada documento.

    Ejemplos de uso:
    INSERT INTO BibliographyData 
    (title, authors, year_publication, editorial, id_doc) VALUES
    ('Python Programming', 'John Doe', 2023, 'TechBooks', 1);
    
    SELECT title, authors FROM BibliographyData WHERE year_publication > 2020;
*/
CREATE TABLE IF NOT EXISTS BibliographyData(
    id INTEGER,
    title TEXT NOT NULL,
    authors TEXT NULL,
    year_publication INTEGER CHECK (year_publication >= 0 AND year_publication <= strftime('%Y', 'now')),
    editorial TEXT NULL,
    place_publication TEXT NULL,
    id_doc INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY (id_doc) REFERENCES Document (id) ON DELETE CASCADE
);

-- Tabla BibliographyComplementary
/*
    Tabla para información bibliográfica adicional.
    Almacena detalles complementarios de las referencias bibliográficas.

    Ejemplos de uso:
    INSERT INTO BibliographyComplementary 
    (id_bib, number_edition, language, isbn) VALUES
    (1, 2, 'Español', '978-0-123456-47-2');
    
    SELECT bc.isbn, bd.title 
    FROM BibliographyComplementary bc 
    JOIN BibliographyData bd ON bc.id_bib = bd.id;
*/
CREATE TABLE IF NOT EXISTS BibliographyComplementary(
    id INTEGER,
    id_bib INTEGER,
    number_edition INTEGER NULL CHECK (number_edition > 0),
    language TEXT NULL,
    volumen_tomo TEXT NULL,
    number_pagina INTEGER CHECK (number_pagina > 0),
    isbn TEXT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY (id_bib) REFERENCES BibliographyData (id) ON DELETE CASCADE
);

-- Tabla Chapter
/*
    Esta tabla contendra la informacion de los capitulos del de los
    documentos
*/
CREATE TABLE IF NOT EXISTS Chapter(
    id INTEGER,
    id_doc INTEGER NOT NULL,
    number_chapter INTEGER NOT NULL,
    title TEXT NOT NULL,
    page_start INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY (id_doc) REFERENCES Document (id) ON DELETE CASCADE
);

-- Table Index
/* -- Renamed to SubSection
    Tabla para gestionar el índice detallado de capítulos.
    Almacena la estructura jerárquica de secciones dentro de cada capítulo.

    Ejemplos de uso:
    INSERT INTO IndexChapter (id_chapter, title, level, page_number) VALUES
    (1, '1.1 Instalación', 1, 2),
    (1, '1.1.1 Windows', 2, 3);
    
    SELECT title, page_number 
    FROM IndexChapter 
    WHERE id_chapter = 1 
    ORDER BY level, page_number;
    
    Estructura jerárquica de índices:
    - Nivel 1: Capítulos principales (1, 2, 3)
    - Nivel 2: Subcapítulos (1.1, 1.2, 2.1)
    - Nivel 3: Secciones (1.1.1, 1.1.2)
    - Nivel 4: Subsecciones (1.1.1.1)
*/
CREATE TABLE IF NOT EXISTS SubSection( -- Table was named SubSection, not IndexChapter
    id INTEGER,
    id_chapter INTEGER NOT NULL,
    title TEXT NOT NULL,
    level TEXT NULL,
    parent_id INTEGER NULL,
    page_number INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT),
    FOREIGN KEY (id_chapter) REFERENCES Chapter (id) ON DELETE CASCADE, -- Corrected FK reference
    FOREIGN KEY (parent_id) REFERENCES SubSection (id) ON DELETE CASCADE -- Corrected FK reference to itself
);


-- Organización de los Documentos --
-- ------------------------------ --

-- Tabla Favorite
/*
    Esta tabla sirve para seleccionar los documentos
    favoritos por el usuario
*/
CREATE TABLE IF NOT EXISTS Favorite(
    id INTEGER,
    id_doc INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id AUTOINCREMENT),
    FOREIGN KEY (id_doc) REFERENCES Document (id) ON DELETE CASCADE
);

-- Tabla Category
/*
    Esta tabla sirve para organizar los documentos por categorías
*/
CREATE TABLE IF NOT EXISTS Category(
    id INTEGER,
    name TEXT NOT NULL UNIQUE,
    description TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT)
);

-- Tabla Collection
/*
    Esta tabla sirve para organizar los documentos en colecciones
    de acuerdo a la preferencia del usuario
*/
CREATE TABLE IF NOT EXISTS Collection(
    id INTEGER,
    name TEXT NOT NULL UNIQUE,
    description TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT)
);

-- Table WordKey
/*
    Esta tabla sirve para organizar los documentos por palabras claves
*/
CREATE TABLE IF NOT EXISTS WordKey(
    id INTEGER,
    wordkey TEXT NOT NULL,
    description TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT)
);

-- Tabla Tag
/*
    Tabla para gestión de etiquetas.
    Permite organizar documentos mediante etiquetas personalizadas.

    Ejemplos de uso:
    INSERT INTO Tag (name, description) VALUES
    ('Importante', 'Documentos prioritarios'),
    ('Python', 'Relacionado con Python');
    
    SELECT d.name, t.name as tag 
    FROM Document d 
    JOIN DocumentTag dt ON d.id = dt.id_document
    JOIN Tag t ON t.id = dt.id_tag;
*/
CREATE TABLE IF NOT EXISTS Tag(
    id INTEGER,
    name TEXT NOT NULL UNIQUE,
    description TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT)
);

-- Tablas Relacionales --
-- ------------------- --
CREATE TABLE IF NOT EXISTS DocumentWordKey(
    id_wordkey INTEGER,
    id_document INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_wordkey, id_document),
    FOREIGN KEY (id_document) REFERENCES Document(id) ON DELETE CASCADE,
    FOREIGN KEY (id_wordkey) REFERENCES WordKey(id) ON DELETE CASCADE
);
)

CREATE TABLE IF NOT EXISTS DocumentCategory(
    id_document INTEGER,
    id_category INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_document, id_category),
    FOREIGN KEY (id_document) REFERENCES Document(id) ON DELETE CASCADE,
    FOREIGN KEY (id_category) REFERENCES Category(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DocumentCollection(
    id_document INTEGER,
    id_collection INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_document, id_collection),
    FOREIGN KEY (id_document) REFERENCES Document(id) ON DELETE CASCADE,
    FOREIGN KEY (id_collection) REFERENCES Collection(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DocumentTag(
    id_document INTEGER,
    id_tag INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_document, id_tag),
    FOREIGN KEY (id_document) REFERENCES Document(id) ON DELETE CASCADE,
    FOREIGN KEY (id_tag) REFERENCES Tag(id) ON DELETE CASCADE
);

-- Triggers para las diferentes tablas --
-- ----------------------------------- --

-- Trigger para Document
CREATE TRIGGER IF NOT EXISTS trig_document_updated 
AFTER UPDATE ON Document
BEGIN
    UPDATE Document 
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Trigger para BibliographyData
CREATE TRIGGER IF NOT EXISTS trig_bibliography_updated 
AFTER UPDATE ON BibliographyData
BEGIN
    UPDATE BibliographyData 
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Trigger para validar extensiones permitidas
CREATE TRIGGER IF NOT EXISTS trig_document_extension_check
BEFORE INSERT ON Document
BEGIN
    SELECT CASE
        WHEN NEW.extension NOT IN ('pdf', 'doc', 'docx', 'txt', 'epub')
        THEN RAISE(ABORT, 'Extensión de archivo no válida')
    END;
END;

-- Trigger para BibliographyComplementary
CREATE TRIGGER IF NOT EXISTS trig_bibliography_complementary_updated 
AFTER UPDATE ON BibliographyComplementary
BEGIN
    UPDATE BibliographyComplementary 
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Índices para mejorar la búsqueda --
-- -------------------------------- --

CREATE INDEX idx_document_hash ON Document(hash);
CREATE INDEX idx_document_extension ON Document(extension);
CREATE INDEX idx_document_name ON Document(name);
CREATE INDEX idx_bibliography_title ON BibliographyData(title);
CREATE INDEX idx_bibliography_year ON BibliographyData(year_publication);
CREATE INDEX idx_favorite_document ON Favorite(id_doc);
CREATE INDEX idx_category_name ON Category(name);
CREATE INDEX idx_collection_name ON Collection(name);
CREATE INDEX idx_tag_name ON Tag(name);
CREATE INDEX idx_chapter_doc ON Chapter(id_doc);
CREATE INDEX idx_chapter_number ON Chapter(number_chapter);
CREATE INDEX idx_subsection_chapter ON SubSection(id_chapter); -- Renamed index
CREATE INDEX idx_subsection_level ON SubSection(level);       -- Renamed index