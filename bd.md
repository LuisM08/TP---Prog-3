
-- ER/Studio 8.0 SQL Code Generation
-- Company :      yo
-- Project :      DATA MODEL
-- Author :       m08luisf@gmail.com
--
-- Date Created : Saturday, May 11, 2024 17:42:09
-- Target DBMS : MySQL 5.x
--

-- 
-- TABLE: estadias 
--

CREATE TABLE estadias(
    id_estadia            INT            NOT NULL,
    total_monto          FLOAT(8, 0),
    forma_pago            INT,
    dia_estadia           INT,
    estado                INT,
    id_tipo_habitacion    INT            NOT NULL,
    PRIMARY KEY (id_estadia)
)ENGINE=MYISAM
;



-- 
-- TABLE: ingresos 
--

CREATE TABLE ingresos(
    id_ingreso            INT    NOT NULL,
    ingresos              INT,
    dias_ocupacioin       INT,
    id_tipo_habitacion    INT    NOT NULL,
    PRIMARY KEY (id_ingreso)
)ENGINE=MYISAM
;



-- 
-- TABLE: tipos_habitacion 
--

CREATE TABLE tipos_habitacion(
    id_tipo_habitacion    INT    NOT NULL,
    tipo_habitacion       INT,
    costo_diario          INT,
    PRIMARY KEY (id_tipo_habitacion)
)ENGINE=MYISAM
;



-- 
-- TABLE: estadias 
--

ALTER TABLE estadias ADD CONSTRAINT Reftipos_habitacion2 
    FOREIGN KEY (id_tipo_habitacion)
    REFERENCES tipos_habitacion(id_tipo_habitacion)
;


-- 
-- TABLE: ingresos 
--

ALTER TABLE ingresos ADD CONSTRAINT Reftipos_habitacion4 
    FOREIGN KEY (id_tipo_habitacion)
    REFERENCES tipos_habitacion(id_tipo_habitacion)
;

