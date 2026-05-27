from flask import Flask, g, render_template, request, redirect, url_for, flash
import sqlite3
import os
import random

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'events.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    # create DB from schema.sql if events table doesn't exist
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    if not cur.fetchone():
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql = f.read()
        db.executescript(sql)
        db.commit()
    else:
        # if events table exists, ensure we have at least 4 events by inserting two extras
        cur.execute('SELECT COUNT(*) FROM events')
        cnt = cur.fetchone()[0]
        if cnt < 4:
            # add two extra events if missing
            cur.execute("INSERT INTO events (title, description, start_datetime, end_datetime, venue_id, owner_id, capacity) VALUES (?,?,?,?,?,?,?)",
                        ('Music Concert', 'Live music night', '2026-08-01 19:00', '2026-08-01 22:00', 1, 1, 250))
            cur.execute("INSERT INTO events (title, description, start_datetime, end_datetime, venue_id, owner_id, capacity) VALUES (?,?,?,?,?,?,?)",
                        ('Coding Workshop', 'Hands-on Python workshop', '2026-09-12 09:00', '2026-09-12 13:00', 2, 2, 80))
            db.commit()
    db.close()

@app.route('/')
def index():
    db = get_db()
    rows = db.execute('''
        SELECT e.event_id, e.title, e.start_datetime, e.end_datetime, v.name AS venue, e.capacity,
               IFNULL(SUM(b.seats),0) AS booked_seats
        FROM events e
        LEFT JOIN bookings b ON e.event_id = b.event_id
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        GROUP BY e.event_id
        ORDER BY e.start_datetime
    ''').fetchall()
    events = []
    for r in rows:
        seats_available = (r['capacity'] or 0) - (r['booked_seats'] or 0)
        events.append({
            'event_id': r['event_id'], 'title': r['title'], 'start': r['start_datetime'],
            'end': r['end_datetime'], 'venue': r['venue'], 'capacity': r['capacity'],
            'booked': r['booked_seats'], 'available': seats_available
        })
    return render_template('index.html', events=events)

@app.route('/book/<int:event_id>', methods=['GET','POST'])
def book(event_id):
    db = get_db()
    event = db.execute('SELECT * FROM events WHERE event_id = ?', (event_id,)).fetchone()
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name') or 'Guest'
        email = request.form.get('email')
        seats = int(request.form.get('seats') or 1)
        if not email:
            flash('Email is required to book', 'error')
            return redirect(request.url)

        # ensure user exists
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if not user:
            cur = db.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            db.commit()
            user_id = cur.lastrowid
        else:
            user_id = user['user_id']

        # create booking and ticket inside transaction
        try:
            cur = db.cursor()
            cur.execute('BEGIN')
            cur.execute('INSERT INTO bookings (event_id, user_id, seats) VALUES (?, ?, ?)', (event_id, user_id, seats))
            booking_id = cur.lastrowid
            # generate simple ticket code
            ticket_code = f"TCKT-{random.randint(1000,9999)}"
            cur.execute('INSERT INTO tickets (booking_id, ticket_code, price) VALUES (?, ?, ?)', (booking_id, ticket_code, 0.0))
            db.commit()
            flash(f'Booking successful — ticket {ticket_code}', 'success')
            return redirect(url_for('book', event_id=event_id))
        except Exception as e:
            db.rollback()
            flash('Failed to create booking: ' + str(e), 'error')
            return redirect(request.url)

    # GET
    # fetch attendees (names and seats)
    attendees = db.execute('''
        SELECT b.booking_id, u.name, b.seats, b.booked_at
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        WHERE b.event_id = ?
        ORDER BY b.booked_at
    ''', (event_id,)).fetchall()

    # compute booked seats for display
    booked_seats = db.execute('SELECT IFNULL(SUM(seats),0) FROM bookings WHERE event_id = ?', (event_id,)).fetchone()[0]
    available = (event['capacity'] or 0) - (booked_seats or 0)

    return render_template('book.html', event=event, attendees=attendees, booked=booked_seats, available=available)


@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    db = get_db()
    # find the event for redirect
    b = db.execute('SELECT event_id FROM bookings WHERE booking_id = ?', (booking_id,)).fetchone()
    if not b:
        flash('Booking not found', 'error')
        return redirect(url_for('index'))
    event_id = b['event_id']
    try:
        cur = db.cursor()
        cur.execute('BEGIN')
        cur.execute('DELETE FROM tickets WHERE booking_id = ?', (booking_id,))
        cur.execute('DELETE FROM bookings WHERE booking_id = ?', (booking_id,))
        db.commit()
        flash('Booking cancelled — seats freed', 'success')
    except Exception as e:
        db.rollback()
        flash('Failed to cancel booking: ' + str(e), 'error')
    return redirect(url_for('book', event_id=event_id))

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)
