from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from openpyxl import load_workbook
from fastapi.responses import RedirectResponse
from fastapi.responses import RedirectResponse
from fastapi import Request, Form
from starlette.middleware.sessions import SessionMiddleware


from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from fastapi.responses import FileResponse
from openpyxl.utils import get_column_letter

import sqlite3

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="irmada-secret")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def db():
    return sqlite3.connect("database.db")


@app.get("/")
def home(request: Request):

    if not request.session.get("user"):
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/fitrah")
def form_fitrah(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/login", status_code=303)
    
    return templates.TemplateResponse("fitrah.html", {"request": request})


@app.post("/fitrah")
def simpan_fitrah(
    tanggal:str=Form(...),
    nama:str=Form(...),
    alamat:str=Form(...),
    jiwa:int=Form(...),
    bungkus:int=Form(...)
):

    conn = db()
    cur = conn.cursor()

    cur.execute(
    "INSERT INTO fitrah (tanggal,nama,alamat,jiwa,bungkus) VALUES (?,?,?,?,?)",
    (tanggal,nama,alamat,jiwa,bungkus)
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/fitrah?success=1", status_code=303)


@app.get("/maal")
def form_maal(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/login", status_code=303)
    
    return templates.TemplateResponse("maal.html", {"request": request})

@app.post("/maal")
def simpan_maal(
    tanggal:str=Form(...),
    nama:str=Form(...),
    jenis:str=Form(...),
    nominal:int=Form(...)
):

    conn = db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO maal (tanggal,nama,jenis,nominal) VALUES (?,?,?,?)",
        (tanggal,nama,jenis,nominal)
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/maal?success=1", status_code=303)

@app.get("/laporan")
def laporan(request: Request):

    if not request.session.get("user"):
        return RedirectResponse("/login", status_code=303)
    
    conn = db()
    cur = conn.cursor()

    # ambil data tabel
    cur.execute("SELECT * FROM fitrah ORDER BY id DESC")
    data_fitrah = cur.fetchall()

    cur.execute("SELECT * FROM maal ORDER BY id DESC")
    data_maal = cur.fetchall()

    # hitung total
    cur.execute("SELECT SUM(jiwa) FROM fitrah")
    total_jiwa = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(nominal) FROM maal")
    total_maal = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(bungkus) FROM fitrah")
    total_bungkus = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(nominal) FROM maal WHERE jenis='Zakat Maal'")
    total_zakatmaal = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(nominal) FROM maal WHERE jenis='Infaq'")
    total_infaq = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(nominal) FROM maal WHERE jenis='Shodaqoh'")
    total_shodaqoh = cur.fetchone()[0] or 0

    total_semua = total_zakatmaal + total_infaq + total_shodaqoh
    # baru tutup database
    conn.close()

    return templates.TemplateResponse(
        "laporan.html",
        {
            "request": request,
            "fitrah": data_fitrah,
            "maal": data_maal,
            "total_jiwa": total_jiwa,
            "total_bungkus": total_bungkus,

            "total_zakatmaal": total_zakatmaal,
            "total_infaq": total_infaq,
            "total_shodaqoh": total_shodaqoh,
            "total_semua": total_semua
        }
    )

@app.get("/hapus_fitrah/{id}")
def hapus_fitrah(id:int):

    conn = db()
    cur = conn.cursor()

    cur.execute("DELETE FROM fitrah WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return RedirectResponse("/laporan", status_code=303)


@app.get("/hapus_maal/{id}")
def hapus_maal(id:int):

    conn = db()
    cur = conn.cursor()

    cur.execute("DELETE FROM maal WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return RedirectResponse("/laporan", status_code=303)

@app.post("/edit_fitrah/{id}")
def update_fitrah(
    id:int,
    tanggal:str = Form(...),
    nama:str = Form(...),
    alamat:str = Form(...),
    jiwa:int = Form(...),
    bungkus:int = Form(...)
):

    conn = db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE fitrah SET tanggal=?, nama=?, alamat=?, jiwa=?, bungkus=? WHERE id=?",
        (tanggal, nama, alamat, jiwa, bungkus, id)
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/laporan", status_code=303)

@app.post("/edit_maal/{id}")
def update_maal(
    id:int,
    tanggal:str = Form(...),
    nama:str = Form(...),
    jenis:str = Form(...),
    nominal:int = Form(...)
):

    conn = db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE maal SET tanggal=?, nama=?, jenis=?, nominal=? WHERE id=?",
        (tanggal, nama, jenis, nominal, id)
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/laporan", status_code=303)

@app.get("/export")
def export_excel():

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT tanggal,nama,alamat,jiwa,bungkus FROM fitrah ORDER BY id ASC")
    fitrah = cur.fetchall()

    cur.execute("SELECT tanggal,nama,jenis,nominal FROM maal ORDER BY id ASC")
    maal = cur.fetchall()

    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Laporan Zakat"

    # style
    header_font = Font(bold=True)
    title_font = Font(bold=True,size=16)
    center = Alignment(horizontal="center")
    fill = PatternFill(start_color="D9EAD3",fill_type="solid")

    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    # judul
    ws.merge_cells("A1:F1")
    ws["A1"] = "LAPORAN PENERIMAAN ZAKAT"
    ws["A1"].font = title_font
    ws["A1"].alignment = center

    ws.merge_cells("A2:F2")
    ws["A2"] = "Panitia Zakat"
    ws["A2"].alignment = center
    ws.merge_cells("A3:F3")
    ws["A3"] = "Tanggal Cetak : " + datetime.now().strftime("%d %B %Y")
    ws["A3"].alignment = center

    # header fitrah
    row = 4
    headers = ["No","Tanggal","Nama","Alamat","Jiwa","Bungkus"]

    for col, h in enumerate(headers,1):
        cell = ws.cell(row=row,column=col,value=h)
        cell.font = header_font
        cell.fill = fill
        cell.border = border
        cell.alignment = center

    row += 1

    total_jiwa = 0
    total_bungkus = 0

    for i,x in enumerate(fitrah,start=1):

        ws.cell(row=row,column=1,value=i).border = border
        ws.cell(row=row,column=2,value=x[0]).border = border
        ws.cell(row=row,column=3,value=x[1]).border = border
        ws.cell(row=row,column=4,value=x[2]).border = border
        ws.cell(row=row,column=5,value=x[3]).border = border
        ws.cell(row=row,column=6,value=x[4]).border = border

        total_jiwa += x[3]
        total_bungkus += x[4]

        row += 1

    # total
    row += 1

    ws.cell(row=row,column=4,value="TOTAL JIWA").font = header_font
    ws.cell(row=row,column=5,value=total_jiwa)

    row += 1

    ws.cell(row=row,column=4,value="TOTAL BUNGKUS").font = header_font
    ws.cell(row=row,column=5,value=total_bungkus)

    # tabel maal
    row += 3

    ws.cell(row=row,column=1,value="ZAKAT MAAL / INFAQ / SHODAQOH").font = header_font

    row += 1

    headers = ["No","Tanggal","Nama","Jenis","Nominal"]

    for col,h in enumerate(headers,1):
        cell = ws.cell(row=row,column=col,value=h)
        cell.font = header_font
        cell.fill = fill
        cell.border = border
        cell.alignment = center

    row += 1

    total_uang = 0

    for i,x in enumerate(maal,start=1):

        ws.cell(row=row,column=1,value=i).border = border
        ws.cell(row=row,column=2,value=x[0]).border = border
        ws.cell(row=row,column=3,value=x[1]).border = border
        ws.cell(row=row,column=4,value=x[2]).border = border

        uang = ws.cell(row=row,column=5,value=x[3])
        uang.number_format = '"Rp "#,##0'
        uang.border = border

        total_uang += x[3]

        row += 1

    row += 1

    ws.cell(row=row,column=4,value="TOTAL").font = header_font

    total_cell = ws.cell(row=row,column=5,value=total_uang)
    total_cell.number_format = '"Rp "#,##0'

    # auto width kolom (aman untuk merged cell)
    for i, col in enumerate(ws.columns, 1):

        max_length = 0

        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        column_letter = get_column_letter(i)
        ws.column_dimensions[column_letter].width = max_length + 3

        row += 4

    ws.cell(row=row,column=2,value="Mengetahui")
    ws.cell(row=row,column=5,value="Bendahara")

    row += 3

    ws.cell(row=row,column=2,value="( Ketua Panitia )")
    ws.cell(row=row,column=5,value="( Bendahara )")

    filename = "laporan_zakat.xlsx"
    wb.save(filename)

    return FileResponse(filename, filename=filename)

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if username == "irmada" and password == "zakat2026":
        request.session["user"] = username
        return RedirectResponse("/", status_code=303)

    return RedirectResponse("/login?error=1", status_code=303)

@app.get("/login")
def login_page(request: Request):

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT SUM(jiwa) FROM fitrah")
    total_jiwa = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(bungkus) FROM fitrah")
    total_bungkus = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(nominal) FROM maal WHERE jenis='Zakat Maal'")
    total_maal = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(nominal) FROM maal WHERE jenis='Infaq'")
    total_infaq = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(nominal) FROM maal WHERE jenis='Shodaqoh'")
    total_shodaqoh = cur.fetchone()[0] or 0

    conn.close()

    error = request.query_params.get("error")

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": error,
            "total_jiwa": total_jiwa,
            "total_bungkus": total_bungkus,
            "total_maal": total_maal,
            "total_infaq": total_infaq,
            "total_shodaqoh": total_shodaqoh
        }
    )

@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/login", status_code=303)

@app.get("/export_fitrah")
def export_fitrah():

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT tanggal,nama,alamat,jiwa,bungkus FROM fitrah ORDER BY id ASC")
    data = cur.fetchall()

    conn.close()

    wb = load_workbook("ZAKAT FITRAH 2026.xlsx")
    ws = wb.active

    row = 7

    for i,x in enumerate(data,start=1):

        ws.cell(row=row,column=1).value = i
        ws.cell(row=row,column=2).value = x[0]
        ws.cell(row=row,column=3).value = datetime.now().strftime("%H:%M")
        ws.cell(row=row,column=4).value = x[1]
        ws.cell(row=row,column=5).value = x[2]
        ws.cell(row=row,column=6).value = "Zakat Fitrah"
        ws.cell(row=row,column=7).value = x[3]
        ws.cell(row=row,column=8).value = x[4]

        row += 1

    file = "laporan_fitrah.xlsx"
    wb.save(file)

    return FileResponse(
    file,
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    filename="laporan_fitrah.xlsx"
)

@app.get("/export_maal")
def export_maal():

    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT tanggal,nama,jenis,nominal FROM maal ORDER BY id ASC")
    data = cur.fetchall()

    conn.close()

    wb = load_workbook("ZAKAT MAAL_INFAQ_SHODAQOH 2026.xlsx")
    ws = wb.active

    row = 7

    for i,x in enumerate(data,start=1):

        ws.cell(row=row,column=1).value = i
        ws.cell(row=row,column=2).value = x[0]
        ws.cell(row=row,column=3).value = datetime.now().strftime("%H:%M")
        ws.cell(row=row,column=4).value = x[1]
        ws.cell(row=row,column=5).value = ""
        ws.cell(row=row,column=6).value = "Zakat"
        ws.cell(row=row,column=7).value = x[2]
        ws.cell(row=row,column=8).value = x[3]

        row += 1

    file = "laporan_maal.xlsx"
    wb.save(file)

    return FileResponse(
    file,
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    filename="laporan_maal.xlsx"
)

