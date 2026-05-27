import sqlite3

conn = sqlite3.connect('events.db')
cur = conn.cursor()
# Update event title to Kannada script
cur.execute("UPDATE events SET title='ಕನ್ನಡ ರಾಜ್ಯೋತ್ಸವ' WHERE title='Kannada Rajyotsava'")
conn.commit()
print('Updated event to Kannada script: ಕನ್ನಡ ರಾಜ್ಯೋತ್ಸವ')
print('\nCurrent events (ordered by date):')
for row in cur.execute("SELECT event_id, title, start_datetime FROM events ORDER BY start_datetime"):
    print(f"{row[0]}: {row[1]} — {row[2]}")
conn.close()
