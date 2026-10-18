CREATE DATABASE IF NOT EXISTS bugtrack CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'bugtrack_user'@'localhost' IDENTIFIED BY 'change_me';
GRANT ALL PRIVILEGES ON bugtrack.* TO 'bugtrack_user'@'localhost';
FLUSH PRIVILEGES;
-- Change the sample password, configure DATABASE_URL, then run: flask --app app init-db
