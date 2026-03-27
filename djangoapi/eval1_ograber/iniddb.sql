CREATE DATABASE exam;

-- Conectarse a la base de datos (asegúrate de haberla creado antes en pgAdmin, ej. 'exam')
CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. Tabla de Polígonos (Zonas)
CREATE TABLE zonas (
    id serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    tipo varchar(100),
    area double precision,
    perimetro double precision,
    responsable varchar(100),
    geom geometry(POLYGON, 25830)
);

-- 2. Tabla de Líneas (Caminos)
CREATE TABLE caminos (
    id serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    dificultad varchar(50),
    longitud double precision,
    ancho double precision,
    material varchar(100),
    geom geometry(LINESTRING, 25830)
);

-- 3. Tabla de Puntos (Árboles)
CREATE TABLE arboles (
    id serial PRIMARY KEY,
    especie varchar(100) NOT NULL,
    altura double precision,
    diametro double precision,
    edad integer,
    estado varchar(50),
    geom geometry(POINT, 25830)
);