CREATE DATABASE IF NOT EXISTS ciber;
USE ciber;
CREATE TABLE chuches(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
	foto VARCHAR(255),
    ingredientes VARCHAR(255)
);
CREATE TABLE comentarios(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL
);
CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL
);
INSERT INTO `usuarios` (`usuario`, `clave`, `perfil`) VALUES ('root','1234', 'admin');
