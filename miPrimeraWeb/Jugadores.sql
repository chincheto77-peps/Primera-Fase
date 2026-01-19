CREATE DATABASE IF NOT EXISTS ciber;
USE ciber;

CREATE TABLE IF NOT EXISTS equipos(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL 
);
CREATE TABLE IF NOT EXISTS jugadores(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    valor_de_mercado DECIMAL(9,2) NOT NULL,
	foto VARCHAR(255),
    estadisticas VARCHAR(255),
    equipo BIGINT UNSIGNED
);
CREATE TABLE IF NOT EXISTS usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS titulos(
	nombre VARCHAR(100) NOT NULL PRIMARY KEY,
    fecha DATE NOT NULL,
    equipo BIGINT UNSIGNED
);
INSERT INTO `usuarios` (`usuario`, `clave`, `perfil`) VALUES ('root','1234', 'admin');

INSERT INTO `equipos` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Atlético Solaris', 'Club de la ciudad de Solaris'),
(2, 'Real Monteverde', 'Equipo histórico de Monteverde'),
(3, 'Deportivo Norte', 'Club emergente del norte');

INSERT INTO `jugadores` (`nombre`, `descripcion`, `valor_de_mercado`, `foto`, `estadisticas`, `equipo`) VALUES
('Luis Gómez', 'Delantero veloz', 1250000.00, '/imagenes/luis_gomez.jpg', 'goles:15,asistencias:5', 1),
('Miguel Fernández', 'Centrocampista creativo', 900000.00, '/imagenes/miguel_fernandez.jpg', 'pases_clave:40', 2),
('Carlos Ruiz', 'Defensa central sólido', 750000.00, '/imagenes/carlos_ruiz.jpg', 'intercepciones:60', 3),
('Javier López', 'Portero joven', 600000.00, '/imagenes/javier_lopez.jpg', 'paradas:80', 1),
('Andrés Morales', 'Extremo habilidoso', 1100000.00, '/imagenes/andres_morales.jpg', 'regates:50', 2);

INSERT INTO `titulos` (`nombre`, `fecha`, `equipo`) VALUES
('Copa Solaris', '2023-06-20', 1),
('Liga Monteverde', '2022-12-15', 2),
('Supercopa Norte', '2024-03-10', 3);

-- Asegúrate de que las tablas usan InnoDB (necesario para FK)
ALTER TABLE equipos ENGINE=InnoDB;
ALTER TABLE jugadores ENGINE=InnoDB;
ALTER TABLE titulos ENGINE=InnoDB;

-- Permitir NULL en las columnas equipo para poder usar ON DELETE SET NULL
ALTER TABLE jugadores MODIFY COLUMN equipo BIGINT UNSIGNED NULL;
ALTER TABLE titulos MODIFY COLUMN equipo BIGINT UNSIGNED NULL;

-- Añadir claves foráneas
ALTER TABLE jugadores
    ADD CONSTRAINT fk_jugadores_equipo
    FOREIGN KEY (equipo) REFERENCES equipos(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE titulos
    ADD CONSTRAINT fk_titulos_equipo
    FOREIGN KEY (equipo) REFERENCES equipos(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;
