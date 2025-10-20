-- Datos de los Documentos --
-- ----------------------- --

-- Tabla de Documentos
/*
    Esta tabla contendrá información más relevante
    sobre los documentos
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

-- Tabla BibliographyData
/*
    Esta tabla contendrá los datos bibliográficos del
    documento
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
    Esta tabla contendrá los datos complementarios a la
    bibliografía del documento
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
    word TEXT NOT NULL,
    description TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id AUTOINCREMENT)
);
);

-- Tabla Tag
/*
    Esta tabla sirve para organizar los documentos por
    etiquetas de acuerdo a la preferencia del usuario
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