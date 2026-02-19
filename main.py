from fastapi import FastAPI, Request
import sqlite3
from datetime import datetime

app = FastAPI()

# Inicializar banco
def init_db():
    conn = sqlite3.connect("ciaq.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefone TEXT,
            mensagem TEXT,
            data_registro TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return {"CIAQ": "Servidor rodando corretamente"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    telefone = data.get("telefone")
    mensagem = data.get("mensagem")
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("ciaq.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (telefone, mensagem, data_registro)
        VALUES (?, ?, ?)
    """, (telefone, mensagem, data_registro))
    conn.commit()
    conn.close()

    return {"status": "salvo no banco"}

@app.get("/mensagens/{telefone}")
def listar_mensagens(telefone: str):
    conn = sqlite3.connect("ciaq.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT telefone, mensagem, data_registro
        FROM messages
        WHERE telefone = ?
        ORDER BY id DESC
    """, (telefone,))
    
    resultados = cursor.fetchall()
    conn.close()

    mensagens = []
    for r in resultados:
        mensagens.append({
            "telefone": r[0],
            "mensagem": r[1],
            "data_registro": r[2]
        })

    return {"mensagens": mensagens}
