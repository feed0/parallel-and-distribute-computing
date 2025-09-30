import asyncio
import aiohttp

BASE_URL = "http://127.0.0.1:5000"


# --- Funções assíncronas para cada rota ---
async def listar_produtos(session):
    r = await session.get(BASE_URL + "/produtos")
    dados = await r.json()
    print("[GET /produtos] " + str(r.status) + " -> " + str(dados))
    r.release()


async def buscar_produto(session, id_produto):
    r = await session.get(BASE_URL + "/produtos/" + str(id_produto))
    dados = await r.json()
    print("[GET /produtos/" + str(id_produto) + "] " + str(r.status) + " -> " + str(dados))
    r.release()


async def adicionar_produto(session, nome, preco):
    r = await session.post(BASE_URL + "/produtos", json={"nome": nome, "preco": preco})
    dados = await r.json()
    print("[POST /produtos] " + str(r.status) + " -> " + str(dados))
    r.release()


async def atualizar_produto(session, id_produto, nome, preco):
    r = await session.put(BASE_URL + "/produtos/" + str(id_produto), json={"nome": nome, "preco": preco})
    dados = await r.json()
    print("[PUT /produtos/" + str(id_produto) + "] " + str(r.status) + " -> " + str(dados))
    r.release()


async def deletar_produto(session, id_produto):
    r = await session.delete(BASE_URL + "/produtos/" + str(id_produto))
    dados = await r.json()
    print("[DELETE /produtos/" + str(id_produto) + "] " + str(r.status) + " -> " + str(dados))
    r.release()


# --- Função principal simplificada ---
async def executar_cliente():
    session = aiohttp.ClientSession()

    # --- 5 x GET /produtos ---
    print("\n=== 5 x GET /produtos ===")
    tarefas = []
    for _ in range(5):
        tarefas.append(listar_produtos(session))
    await asyncio.gather(*tarefas)

    # --- 5 x GET /produtos/1 ---
    print("\n=== 5 x GET /produtos/1 ===")
    tarefas = []
    for _ in range(5):
        tarefas.append(buscar_produto(session, 1))
    await asyncio.gather(*tarefas)

    # --- 5 x POST /produtos ---
    print("\n=== 5 x POST /produtos ===")
    tarefas = []
    for i in range(5):
        tarefas.append(adicionar_produto(session, "Produto_" + str(i), 10.0 + i))
    await asyncio.gather(*tarefas)

    # --- 5 x PUT /produtos/2 ---
    print("\n=== 5 x PUT /produtos/2 ===")
    tarefas = []
    for i in range(5):
        tarefas.append(atualizar_produto(session, 2, "Mouse_Atualizado_" + str(i), 80.0 + i))
    await asyncio.gather(*tarefas)

    # --- 5 x DELETE /produtos/3 ---
    print("\n=== 5 x DELETE /produtos/3 ===")
    tarefas = []
    for _ in range(5):
        tarefas.append(deletar_produto(session, 3))
    await asyncio.gather(*tarefas)

    await session.close()


# --- Bloco de execução ---
if __name__ == "__main__":
    asyncio.run(executar_cliente())
