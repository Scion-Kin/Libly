-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS db;
CREATE USER IF NOT EXISTS 'username'@'localhost' IDENTIFIED BY 'pwd';
GRANT ALL PRIVILEGES ON `db`.* TO 'username'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'username'@'localhost';

-- set up the pool table
CREATE TABLE IF NOT EXISTS db.`pool`(`user_id` VARCHAR(128), `code` INT(20));

FLUSH PRIVILEGES;
