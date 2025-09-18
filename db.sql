CREATE SCHEMA IF NOT EXISTS `lab_5` DEFAULT CHARACTER SET utf8;
USE `lab_5`;

DROP TABLE IF EXISTS laser_cutter_order;
DROP TABLE IF EXISTS laser_cutter_repair;
DROP TABLE IF EXISTS laser_cutter;
DROP TABLE IF EXISTS equipment_repair;
DROP TABLE IF EXISTS user_order;
DROP TABLE IF EXISTS worker;
DROP TABLE IF EXISTS worker_position;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS equipment_condition;
DROP TABLE IF EXISTS equipment_type;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS team;


CREATE TABLE IF NOT EXISTS team (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) UNIQUE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    surname VARCHAR(45) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    team_id INT,
    INDEX idx_team_id (team_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS equipment_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS equipment_condition (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(45) NOT NULL,
    serial_number VARCHAR(45) NOT NULL UNIQUE,
    equipment_type_id INT NOT NULL,
    equipment_condition_id INT NOT NULL,
    INDEX idx_equipment_type (equipment_type_id),
    INDEX idx_equipment_condition (equipment_condition_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS worker_position (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS worker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    surname VARCHAR(45) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number INT NOT NULL UNIQUE,
    address VARCHAR(100) NOT NULL,
    worker_position_id INT NOT NULL,
    INDEX idx_position_id (worker_position_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS user_order (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    time_of_order DATETIME NOT NULL,
    INDEX idx_equipment_id (equipment_id),
    INDEX idx_user_id (user_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS equipment_repair (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_repair DATETIME NOT NULL,
    worker_id INT NOT NULL,
    equipment_id INT NOT NULL,
    INDEX idx_worker_id (worker_id),
    INDEX idx_equipment_id_repair (equipment_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS laser_cutter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(45),
    serial_number VARCHAR(45) UNIQUE,
    equipment_condition_id INT NOT NULL,
    INDEX idx_laser_condition (equipment_condition_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS laser_cutter_repair (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_repair DATETIME NOT NULL,
    worker_id INT NOT NULL,
    laser_cutter_id INT NOT NULL,
    INDEX idx_worker_laser_repair (worker_id),
    INDEX idx_laser_cutter_id (laser_cutter_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS laser_cutter_order (
    id INT AUTO_INCREMENT PRIMARY KEY,
    time_of_start DATETIME NOT NULL,
    time_of_end DATETIME NOT NULL,
    user_id INT NOT NULL,
    laser_cutter_id INT NOT NULL,
    INDEX idx_user_laser_order (user_id),
    INDEX idx_laser_cutter_order_id (laser_cutter_id)
) ENGINE = InnoDB;

ALTER TABLE user 
    ADD CONSTRAINT fk_user_team FOREIGN KEY (team_id) REFERENCES team (id);

ALTER TABLE equipment 
    ADD CONSTRAINT fk_equipment_type FOREIGN KEY (equipment_type_id) REFERENCES equipment_type (id),
    ADD CONSTRAINT fk_equipment_condition FOREIGN KEY (equipment_condition_id) REFERENCES equipment_condition (id);

ALTER TABLE worker 
    ADD CONSTRAINT fk_worker_position FOREIGN KEY (worker_position_id) REFERENCES worker_position (id);

ALTER TABLE user_order 
    ADD CONSTRAINT fk_order_user FOREIGN KEY (user_id) REFERENCES user (id),
    ADD CONSTRAINT fk_order_equipment FOREIGN KEY (equipment_id) REFERENCES equipment (id);

ALTER TABLE equipment_repair 
    ADD CONSTRAINT fk_repair_worker FOREIGN KEY (worker_id) REFERENCES worker (id),
    ADD CONSTRAINT fk_repair_equipment FOREIGN KEY (equipment_id) REFERENCES equipment (id);

ALTER TABLE laser_cutter 
    ADD CONSTRAINT fk_laser_condition FOREIGN KEY (equipment_condition_id) REFERENCES equipment_condition (id);

ALTER TABLE laser_cutter_repair 
    ADD CONSTRAINT fk_laser_repair_worker FOREIGN KEY (worker_id) REFERENCES worker (id),
    ADD CONSTRAINT fk_laser_repair_cutter FOREIGN KEY (laser_cutter_id) REFERENCES laser_cutter (id);

ALTER TABLE laser_cutter_order 
    ADD CONSTRAINT fk_laser_order_user FOREIGN KEY (user_id) REFERENCES user (id),
    ADD CONSTRAINT fk_laser_order_cutter FOREIGN KEY (laser_cutter_id) REFERENCES laser_cutter (id);

