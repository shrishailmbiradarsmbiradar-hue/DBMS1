import sqlite3

conn = sqlite3.connect('events.db')
cur = conn.cursor()
# Update Aurafesta 3.0 dates to 2027
cur.execute("UPDATE events SET start_datetime='2027-06-10 18:00', end_datetime='2027-06-10 21:00' WHERE title='sapthagiri Aurafesta 3.0'")
# Add Kannada Rajyotsava if not already present
cur.execute("SELECT COUNT(*) FROM events WHERE title='Kannada Rajyotsava'")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO events (title, description, start_datetime, end_datetime, venue_id, owner_id, capacity) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ('Kannada Rajyotsava', 'Kannada cultural celebration', '2026-11-01 10:00', '2026-11-01 18:00', 1, 1, 150))
conn.commit()
print('Updated Aurafesta to 2027 and added Kannada Rajyotsava')
print('\nCurrent events (ordered by date):')
for row in cur.execute("SELECT event_id, title, start_datetime FROM events ORDER BY start_datetime"):
    print(f"{row[0]}: {row[1]} — {row[2]}")
conn.close()
