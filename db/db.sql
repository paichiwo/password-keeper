BEGIN TRANSACTION;

DROP TABLE IF EXISTS user_profile;

CREATE TABLE user_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

DROP TABLE IF EXISTS user_data;

CREATE TABLE user_data (
  user_id INTEGER NOT NULL,
  website TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user_profile(id)
);

COMMIT;