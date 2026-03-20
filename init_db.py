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
nik TEXT,
alamat TEXT,
rt TEXT,
rw TEXT,
kecamatan TEXT,
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
nik TEXT,
alamat TEXT,
rt TEXT,
rw TEXT,
kecamatan TEXT,
jenis TEXT,
nominal INTEGER
)
""")


cur.execute("""
CREATE TABLE penyaluran (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tanggal TEXT,
nama TEXT,
nik TEXT,
alamat TEXT,
rt TEXT,
rw TEXT,
kecamatan TEXT,
jumlah_bungkus INTEGER,
tanda_tangan TEXT
)
""")

conn.commit()
conn.close()

print("DATABASE BERHASIL DIBUAT")