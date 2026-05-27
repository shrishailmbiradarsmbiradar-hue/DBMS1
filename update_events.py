import sqlite3

conn = sqlite3.connect('events.db')
cur = conn.cursor()
cur.execute("UPDATE events SET title='sapthagiri Aurafesta 2.0' WHERE title='Tech Meetup'")
cur.execute("UPDATE events SET title='Hackthon' WHERE title='Art Exhibition'")
conn.commit()
print('Applied updates to events.db')
for row in cur.execute("SELECT event_id, title FROM events ORDER BY event_id"):
    print(f"{row[0]}: {row[1]}")
conn.close()
