INSERT INTO `lab_5`.`team` (`id`, `name`) VALUES
(1, 'EIR Solutions'),
(2, 'Rubicon'),
(3, 'RipCA'),
(4, 'NoName'),
(5, 'MRIYA');


INSERT INTO `lab_5`.`user` (`id`, `name`, `surname`, `email`, `team_id`) VALUES 
(1, 'John', 'Doe', 'john.doe@gmail.com', 1),
(2, 'Jane', 'Smith', 'jane.smith@gmail.com', 2),
(3, 'Michael', 'Johnson', 'michael.johnson@gmail.com', 1),
(4, 'Emily', 'Davis', 'emily.davis@gmail.com', 3),
(5, 'Robert', 'Brown', 'robert.brown@gmail.com', 2),
(6, 'Alice', 'Williams', 'alice.williams@example.com', NULL);


INSERT INTO `lab_5`.`worker_position` (`id`, `name`) VALUES
(1, 'Manager'),
(2, 'CEO'),
(3, 'Repairer'),
(4, 'Secretary');


INSERT INTO `lab_5`.`worker` (`id`, `name`, `surname`, `email`, `phone_number`, `address`, `worker_position_id`) VALUES
(1, 'Danylo', 'Hnyp', 'dan@gmail.com', 912872685, 'lviv.lviv', 2),
(2, 'Stephen', 'Ward', 'khan.naomi@yahoo.co.uk', 844542903, '086 Tiffany Circle, Holmesstad', 4),
(3, 'Nancy', 'White', 'peter.khan@yahoo.co.uk', 206432344, '55 Taylor River North Jennifertown', 1),
(4, 'Melissa', 'Jackson', 'kirsten.green@hotmail.com', 123034949, 'Studio 28 Davies Branch Rosschester', 3),
(5, 'Douglas', 'Turner', 'shannon26@hotmail.com', 148281573, '747 Bradley Ridge Wendystad', 3),
(6, 'John', 'Miller', 'npatel@hotmail.com', 230873695, '24 Joseph Bypass New Williamview', 1),
(7, 'Tyler', 'Turner', 'alison25@gmail.com', 893931452, 'Flat 41 Robinson Trafficway Port Wayne', 4),
(8, 'Laura', 'Johnson', 'LauraTJohnson@rhyta.com', 215379082, '830 Shinn Street New York', 3);


INSERT INTO `lab_5`.`equipment_type` (`id`, `name`) VALUES
(1, '3D Printer'),
(2, '3D Scanner'),
(3, 'Microscope'),
(4, 'Soldering iron'),
(5, 'Microcontroller'),
(6, 'CNC milling');


INSERT INTO `lab_5`.`equipment_condition` (`id`, `name`) VALUES
(1, 'Need repair'),
(2, 'Good'),
(3, 'Excellent'),
(4, 'Brand new'),
(5, 'Bad'),
(6, 'Normal');


INSERT INTO `lab_5`.`equipment` (`id`, `model`, `serial_number`, `equipment_type_id`, `equipment_condition_id`) VALUES
(1, 'Creality K1C', 'BX8C-LJFH-59MV-RWJQ', 1, 2),
(2, 'Elegoo Neptune 4 Pro', 'N89W-TBV3-FCCG-QSYG', 1, 4),
(3, '3DMakerpro Whale', 'C626-76SF-Z7F6-2DKU', 2, 6),
(4, 'Bambu Lab X1 Carbon', 'KLHZ-KEJF-LCKL-WBGL', 2, 3),
(5, 'Bresser Trino Researcher', 'LQ7N-K5CE-YW2M-CSMP', 3, 6),
(6, 'YIHUA 853AAA', 'FY6E-V3DC-VR7W-P5ZK', 4, 6),
(7, 'Baku BA-8702D', 'W5QD-ZGVZ-PKQS-AZVB', 4, 1),
(8, 'Ersa i-CON 1V MK2', '6YPR-RFRE-8B9F-WPC5', 4, 2),
(9, 'Ersa i-CON 1V MK2', 'L9P2-YZCE-BWDC-J4GN', 4, 4),
(10, 'Ersa i-CON 1V MK2', '8JD3-EZ4F-GFC3-7NDN', 4, 4),
(11, 'Dnipro-M ЕR-210LX', 'RXQG-ZN6M-7YBV-T5TR', 6, 6),
(12, 'Arduino Uno', '46MS-L3QY-T2YZ-J35A', 5, 2),
(13, 'Arduino Uno', 'YJ2D-GMLC-Z82G-MPRV', 5, 2),
(14, 'Arduino Uno', '53QS-A4RB-DYCE-84V6', 5, 5),
(15, 'ESP32', '3HNU-NU4B-7W9X-3ZF2', 5, 2),
(16, 'ESP32', 'T5ZT-24VL-JSVM-42KU', 5, 4),
(17, 'Raspberry Pi Pico', '35B7-HQYA-X9MX-P6T8', 5, 1),
(18, 'STM32 Nucleo', '5QUZ-CXEF-SEHV-K7MW', 5, 6);


