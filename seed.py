# import sqlite3
# import random
# from datetime import datetime, timedelta

# conn = sqlite3.connect("database.db")
# cur = conn.cursor()

# nama_list = [
#     "Budi", "Siti", "Joko", "Dewi", "Ahmad", "Rina",
#     "Hendra", "Lina", "Agus", "Yuni", "Rizky", "Nina",
#     "Fajar", "Putri", "Andi", "Dina"
# ]

# desa_list = [
#     "Ajibarang Wetan", "Ajibarang Kulon",
#     "Kracak", "Pancasan", "Karangbawang"
# ]

# kecamatan = "Ajibarang"

# for i in range(200):
#     nama = random.choice(nama_list) + " " + random.choice(nama_list)
#     nik = str(3301010101010000 + i)

#     alamat = random.choice(desa_list)
#     rt = str(random.randint(1, 5)).zfill(2)
#     rw = str(random.randint(1, 3)).zfill(2)

#     kategori = random.choice(["perorangan", "instansi"])

#     if kategori == "perorangan":
#         jiwa = 1
#     else:
#         jiwa = random.randint(2, 10)

#     bungkus = jiwa

#     tanggal = "2026-03-20"
#     jam = (datetime(2026, 3, 20, 8, 0) + timedelta(minutes=i)).strftime("%H:%M")

#     cur.execute("""
#     INSERT INTO fitrah (tanggal, jam, kategori, nama, nik, alamat, rt, rw, kecamatan, jiwa, bungkus)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (tanggal, jam, kategori, nama, nik, alamat, rt, rw, kecamatan, jiwa, bungkus))

# conn.commit()
# conn.close()

# print("200 data dummy masuk. sekarang keliatan kayak sistem beneran, bukan latihan anak TK.")

# ===== MAAL =====

import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("database.db")
cur = conn.cursor()

nama_list = [
    "Budi", "Siti", "Joko", "Dewi", "Ahmad", "Rina",
    "Hendra", "Lina", "Agus", "Yuni", "Rizky", "Nina",
    "Fajar", "Putri", "Andi", "Dina"
]

desa_list = [
    "Ajibarang Wetan", "Ajibarang Kulon",
    "Kracak", "Pancasan", "Karangbawang"
]

jenis_list = ["Zakat Maal", "Infaq", "Shodaqoh"]

kecamatan = "Ajibarang"

for i in range(200):
    nama = random.choice(nama_list) + " " + random.choice(nama_list)
    nik = str(3301010101011000 + i)

    alamat = random.choice(desa_list)
    rt = str(random.randint(1, 5)).zfill(2)
    rw = str(random.randint(1, 3)).zfill(2)

    kategori = random.choice(["perorangan", "instansi"])
    jenis = random.choice(jenis_list)

    # nominal realistis
    nominal = random.choice([
        10000, 20000, 50000, 100000, 200000, 500000
    ])

    tanggal = "2026-03-20"
    jam = (datetime(2026, 3, 20, 8, 0) + timedelta(minutes=i)).strftime("%H:%M")

    cur.execute("""
    INSERT INTO maal
    (tanggal,jam,kategori,nama,nik,alamat,rt,rw,kecamatan,jenis,nominal)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (tanggal,jam,kategori,nama,nik,alamat,rt,rw,kecamatan,jenis,nominal))

conn.commit()
conn.close()

print("200 data maal masuk. sekarang laporan lu ga sepi kayak kuburan.")