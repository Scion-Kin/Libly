-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS db;
CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'pwd';
GRANT ALL PRIVILEGES ON `db`.* TO 'user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'user'@'localhost';

-- set up the pool table
CREATE TABLE IF NOT EXISTS db.`pool`(`user_id` VARCHAR(128), `code` INT(20));

FLUSH PRIVILEGES;
