import sqlite3
conn = sqlite3.connect('database/data/water_footprint.db')
cursor = conn.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Database tables:", tables)
for t in tables:
    name = t[0]
    count = cursor.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    cols = [c[1] for c in cursor.execute(f"PRAGMA table_info({name})").fetchall()]
    print(f"Table '{name}': {count} rows. Columns: {cols}")
conn.close()
