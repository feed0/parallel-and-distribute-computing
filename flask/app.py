from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

BANCO = "produtos.db"


def criar_banco():
    """Cria o banco SQLite apenas se não existir."""
    if not os.path.exists(BANCO):
        conexao = sqlite3.connect(BANCO)
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL
            )
        """)

        produtos = [
            ("Teclado", 120.50),
            ("Mouse", 60.00),
            ("Monitor", 899.90)
        ]

        cursor.executemany("INSERT INTO produtos (nome, preco) VALUES (?, ?)", produtos)

        conexao.commit()
        conexao.close()
        print("Banco criado com 3 produtos iniciais.")
    else:
        print("Banco já existe. Usando os dados existentes.")


# ---------------- ROTAS ----------------

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    linhas = cursor.fetchall()
    conexao.close()

    produtos = [{"id": l[0], "nome": l[1], "preco": l[2]} for l in linhas]
    return jsonify(produtos)


@app.route("/produtos/<int:id>", methods=["GET"])
def buscar_produto(id):
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id=?", (id,))
    linha = cursor.fetchone()
    conexao.close()

    if linha:
        return jsonify({"id": linha[0], "nome": linha[1], "preco": linha[2]})
    return jsonify({"erro": "Produto não encontrado"}), 404


@app.route("/produtos", methods=["POST"])
def adicionar_produto():
    dados = request.json
    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (dados["nome"], dados["preco"]))
    conexao.commit()
    conexao.close()

    return jsonify({"mensagem": "Produto adicionado com sucesso"}), 201


@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = request.json
    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("UPDATE produtos SET nome=?, preco=? WHERE id=?", (dados["nome"], dados["preco"], id))
    if cursor.rowcount == 0:
        conexao.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    conexao.commit()
    conexao.close()
    return jsonify({"mensagem": "Produto atualizado com sucesso"})


@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
    if cursor.rowcount == 0:
        conexao.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    conexao.commit()
    conexao.close()
    return jsonify({"mensagem": "Produto deletado com sucesso"})


# ---------------- MAIN ----------------

if __name__ == "__main__":
    criar_banco()
    app.run(host="0.0.0.0", port=5000)
