import sqlite3

conn = sqlite3.connect('events.db')
cur = conn.cursor()
# Update known venue ids (1 and 2) to the requested name
cur.execute("UPDATE venues SET name='sapthagiri nps university' WHERE venue_id IN (1,2)")
# Also update any remaining old names just in case
cur.execute("UPDATE venues SET name='sapthagiri nps university' WHERE name IN ('Town Hall','Conference Center')")
conn.commit()
print('Applied venue name updates to events.db')
for row in cur.execute("SELECT venue_id, name, capacity FROM venues ORDER BY venue_id"):
    print(f"{row[0]}: {row[1]} (capacity {row[2]})")
conn.close()
