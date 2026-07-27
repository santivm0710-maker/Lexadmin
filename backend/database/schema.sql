-- Esquema generado a partir de backend/entities/*.py
-- Refleja el modelo de datos que ya usa el backend. Sin datos semilla:
-- las tablas quedan vacías y se llenan mediante la aplicación (API/frontend).

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    correo VARCHAR(150),
    caso_relacionado VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS casos (
    id_caso INT AUTO_INCREMENT PRIMARY KEY,
    numero_expediente VARCHAR(50) NOT NULL,
    id_cliente INT NOT NULL,
    tipo_caso VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    prioridad VARCHAR(20) NOT NULL,
    abogado_responsable VARCHAR(150),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS expedientes (
    id_expediente INT AUTO_INCREMENT PRIMARY KEY,
    id_caso INT NOT NULL,
    nombre_documento VARCHAR(200) NOT NULL,
    tipo_documento VARCHAR(100) NOT NULL,
    ruta_archivo VARCHAR(255),
    estado_ocr VARCHAR(50) DEFAULT 'Pendiente',
    FOREIGN KEY (id_caso) REFERENCES casos(id_caso)
);

CREATE TABLE IF NOT EXISTS agenda (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_caso INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    actividad VARCHAR(150) NOT NULL,
    lugar VARCHAR(150),
    prioridad VARCHAR(20),
    FOREIGN KEY (id_caso) REFERENCES casos(id_caso)
);

CREATE TABLE IF NOT EXISTS informacion_judicial (
    id_info_judicial INT AUTO_INCREMENT PRIMARY KEY,
    id_caso INT NOT NULL,
    juzgado VARCHAR(150) NOT NULL,
    juez VARCHAR(150),
    fiscal VARCHAR(150),
    contacto_institucional VARCHAR(150),
    FOREIGN KEY (id_caso) REFERENCES casos(id_caso)
);

CREATE TABLE IF NOT EXISTS bitacora (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL,
    actor VARCHAR(100) NOT NULL,
    modulo VARCHAR(100) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    detalle TEXT
);
