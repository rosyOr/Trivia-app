-- 1) Esquema base
CREATE DATABASE IF NOT EXISTS trivia
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE trivia;

-- 2) Catálogos
CREATE TABLE categoria (
  categoria_id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE dificultad (
  dificultad_id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 3) Imágenes / API externa
CREATE TABLE proveedor_api (
  proveedor_id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE imagen (
  imagen_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  proveedor_id INT NOT NULL,
  alto INT,
  alt_text VARCHAR(255),
  fecha_descarga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_imagen_proveedor
    FOREIGN KEY (proveedor_id) REFERENCES proveedor_api(proveedor_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 4) Modelo de juego y usuarios
CREATE TABLE jugador (
  jugador_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  alias VARCHAR(50) NOT NULL,
  fecha_alta TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_jugador_alias UNIQUE(alias)
) ENGINE=InnoDB;

CREATE TABLE pregunta (
  pregunta_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  enunciado TEXT NOT NULL,
  categoria_id INT NOT NULL,
  dificultad_id INT NOT NULL,
  imagen_id BIGINT NULL,
  CONSTRAINT fk_pregunta_categoria FOREIGN KEY (categoria_id)
    REFERENCES categoria(categoria_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pregunta_dificultad FOREIGN KEY (dificultad_id)
    REFERENCES dificultad(dificultad_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pregunta_imagen FOREIGN KEY (imagen_id)
    REFERENCES imagen(imagen_id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE opcion_respuesta (
  opcion_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  pregunta_id BIGINT NOT NULL,
  texto VARCHAR(500) NOT NULL,
  es_correcta BOOLEAN NOT NULL,
  CONSTRAINT fk_opcion_pregunta FOREIGN KEY (pregunta_id)
    REFERENCES pregunta(pregunta_id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE partida (
  partida_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  jugador_id BIGINT NOT NULL,
  fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_fin TIMESTAMP NULL,
  categoria_id INT NULL,
  dificultad_id INT NULL,
  num_preguntas INT NULL,
  puntaje_total INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_partida_jugador FOREIGN KEY (jugador_id)
    REFERENCES jugador(jugador_id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_partida_categoria FOREIGN KEY (categoria_id)
    REFERENCES categoria(categoria_id) ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_partida_dificultad FOREIGN KEY (dificultad_id)
    REFERENCES dificultad(dificultad_id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE partida_pregunta (
  partida_id BIGINT NOT NULL,
  pregunta_id BIGINT NOT NULL,
  nro_orden INT NOT NULL,
  PRIMARY KEY (partida_id, pregunta_id),
  CONSTRAINT fk_pp_partida FOREIGN KEY (partida_id)
    REFERENCES partida(partida_id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_pp_pregunta FOREIGN KEY (pregunta_id)
    REFERENCES pregunta(pregunta_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT uq_pp_orden UNIQUE (partida_id, nro_orden)
) ENGINE=InnoDB;

CREATE TABLE respuesta (
  respuesta_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  partida_id BIGINT NOT NULL,
  pregunta_id BIGINT NOT NULL,
  opcion_id BIGINT NOT NULL,
  es_correcta BOOLEAN NOT NULL,
  puntos_otorgados INT NOT NULL DEFAULT 0,
  respondida_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_resp_partida FOREIGN KEY (partida_id)
    REFERENCES partida(partida_id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_resp_pregunta FOREIGN KEY (pregunta_id)
    REFERENCES pregunta(pregunta_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_resp_opcion FOREIGN KEY (opcion_id)
    REFERENCES opcion_respuesta(opcion_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 5) Vistas de ranking y puntajes
CREATE OR REPLACE VIEW vw_ranking_top10 AS
SELECT
  j.alias,
  MAX(p.puntaje_total) AS mejor_puntaje_partida
FROM partida p
JOIN jugador j ON j.jugador_id = p.jugador_id
WHERE p.estado = 'finalizada'
GROUP BY j.alias
ORDER BY mejor_puntaje_partida DESC
LIMIT 10;

CREATE OR REPLACE VIEW vw_puntaje_acumulado AS
SELECT
  j.jugador_id,
  j.alias,
  COALESCE(SUM(r.puntos_otorgados),0) AS puntaje_acumulado
FROM jugador j
LEFT JOIN partida p ON p.jugador_id = j.jugador_id
LEFT JOIN respuesta r ON r.partida_id = p.partida_id
GROUP BY j.jugador_id, j.alias;

-- 1) Agrego la columna para el texto fuente (inglés)
ALTER TABLE pregunta
  ADD COLUMN enunciado_src_en TEXT NULL AFTER enunciado;

-- 2) Agrego la columna HASH generada desde el texto fuente
ALTER TABLE pregunta
  ADD COLUMN enunciado_hash_en CHAR(64)
    GENERATED ALWAYS AS (SHA2(enunciado_src_en, 256)) STORED;

-- 3) Hago único el hash (evita duplicados)
CREATE UNIQUE INDEX uq_preg_en_hash ON pregunta(enunciado_hash_en);

SELECT p.pregunta_id, p.enunciado
FROM pregunta p
JOIN categoria c ON p.categoria_id = c.categoria_id
WHERE c.categoria_id = 6
GROUP BY p.pregunta_id
ORDER BY p.pregunta_id ASC;

SELECT p.enunciado, COUNT(*) AS total
FROM pregunta p
GROUP BY p.enunciado;

SELECT enunciado_hash_en, COUNT(*) AS c
FROM pregunta
WHERE enunciado_hash_en IS NOT NULL
GROUP BY enunciado_hash_en
HAVING COUNT(*) > 1;

SELECT COUNT(*) AS sin_src_o_hash
FROM pregunta
WHERE enunciado_src_en IS NULL OR enunciado_hash_en IS NULL;
