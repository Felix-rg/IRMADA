import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("database.db")
cur = conn.cursor()

nama_list = [
"Ahmad","Budi","Cahyo","Dedi","Eko","Fajar","Gilang","Hadi","Indra","Joko",
"Karim","Lukman","Maulana","Naufal","Omar","Rizki","Slamet","Taufik","Umar","Yusuf"
]

alamat_list = [
"Ajibarang Wetan",
"Ajibarang Kulon",
"Tipar Kidul",
"Tipar Lor"
]

kategori_list = ["perorangan","instansi"]
jenis_list = ["Zakat Maal","Infaq","Shodaqoh"]

# ===== FITRAH =====

for i in range(150):

    tanggal = (datetime.now() - timedelta(days=random.randint(0,10))).strftime("%Y-%m-%d")
    jam = f"{random.randint(17,21)}:{random.randint(10,59)}"
    nama = random.choice(nama_list) + " " + random.choice(nama_list)
    alamat = random.choice(alamat_list)
    rt = f"{random.randint(1,5):02}"
    rw = f"{random.randint(1,3):02}"
    kategori = random.choice(kategori_list)
    jiwa = random.randint(1,6)
    bungkus = jiwa

    cur.execute("""
    INSERT INTO fitrah
    (tanggal,jam,kategori,nama,alamat,rt,rw,jiwa,bungkus)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,(tanggal,jam,kategori,nama,alamat,rt,rw,jiwa,bungkus))


# ===== MAAL =====

for i in range(80):

    tanggal = (datetime.now() - timedelta(days=random.randint(0,10))).strftime("%Y-%m-%d")
    jam = f"{random.randint(17,21)}:{random.randint(10,59)}"
    nama = random.choice(nama_list) + " " + random.choice(nama_list)
    alamat = random.choice(alamat_list)
    rt = f"{random.randint(1,5):02}"
    rw = f"{random.randint(1,3):02}"
    kategori = random.choice(kategori_list)
    jenis = random.choice(jenis_list)
    nominal = random.choice([10000,20000,50000,100000,200000])

    cur.execute("""
    INSERT INTO maal
    (tanggal,jam,kategori,nama,alamat,rt,rw,jenis,nominal)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,(tanggal,jam,kategori,nama,alamat,rt,rw,jenis,nominal))


conn.commit()
conn.close()

print("Dummy data berhasil dimasukkan.")