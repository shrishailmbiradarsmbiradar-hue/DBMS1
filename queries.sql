-- Sample queries for Event Management System

-- 1. List all upcoming events
SELECT event_id, title, start_datetime, end_datetime, name AS venue
FROM events JOIN venues USING(venue_id)
WHERE start_datetime >= datetime('now')
ORDER BY start_datetime;

-- 2. Show bookings for an event
SELECT b.booking_id, u.name AS attendee, b.seats, b.booked_at, b.status
FROM bookings b
JOIN users u USING(user_id)
WHERE b.event_id = 1;

-- 3. Count attendees per event
SELECT e.event_id, e.title, IFNULL(SUM(b.seats),0) AS total_seats
FROM events e
LEFT JOIN bookings b ON e.event_id = b.event_id
GROUP BY e.event_id;

-- 4. Available seats (event capacity - booked seats)
SELECT e.event_id, e.title, e.capacity,
       e.capacity - IFNULL(SUM(b.seats),0) AS seats_available
FROM events e
LEFT JOIN bookings b ON e.event_id = b.event_id
GROUP BY e.event_id;

-- 5. Revenue per event (tickets)
SELECT e.event_id, e.title, IFNULL(SUM(t.price),0) AS revenue
FROM events e
LEFT JOIN bookings b ON e.event_id = b.event_id
LEFT JOIN tickets t ON b.booking_id = t.booking_id
GROUP BY e.event_id;

-- 6. Transactional booking example (SQLite syntax)
-- BEGIN TRANSACTION;
-- INSERT INTO bookings (event_id, user_id, seats) VALUES (1, 1, 2);
-- INSERT INTO tickets (booking_id, ticket_code, price) VALUES (last_insert_rowid(), 'TCKT-0003', 0.0);
-- COMMIT;
