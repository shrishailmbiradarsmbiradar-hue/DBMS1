-- SQLite schema for small Event Management System
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE venues (
  venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  address TEXT,
  capacity INTEGER
);

CREATE TABLE events (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  start_datetime TEXT,
  end_datetime TEXT,
  venue_id INTEGER,
  owner_id INTEGER,
  status TEXT DEFAULT 'scheduled',
  capacity INTEGER,
  FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
  FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

CREATE TABLE bookings (
  booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  seats INTEGER DEFAULT 1,
  booked_at TEXT DEFAULT CURRENT_TIMESTAMP,
  status TEXT DEFAULT 'confirmed',
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE tickets (
  ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
  booking_id INTEGER NOT NULL,
  ticket_code TEXT UNIQUE,
  price REAL DEFAULT 0.0,
  issued_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);

CREATE TABLE tags (
  tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE event_tags (
  event_id INTEGER,
  tag_id INTEGER,
  PRIMARY KEY (event_id, tag_id),
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- Sample data
INSERT INTO users (name, email, phone) VALUES
('Alice Kumar','alice@example.com','+91-9000000001'),
('Bob Sharma','bob@example.com','+91-9000000002');

INSERT INTO venues (name, address, capacity) VALUES
('sapthagiri nps university','123 Main St',300),
('sapthagiri nps university','45 Business Ave',150);

INSERT INTO events (title, description, start_datetime, end_datetime, venue_id, owner_id, capacity) VALUES
('sapthagiri Aurafesta 3.0','Monthly tech meetup','2027-06-10 18:00','2027-06-10 21:00',1,1,200),
('ಕನ್ನಡ ರಾಜ್ಯೋತ್ಸವ','Kannada cultural celebration','2026-11-01 10:00','2026-11-01 18:00',1,1,150),
('Hackthon','Local artists showcase','2026-07-05 10:00','2026-07-05 17:00',2,2,120);

INSERT INTO bookings (event_id, user_id, seats) VALUES
(1,2,2),
(2,1,1);

INSERT INTO tickets (booking_id, ticket_code, price) VALUES
(1,'TCKT-0001',0.0),
(2,'TCKT-0002',50.0);

INSERT INTO tags (name) VALUES ('technology'),('art');
INSERT INTO event_tags (event_id, tag_id) VALUES (1,1),(2,2);
