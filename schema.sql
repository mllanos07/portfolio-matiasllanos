-- Crear base de datos
CREATE DATABASE IF NOT EXISTS portafolio_matias
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE portafolio_matias;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    full_name VARCHAR(100) NOT NULL
);

-- Hash SHA-256 de "12345678":
-- ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f
INSERT INTO users (username, password_hash, full_name)
VALUES ('matias',
        'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f',
        'Matias Llanos');

-- Tabla "about" (Acerca de mí)
CREATE TABLE IF NOT EXISTS about (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    title VARCHAR(100) NOT NULL,
    summary TEXT NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(30),
    address VARCHAR(255),
    profile_image VARCHAR(255)
);

INSERT INTO about (full_name, title, summary, email, phone, address, profile_image)
VALUES (
    'Matias Llanos',
    'Full Stack Developer Jr.',
    'Soy una persona que intenta ser cada dia mas responsable, proactiva y con muchas ganas de aprender. Me gusta trabajar en equipo y siempre estoy buscando maneras creativas de resolver problemas. En mi tiempo libre voy al gimnasio, lo que me ayuda a mantener disciplina, constancia y un buen estado físico y mental. Busco una oportunidad para seguir desarrollándome personal y profesionalmente.',
    'matiasjoel.llanos@gmail.com',
    '+54 9 351 1234567',
    'Los Durmientes 999',
    'img/matias-logo.png'
);

-- Experiencia laboral
CREATE TABLE IF NOT EXISTS experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(100) NOT NULL,
    company VARCHAR(100) NOT NULL,
    description TEXT,
    year_start INT,
    year_end INT,
    is_current TINYINT(1) DEFAULT 0
);

INSERT INTO experiences (role, company, description, year_start, year_end, is_current)
VALUES
('Empleado de lavadero de autos', 'Lavadero de Autos', 
 'Limpieza integral de vehículos (interior, exterior y motor), atención al público y organización de turnos.',
 2024, 2024, 0),
('Pintor de casa particular', 'Trabajo independiente',
 'Lijado, empapelado y aplicación de pintura en muros y techos, selección de materiales junto al cliente.',
 2025, 2025, 0);

-- Educación
CREATE TABLE IF NOT EXISTS education (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institution VARCHAR(150) NOT NULL,
    degree VARCHAR(150) NOT NULL,
    description TEXT,
    year_start INT,
    year_end INT
);

INSERT INTO education (institution, degree, description, year_start, year_end)
VALUES (
    'Instituto Técnico Renault',
    'Nivel secundario con orientación en Informática',
    'Conocimientos en programación, redes, sistemas operativos, hardware, mantenimiento de equipos y proyectos grupales de desarrollo de software.',
    2023,
    2026
),
(
    'Curso de Python - Codo a Codo 4.0',
    'Curso introductorio de programación en Python',
    'Aprendizaje de conceptos básicos de programación, estructuras de datos, control de flujo y desarrollo de pequeños proyectos en Python.',
    2023,
    2023
);

-- Skills (hard, soft, idiomas)
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level INT NOT NULL,              -- 0 a 100
    type ENUM('hard','soft','language') NOT NULL DEFAULT 'hard'
);

INSERT INTO skills (name, level, type) VALUES
('Resolución de problemas', 85, 'soft'),
('Trabajo en equipo', 60, 'soft'),
('Adaptación rápida', 80, 'soft'),
('Comunicación efectiva', 70, 'soft'),
('Python básico', 80, 'hard'),
('HTML y CSS', 70, 'hard'),
('JavaScript básico', 80, 'hard'),
('SQL básico', 55, 'hard'),
('Redes y sistemas', 55, 'hard'),
('Español', 100, 'language'),
('Inglés', 65, 'language');

-- Proyectos
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    date_label VARCHAR(50),
    description TEXT,
    link VARCHAR(255)
);

INSERT INTO projects (name, date_label, description, link) VALUES
('Portfolio web del secundario', '2025',
 'Aplicación web desarrollada con Flask para presentar datos personales, formación académica y experiencia, funcionando como portfolio profesional.',
 'https://github.com/mllanos07/portfolio-matias.git'),
('Aplicación Copa Renault', '2025',
 'Sistema web para la gestión de la Copa Renault 2026, incluyendo administración de equipos, resultados y organización general del torneo.',
 'https://github.com/mllanos07/copa-renault.git'),
('Simulador de cobro', '2025',
 'Aplicación que simula el proceso de cobro, permitiendo practicar operaciones básicas y el flujo de atención a clientes.',
 'https://github.com/mllanos07/app_cobro.git'),
('Aula virtual', '2025',
 'Plataforma tipo aula virtual para la gestión de cursos, materiales y tareas, desarrollada como proyecto escolar.',
 'https://github.com/mllanos07/aula-virtual.git'),
('Taller mecánico', '2025',
 'Sitio web desarrollado con Python y Django para mostrar los servicios de un taller mecánico y administrar sus empleados y turnos.',
 'https://github.com/mllanos07/taller-mecanico-django.git');

-- Redes sociales
CREATE TABLE IF NOT EXISTS social_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    url VARCHAR(255) NOT NULL,
    icon_class VARCHAR(100) NOT NULL
);

INSERT INTO social_links (platform, url, icon_class) VALUES
('GitHub', 'https://github.com/mllanos07', 'fab fa-github'),
('LinkedIn', 'https://www.linkedin.com/in/tu-perfil', 'fab fa-linkedin'),
('Instagram', 'https://www.instagram.com/matias.llanoss_', 'fab fa-instagram');
