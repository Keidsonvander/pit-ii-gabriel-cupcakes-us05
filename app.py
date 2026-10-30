from flask import Flask, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path("catalogo.db")

PRODUTOS = [
    {"id": 1, "nome": "Cupcake Chocolate Intenso", "descricao": "Massa de chocolate com cobertura cremosa.", "ingredientes": "Farinha, ovos, leite, cacau, açúcar e chocolate.", "tamanho": "Médio — 90 g", "preco": 9.50},
    {"id": 2, "nome": "Cupcake Morango", "descricao": "Massa de baunilha com creme e morango.", "ingredientes": "Farinha, ovos, leite, baunilha, açúcar, creme e morango.", "tamanho": "Médio — 95 g", "preco": 10.00},
    {"id": 3, "nome": "Cupcake Baunilha", "descricao": "Massa macia de baunilha com cobertura artesanal.", "ingredientes": "Farinha, ovos, leite, baunilha, açúcar e manteiga.", "tamanho": "Pequeno — 80 g", "preco": 8.50},
    {"id": 4, "nome": "Cupcake Red Velvet", "descricao": "Massa red velvet com cobertura de cream cheese.", "ingredientes": "Farinha, ovos, leite, cacau, açúcar e cream cheese.", "tamanho": "Grande — 110 g", "preco": 11.00},
]

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            preco REAL NOT NULL
        )""")
        for p in PRODUTOS:
            conn.execute("""INSERT OR REPLACE INTO produtos
            (id,nome,descricao,ingredientes,tamanho,preco)
            VALUES(?,?,?,?,?,?)""",
            (p["id"],p["nome"],p["descricao"],p["ingredientes"],p["tamanho"],p["preco"]))

@app.route("/api/produtos")
def listar_produtos():
    init_db()
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        dados = conn.execute("SELECT * FROM produtos ORDER BY id").fetchall()
    return jsonify([dict(x) for x in dados])

@app.route("/api/produtos/<int:produto_id>")
def detalhe_produto(produto_id):
    init_db()
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        dado = conn.execute("SELECT * FROM produtos WHERE id=?", (produto_id,)).fetchone()
    if not dado:
        return jsonify({"erro":"Produto não encontrado"}),404
    return jsonify(dict(dado))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
