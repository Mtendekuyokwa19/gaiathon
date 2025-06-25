
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS report;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE sensor_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  time TEXT,
  date TEXT,
  location TEXT,
  ultrasonic_value REAL,
  gas_sensor_value REAL
);
CREATE TABLE report (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location_name TEXT NOT NULL,
  coordinates TEXT NOT NULL,
  reporter_name TEXT NOT NULL
);
CREATE TABLE location (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location_name TEXT NOT NULL,
  coordinates TEXT NOT NULL,
  owner TEXT NOT NULL,
  isfull TEXT NOT NULL DEFAULT 'yes'
);
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

INSERT INTO report(location_name, coordinates, reporter_name ) VALUES
("Limbe", "-15.8011,35.0657", "admin"),
("Chichiri", "-15.7984,35.0293", "admin"),
("Soche", "-15.8255,35.0341", "admin"),
("Chilomoni", "-15.8212,35.0121", "admin"),
("Ndirande", "-15.7835,35.0446", "admin");
INSERT INTO location(location_name, coordinates, owner, isfull) VALUES
("Limbe", "-15.8011,35.0657", "admin", "no"),
("Chichiri", "-15.7984,35.0293", "admin", "no"),
("Soche", "-15.8255,35.0341", "admin", "no"),
("Chilomoni", "-15.8212,35.0121", "admin", "yes"),
("Ndirande", "-15.7835,35.0446", "admin","yes" );
