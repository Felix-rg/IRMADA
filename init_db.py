import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# =========================
# TABEL ZAKAT FITRAH
# =========================

cur.execute("""
CREATE TABLE fitrah (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tanggal TEXT,
jam TEXT,
kategori TEXT,
nama TEXT,
alamat TEXT,
rt TEXT,
rw TEXT,
jiwa INTEGER,
bungkus INTEGER
)
""")

# =========================
# TABEL ZAKAT MAAL
# =========================

cur.execute("""
CREATE TABLE maal (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tanggal TEXT,
jam TEXT,
kategori TEXT,
nama TEXT,
alamat TEXT,
rt TEXT,
rw TEXT,
jenis TEXT,
nominal INTEGER
)
""")

conn.commit()
conn.close()

print("DATABASE BERHASIL DIBUAT")