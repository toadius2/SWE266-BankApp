DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS account;

-- Currentlly, we only have regular user (i.e., no role field in this table for user like manager or admin)
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phone_number INTEGER NOT NULL
);

CREATE TABLE account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  balance DECIMAl(16, 2) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);