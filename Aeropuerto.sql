CREATE DATABASE aeropuerto_database;
USE aeropuerto_database;

CREATE TABLE avion(
id_avion INT PRIMARY KEY,
modelo VARCHAR(60),
matricula VARCHAR(20),
anio_fabricacion INT,
estado_avion VARCHAR(20),
capacidad_total INT);

CREATE TABLE clase(
id_clase INT PRIMARY KEY,
codigo_clase VARCHAR(5),
nombre_clase VARCHAR(40));

CREATE TABLE aeropuerto(
id_aeropuerto INT PRIMARY KEY,
codigo_iata VARCHAR(10),
nombre VARCHAR(100),
ciudad VARCHAR(60),
pais VARCHAR(60));

CREATE TABLE ruta(
id_ruta INT PRIMARY KEY,
aeropuerto_origen INT,
aeropuerto_destino INT,
FOREIGN KEY (aeropuerto_origen) REFERENCES aeropuerto (id_aeropuerto),
FOREIGN KEY (aeropuerto_destino) REFERENCES aeropuerto (id_aeropuerto)
 );

CREATE TABLE cabina(
id_cabina INT PRIMARY KEY,
id_avion INT,
id_clase INT,
capacidad_cabina INT,
nombre_cabina VARCHAR(40),
FOREIGN KEY (id_avion) REFERENCES avion (id_avion),
FOREIGN KEY (id_clase) REFERENCES clase (id_clase));

CREATE TABLE vuelo_programado(
id_vuelo_programado INT PRIMARY KEY,
id_ruta INT,
numero_vuelo VARCHAR(10),
dias_operacion VARCHAR(20),
hora_salida_programada TIME,
hora_llegada_programada TIME,
temporada_operacion VARCHAR(20),
tipo_servicio VARCHAR(20),
tiempo_min_conexion INT,
FOREIGN KEY (id_ruta) REFERENCES ruta (id_ruta));

CREATE TABLE vuelo_instancia(
id_vuelo_instancia INT PRIMARY KEY,
id_vuelo_programado INT,
id_avion INT,
fecha_operacion DATE,
hora_salida_real DATETIME,
hora_llegada_real DATETIME,
estado_vuelo VARCHAR(20),
puerta_embarque VARCHAR(20),
clima_afectado BOOLEAN,
motivo_cancelacion TEXT,
FOREIGN KEY (id_vuelo_programado) REFERENCES vuelo_programado (id_vuelo_programado),
FOREIGN KEY (id_avion) REFERENCES avion (id_avion));

CREATE TABLE tarifa(
id_tarifa INT PRIMARY KEY,
id_clase INT,
codigo_tarifa VARCHAR(10),
precio_base DECIMAL(12,2),
moneda VARCHAR(20),
anticipacion_minima INT,
permite_cambio BOOLEAN,
permite_reembolso BOOLEAN,
restricciones TEXT,
reglas_penalizacion TEXT,
FOREIGN KEY (id_clase) REFERENCES clase (id_clase));

CREATE TABLE tarifa_vuelo(
id_tarifa_vuelo INT PRIMARY KEY,
id_vuelo_instancia INT,
id_tarifa INT,
precio_actual DECIMAL(12,2),
fecha_actualizacion DATETIME,
cupo_asignado INT,
cupo_disponible INT,
nivel_demanda VARCHAR(20),
factor_ocupacion DECIMAL(5,2),
sobreventa_permitida INT,
FOREIGN KEY (id_vuelo_instancia) REFERENCES vuelo_instancia (id_vuelo_instancia),
FOREIGN KEY (id_tarifa) REFERENCES tarifa (id_tarifa));

CREATE TABLE inventario_clase(
id_inventario INT PRIMARY KEY,
id_vuelo_instancia INT,
id_clase INT,
asientos_totales INT,
asientos_disponibles INT,
asientos_bloqueados INT,
asientos_sobrevendidos INT,
FOREIGN KEY (id_vuelo_instancia) REFERENCES vuelo_instancia (id_vuelo_instancia),
FOREIGN KEY (id_clase) REFERENCES clase (id_clase));

CREATE TABLE pasajero(
id_pasajero INT PRIMARY KEY,
nombre_completo VARCHAR(120),
genero VARCHAR(10),
fecha_nacimiento DATE,
email VARCHAR(100),
telefono VARCHAR(20),
nacionalidad VARCHAR(60),
tipo_documento VARCHAR(20),
documento_pasajero VARCHAR(30),
preferencias_vuelo TEXT,
programa_frecuente VARCHAR(30),
nivel_fidelidad VARCHAR(20),
contacto_emergencia VARCHAR(100));

CREATE TABLE pnr(
id_pnr INT PRIMARY KEY,
id_pasajero INT,
codigo_localizador VARCHAR(10),
fecha_reserva DATE,
estado_reserva VARCHAR(20),
forma_pago VARCHAR(30),
estado_pago VARCHAR(20),
monto_total DECIMAL(12,2),
fecha_limite_emision DATE,
canal_reserva VARCHAR(30),
agencia_emisora VARCHAR(60),
FOREIGN KEY (id_pasajero) REFERENCES pasajero (id_pasajero));

CREATE TABLE segmento_reserva(
id_segmento INT PRIMARY KEY,
id_pnr INT,
id_pasajero INT,
id_vuelo_instancia INT,
id_tarifa_vuelo INT,
estado_segmento VARCHAR(20),
asiento_asignado VARCHAR(6),
precio_pagado DECIMAL(12,2),
impuestos DECIMAL(10,2),
estado_checkin VARCHAR(20),
equipaje_incluido VARCHAR(30),
equipaje_adicional VARCHAR(30),
numero_ticket_electronico VARCHAR(20),
canal_vanta VARCHAR(30),
FOREIGN KEY (id_pnr) REFERENCES pnr (id_pnr),
FOREIGN KEY (id_pasajero) REFERENCES pasajero (id_pasajero),
FOREIGN KEY (id_vuelo_instancia) REFERENCES vuelo_instancia (id_vuelo_instancia),
FOREIGN KEY (id_tarifa_vuelo) REFERENCES tarifa_vuelo (id_tarifa_vuelo));