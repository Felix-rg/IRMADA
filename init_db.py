import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS fitrah (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tanggal TEXT,
nama TEXT,
alamat TEXT,
jiwa INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS maal (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tanggal TEXT,
nama TEXT,
jenis TEXT,
nominal INTEGER
)
""")

conn.commit()
conn.close()

print("database siap")