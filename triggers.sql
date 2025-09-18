USE `lab_5`;

-- Drop existing triggers if they exist
DROP TRIGGER IF EXISTS equipment_type_update;
DROP TRIGGER IF EXISTS order_delete;
DROP TRIGGER IF EXISTS equipment_insert;
DROP TRIGGER IF EXISTS set_order_id_for_evaluation;

DELIMITER //

-- Create the trigger for equipment_type_update
CREATE TRIGGER equipment_type_update
BEFORE UPDATE ON equipment_type
FOR EACH ROW 
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Зміну даних у таблиці equipment_type заборонено.';
END;
//

-- Create the trigger for order_delete
CREATE TRIGGER order_delete
BEFORE DELETE ON user_order
FOR EACH ROW 
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Видалення даних з таблиці user_order заборонено.';
END;
//
-- Create the trigger for equipment_insert
CREATE TRIGGER equipment_insert
BEFORE INSERT ON equipment
FOR EACH ROW 
BEGIN
    IF NEW.serial_number NOT REGEXP '^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Неправильний серійний номер.';
    END IF;
END;
//

CREATE TRIGGER set_order_id_for_evaluation
BEFORE INSERT ON laser_cutter_order_evaluation
FOR EACH ROW
BEGIN
    -- Перевірка на наявність зв'язку за певною логікою
    DECLARE order_exists INT;

    -- Перевірка чи існує замовлення
    SELECT COUNT(*) INTO order_exists
    FROM laser_cutter_order
    WHERE id = NEW.order_id;

    -- Якщо замовлення не існує, встановлюємо значення за замовчуванням або генеруємо помилку
    IF order_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No matching laser_cutter_order found.';
    END IF;
END;
//
DELIMITER ;