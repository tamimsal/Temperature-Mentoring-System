CREATE DATABASE switch_db;

CREATE USER 'tamim'@'localhost' IDENTIFIED BY '22585933';
GRANT ALL PRIVILEGES ON switch_db.* TO 'tamim'@'localhost';
FLUSH PRIVILEGES;

USE switch_db;

CREATE TABLE switches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    switch_name VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255) NOT NULL
);

INSERT INTO switches (switch_name, ip_address) VALUES 
('Switch1', '192.168.1.11'),
('Switch2', '192.168.1.12'),
('Switch3', '192.168.1.13'),
('Switch4', '192.168.1.14'),
('Switch5', '192.168.1.15');
