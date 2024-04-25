-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS libly;
CREATE USER IF NOT EXISTS 'libly_user'@'localhost' IDENTIFIED BY 'libDev';
GRANT ALL PRIVILEGES ON `libly`.* TO 'libly_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'libly'@'localhost';
FLUSH PRIVILEGES;
