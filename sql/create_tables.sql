CREATE DATABASE IF NOT EXISTS weather_db;

USE weather_db;

CREATE TABLE IF NOT EXISTS weather_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    regiao VARCHAR(255),
    data DATE,
    raw_data JSON,
    CONSTRAINT uq_raw_regiao_data UNIQUE (regiao, data)
);

CREATE TABLE IF NOT EXISTS weather_daily (
    id INT AUTO_INCREMENT PRIMARY KEY,
    regiao VARCHAR(255),
    data DATE,
    temperatura_maxima FLOAT,
    temperatura_minima FLOAT,
    precipitacao_total FLOAT,
    amplitude_termica FLOAT,
    CONSTRAINT uq_regiao_data UNIQUE (regiao, data)
);