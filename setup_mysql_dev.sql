-- Creates a database and Users
-- Grants permission to the user and database

CREATE DATABASE IF NOT EXISTS fr_attendance_auth_db;
CREATE USER IF NOT EXISTS fr_attendance@localhost IDENTIFIED BY 'fr_attendance_pwd';
GRANT ALL PRIVILEGES ON fr_attendance_auth_db .* TO fr_attendance@localhost;
GRANT SELECT ON performance_schema .* TO fr_attendance@localhost;