INSERT INTO `lab_5`.`equipment_repair` (`id`, `date_of_repair`, `worker_id`, `equipment_id`) VALUES
(1, '2023-09-21', 4, 3),
(2, '2023-05-24', 5, 5),
(3, '2024-11-01', 4, 11),
(4, '2022-03-10', 8, 15);


INSERT INTO `lab_5`.`user_order` (`id`, `user_id`, `equipment_id`, `time_of_order`) VALUES
(1, 1, 4, '2023-02-15 14:20:31'),
(2, 1, 6, '2023-07-11 09:45:16'),
(3, 6, 11, '2023-11-23 17:10:09'),
(4, 2, 15, '2024-01-05 08:35:52'),
(5, 3, 2, '2024-03-19 12:00:41'),
(6, 3, 18, '2023-06-27 19:25:38'),
(7, 5, 7, '2023-10-12 11:40:22'),
(8, 4, 8, '2024-04-21 15:15:18'),
(9, 1, 11, '2023-08-05 16:32:50'),
(10, 4, 4, '2024-02-28 09:55:45'),
(11, 2, 13, '2023-12-14 18:20:33'),
(12, 2, 18, '2023-05-22 10:48:19'),
(13, 1, 9, '2023-09-30 14:12:26'),
(14, 5, 4, '2023-04-10 13:23:05'),
(15, 3, 10, '2024-06-16 10:04:37'),
(16, 6, 3, '2023-03-03 20:50:11');


INSERT INTO `lab_5`.`laser_cutter` (`id`, `model`, `serial_number`, `equipment_condition_id`) VALUES
(1, 'LaserMaster X500', '73P6-3BUC-PDWG-UH3P', 3),
(2, 'PrecisionCut Pro 3000', '8XHJ-JFA3-SHRK-88E4', 5),
(3, 'UltraBeam S200', 'VT7A-KAFQ-2Y3S-VYHU', 6),
(4, 'UltraBeam S200', 'N8PQ-FYV8-CY2P-WR6T', 6);


INSERT INTO `lab_5`.`laser_cutter_order` (`id`, `time_of_start`, `time_of_end`, `user_id`, `laser_cutter_id`) VALUES
(1, '2023-01-15 09:15:10', '2023-01-15 10:15:45', 1, 3),
(2, '2023-03-22 14:25:30', '2023-03-22 15:45:50', 4, 1),
(3, '2023-05-10 11:10:20', '2023-05-10 12:50:00', 2, 4),
(4, '2023-07-17 08:45:15', '2023-07-17 10:00:32', 5, 2),
(5, '2023-09-28 16:30:45', '2023-09-28 17:30:10', 3, 1),
(6, '2023-12-03 09:20:33', '2023-12-03 10:35:42', 6, 2),
(7, '2024-02-19 12:00:10', '2024-02-19 13:25:18', 4, 3),
(8, '2024-04-11 14:10:35', '2024-04-11 15:50:45', 1, 4),
(9, '2024-06-05 11:35:25', '2024-06-05 12:40:33', 5, 1),
(10, '2024-08-22 13:40:20', '2024-08-22 15:00:55', 3, 4),
(11, '2023-11-15 09:15:50', '2023-11-15 10:30:20', 6, 2),
(12, '2024-01-08 10:05:15', '2024-01-08 11:45:32', 2, 3),
(13, '2023-04-18 14:55:22', '2023-04-18 16:20:35', 4, 4),
(14, '2023-07-29 09:40:13', '2023-07-29 10:55:19', 1, 2),
(15, '2023-10-12 11:25:45', '2023-10-12 12:30:48', 5, 1),
(16, '2024-03-14 12:15:30', '2024-03-14 13:40:22', 6, 3);


INSERT INTO `lab_5`.`laser_cutter_repair` (`id`, `date_of_repair`, `worker_id`, `laser_cutter_id`) VALUES
(1, '2023-05-17', 5, 3),
(2, '2023-08-13', 4, 3),
(3, '2024-03-01', 5, 3),
(4, '2024-08-29', 8, 3);


INSERT INTO `lab_5`.`laser_cutter_order_evaluations` (`order_id`, `quality_score`) VALUES
    (1, 8),
    (2, 9),
    (3, 7),
    (4, 6),
    (5, 9),
    (6, 10),
    (7, 8),
    (8, 7),
    (9, 6),
    (10, 8);
