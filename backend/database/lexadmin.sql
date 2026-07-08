CREATE DATABASE IF NOT EXISTS lexadmin;
USE lexadmin;

-- ==========================================
-- CLIENTES
-- ==========================================

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,

    nombre_completo VARCHAR(150) NOT NULL,
    identificacion VARCHAR(30) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    correo VARCHAR(120),

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- ==========================================
-- CASOS
-- ==========================================

CREATE TABLE casos (

    id_caso INT AUTO_INCREMENT PRIMARY KEY,

    id_cliente INT NOT NULL,

    numero_expediente VARCHAR(60) NOT NULL UNIQUE,

    tipo_proceso VARCHAR(100),

    estado VARCHAR(50),

    juzgado VARCHAR(150),

    descripcion TEXT,

    fecha_inicio DATE,

    fecha_cierre DATE,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)

);



-- ==========================================
-- AGENDA
-- ==========================================

CREATE TABLE agenda (

    id_agenda INT AUTO_INCREMENT PRIMARY KEY,

    id_caso INT NOT NULL,

    fecha DATE NOT NULL,

    hora TIME NOT NULL,

    actividad VARCHAR(150),

    lugar VARCHAR(150),

    prioridad VARCHAR(30),

    observaciones TEXT,

    FOREIGN KEY (id_caso)
        REFERENCES casos(id_caso)

);



-- ==========================================
-- EXPEDIENTES
-- ==========================================

CREATE TABLE expedientes (

    id_expediente INT AUTO_INCREMENT PRIMARY KEY,

    id_cliente INT NOT NULL,

    id_caso INT NOT NULL,

    nombre_documento VARCHAR(200),

    tipo_documento VARCHAR(100),

    ruta_pdf VARCHAR(255),

    estado_ocr VARCHAR(50),

    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    FOREIGN KEY (id_caso)
        REFERENCES casos(id_caso)

);



-- ==========================================
-- BITÁCORA
-- ==========================================

CREATE TABLE bitacora (

    id_bitacora INT AUTO_INCREMENT PRIMARY KEY,

    fecha DATE,

    hora TIME,

    actor VARCHAR(120),

    modulo VARCHAR(100),

    accion VARCHAR(200),

    descripcion TEXT

);