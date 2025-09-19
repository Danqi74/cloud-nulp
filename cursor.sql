DROP PROCEDURE IF EXISTS create_dynamic_equipment_tables;

DELIMITER //

CREATE PROCEDURE create_dynamic_equipment_tables()
BEGIN
    DECLARE finished INT DEFAULT 0;
    DECLARE equipment_id INT;
    DECLARE model VARCHAR(100);
    DECLARE serial_number VARCHAR(100);
    DECLARE equipment_type_id INT;
    DECLARE equipment_condition_id INT;
    DECLARE cur CURSOR FOR SELECT id, model, serial_number, equipment_type_id, equipment_condition_id FROM equipment;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

    SET @table1 = CONCAT('equipment_', UNIX_TIMESTAMP(), '_1');
    SET @table2 = CONCAT('equipment_', UNIX_TIMESTAMP(), '_2');

    -- Динамічно створюємо таблиці
    SET @create_table_sql = CONCAT(
        'CREATE TABLE ', @table1, ' LIKE equipment;'
    );
    PREPARE stmt FROM @create_table_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET @create_table_sql = CONCAT(
        'CREATE TABLE ', @table2, ' LIKE equipment;'
    );
    PREPARE stmt FROM @create_table_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Відкриваємо курсор
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO equipment_id, model, serial_number, equipment_type_id, equipment_condition_id;
        IF finished THEN
            LEAVE read_loop;
        END IF;

        -- Випадковий розподіл даних між таблицями
        IF RAND() < 0.5 THEN
            SET @insert_sql = CONCAT(
                'INSERT INTO ', @table1, ' (id, model, serial_number, equipment_type_id, equipment_condition_id) ',
                'SELECT id, model, serial_number, equipment_type_id, equipment_condition_id FROM equipment WHERE id = ', equipment_id, ';'
            );
        ELSE
            SET @insert_sql = CONCAT(
                'INSERT INTO ', @table2, ' (id, model, serial_number, equipment_type_id, equipment_condition_id) ',
                'SELECT id, model, serial_number, equipment_type_id, equipment_condition_id FROM equipment WHERE id = ', equipment_id, ';'
            );
        END IF;

        PREPARE stmt FROM @insert_sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;

    -- Закриваємо курсор
    CLOSE cur;
END //

DELIMITER ;

