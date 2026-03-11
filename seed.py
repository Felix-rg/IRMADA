import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("database.db")
cur = conn.cursor()

nama_list = [
    "Ahmad","Budi","Siti","Rina","Dedi","Hadi","Asep",
    "Ujang","Tono","Joko","Fajar","Rizki","Agus","Yusuf"
]

alamat_list = [
    "RT 01","RT 02","RT 03","RT 04","RT 05"
]

jenis_list = ["Zakat Maal","Infaq","Shodaqoh"]

# =====================
# DATA FITRAH
# =====================

for i in range(150):

    tanggal = (datetime.now() - timedelta(days=random.randint(0,3))).strftime("%Y-%m-%d")
    nama = random.choice(nama_list)
    alamat = random.choice(alamat_list)
    jiwa = random.randint(1,6)
    bungkus = jiwa

    cur.execute(
        "INSERT INTO fitrah (tanggal,nama,alamat,jiwa,bungkus) VALUES (?,?,?,?,?)",
        (tanggal,nama,alamat,jiwa,bungkus)
    )

# =====================
# DATA MAAL
# =====================

for i in range(80):

    tanggal = (datetime.now() - timedelta(days=random.randint(0,3))).strftime("%Y-%m-%d")
    nama = random.choice(nama_list)
    jenis = random.choice(jenis_list)
    nominal = random.randint(10000,200000)

    cur.execute(
        "INSERT INTO maal (tanggal,nama,jenis,nominal) VALUES (?,?,?,?)",
        (tanggal,nama,jenis,nominal)
    )

conn.commit()
conn.close()

print("Data dummy berhasil dimasukkan")