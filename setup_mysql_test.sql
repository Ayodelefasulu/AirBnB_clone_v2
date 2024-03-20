-- My setup test file
-- Create a database name hbnb_test
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a new user 'hbnb_test', on localhost, with password 'hbnb_test_pwd'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the HBNB_TEST_DB to hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_test user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
