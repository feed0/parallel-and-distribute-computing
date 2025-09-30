import requests

# Endereço base da API (ajuste para conectar em outro host/porta)
BASE_URL = "http://127.0.0.1:5000"


def listar_produtos():
    """Faz um GET para /produtos e mostra todos os produtos"""
    url = BASE_URL + "/produtos"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        print("Lista de produtos:")
        for p in resposta.json():
            print("- ID " + str(p["id"]) + ": " + p["nome"] + " (R$ " + str(p["preco"]) + ")")
    else:
        print("Erro ao listar produtos:", resposta.text)


def buscar_produto(id_produto):
    """Faz um GET para /produtos/<id>"""
    url = BASE_URL + "/produtos/" + str(id_produto)
    resposta = requests.get(url)
    if resposta.status_code == 200:
        p = resposta.json()
        print("Produto encontrado: " + p["nome"] + " (R$ " + str(p["preco"]) + ")")
    else:
        print("Erro:", resposta.json())


def adicionar_produto(nome, preco):
    """Faz um POST para /produtos"""
    url = BASE_URL + "/produtos"
    dados = {"nome": nome, "preco": preco}
    resposta = requests.post(url, json=dados)
    print("Resposta:", resposta.json())


def atualizar_produto(id_produto, nome, preco):
    """Faz um PUT para /produtos/<id>"""
    url = BASE_URL + "/produtos/" + str(id_produto)
    dados = {"nome": nome, "preco": preco}
    resposta = requests.put(url, json=dados)
    print("Resposta:", resposta.json())


def deletar_produto(id_produto):
    """Faz um DELETE para /produtos/<id>"""
    url = BASE_URL + "/produtos/" + str(id_produto)
    resposta = requests.delete(url)
    print("Resposta:", resposta.json())


# ------------------- EXEMPLO DE USO -------------------

if __name__ == "__main__":
    # 1. Listar produtos iniciais
    listar_produtos()

    # 2. Buscar produto existente
    buscar_produto(1)

    # 3. Adicionar novo produto
    adicionar_produto("Headset Gamer", 250.00)

    # 4. Listar novamente para ver o novo produto
    listar_produtos()

    # 5. Atualizar um produto (por exemplo, o de ID 2)
    atualizar_produto(2, "Mouse Sem Fio", 75.00)

    # 6. Deletar um produto (por exemplo, o de ID 3)
    deletar_produto(3)

    # 7. Listar para ver as mudanças finais
    listar_produtos()
