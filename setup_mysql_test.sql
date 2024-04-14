-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS libly;
CREATE USER IF NOT EXISTS 'libly_test_user'@'localhost' IDENTIFIED BY 'libDevTest';
GRANT ALL PRIVILEGES ON `libly_test`.* TO 'libly_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
