Event Management System (Small DBMS Project)

Overview
- Small SQLite-based database project for managing events, venues, users, bookings, and tickets.

Files
- [README.md](README.md#L1)
- [schema.sql](schema.sql#L1) — DDL + sample data
- [queries.sql](queries.sql#L1) — Useful sample queries and transactions
- [er_diagram.md](er_diagram.md#L1) — Textual ER diagram

Getting started (SQLite)
1. Create/open database:

```bash
sqlite3 events.db
```

2. Load the schema (creates tables and inserts sample data):

```sql
.read schema.sql
```

3. Run sample queries:

```sql
.read queries.sql
```

Run the demo Flask app (optional):

1. Create a virtual environment and install requirements:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Start the app:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. The app will auto-create `events.db` from `schema.sql` on first run.

Notes
- Designed for SQLite for simplicity; can be ported to MySQL/Postgres with minor changes.
- Optional: build a small web UI or CLI to demo CRUD operations.
