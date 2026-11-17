import os, sqlite3, hashlib
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import aiosqlite

app = FastAPI(docs_url=None, redoc_url=None)
DB = Path("data.db")
TOKEN = os.environ.get("AGENT_TOKEN")
USER = os.environ.get("PANEL_USER")
HASH = os.environ.get("PANEL_HASH")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS devices(id TEXT PRIMARY KEY, alias TEXT, last_seen TEXT, battery INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS locations(id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, lat REAL, lon REAL, ts TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS sms(id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT, address TEXT, body TEXT, ts TEXT)""")
    conn.commit()
    conn.close()

init_db()

async def verify_token(req: Request):
    auth = req.headers.get("authorization")
    if not auth or auth != f"Bearer {TOKEN}":
        raise HTTPException(status_code=401)

@app.post("/ingest/location", dependencies=[Depends(verify_token)])
async def loc(device: str, lat: float, lon: float, bat: int = -1):
    ts = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB) as db:
        await db.execute("REPLACE INTO devices(id,alias,last_seen,battery) VALUES (?, ?, ?, ?)", (device, device, ts, bat))
        await db.execute("INSERT INTO locations(device_id,lat,lon,ts) VALUES (?, ?, ?, ?)", (device, lat, lon, ts))
        await db.commit()
    return {"ok": True}

@app.post("/ingest/sms", dependencies=[Depends(verify_token)])
async def sms(device: str, address: str, body: str):
    ts = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT INTO sms(device_id,address,body,ts) VALUES (?, ?, ?, ?)", (device, address, body, ts))
        await db.commit()
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
async def home(req: Request):
    cookie = req.cookies.get("panel_auth")
    if cookie != HASH:
        return RedirectResponse("/login")
    return open("panel.html", "r", encoding="utf-8").read()

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return '<form method="POST"><input name="u" placeholder="Usuario"><input name="p" placeholder="Contraseña" type="password"><button type="submit">Entrar</button></form>'

@app.post("/login")
async def login(u: str = Form(...), p: str = Form(...)):
    if u == USER and hashlib.sha256(p.encode()).hexdigest() == HASH:
        resp = RedirectResponse("/")
        resp.set_cookie("panel_auth", HASH)
        return resp
    return HTMLResponse('<h3>Credenciales incorrectas</h3><a href="/login">Volver</a>')

@app.get("/api/latest")
async def latest(req: Request):
    if req.cookies.get("panel_auth") != HASH:
        raise HTTPException(status_code=403)
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM devices")
        devs = await cur.fetchall()
        cur = await db.execute("SELECT * FROM locations ORDER BY id DESC LIMIT 100")
        locs = await cur.fetchall()
        cur = await db.execute("SELECT * FROM sms ORDER BY id DESC LIMIT 100")
        msgs = await cur.fetchall()
    return JSONResponse({"devices": [dict(d) for d in devs], "locations": [dict(l) for l in locs], "sms": [dict(m) for m in msgs]})
