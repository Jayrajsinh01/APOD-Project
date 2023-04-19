DROP TABLE IF EXISTS apod_data;

CREATE TABLE apod_data (
    id TEXT PRIMARY KEY,
    title TEXT,
    explanation TEXT,
    img_path TEXt,
    SHA_hash TEXT
);
