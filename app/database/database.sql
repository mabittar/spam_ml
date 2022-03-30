GRANT ALL PRIVILEGES on spam_ml.* to 'postgres_user';
CREATE SCHEMA IF NOT EXISTS spam_ml DEFAULT CHARACTER SET utf8;


CREATE TABLE IF NOT EXISTS spam_ml.User (
  id INT(11) NOT NULL AUTO_INCREMENT,
  user_key VARCHAR(36) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  user_role enum("super admin", "admin", "user") NOT NULL,
  password VARCHAR(120),
  full_name VARCHAR(120) NOT NULL,
  phone VARCHAR(120) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY id (id),
  UNIQUE KEY UC_person_key (user_key),
  UNIQUE KEY UC_email (email),
);