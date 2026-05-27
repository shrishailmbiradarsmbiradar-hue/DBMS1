import sqlite3

conn = sqlite3.connect('events.db')
cur = conn.cursor()
cur.execute("UPDATE events SET title='sapthagiri Aurafesta 3.0' WHERE title='sapthagiri Aurafesta 2.0'")
conn.commit()
print('Updated event title to Aurafesta 3.0')
for row in cur.execute("SELECT event_id, title FROM events ORDER BY event_id"):
    print(f"{row[0]}: {row[1]}")
conn.close()
