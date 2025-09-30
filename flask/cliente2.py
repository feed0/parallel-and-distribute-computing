import requests
import threading

BASE_URL = "http://127.0.0.1:5000"

# --- Funções simples para cada rota ---

def listar_produtos():
    r = requests.get(BASE_URL + "/produtos")
    print("[GET /produtos] " + str(r.status_code) + " -> " + str(r.json()))

def buscar_produto(id_produto):
    r = requests.get(BASE_URL + "/produtos/" + str(id_produto))
    print("[GET /produtos/" + str(id_produto) + "] " + str(r.status_code) + " -> " + str(r.json()))

def adicionar_produto(nome, preco):
    r = requests.post(BASE_URL + "/produtos", json={"nome": nome, "preco": preco})
    print("[POST /produtos] " + str(r.status_code) + " -> " + str(r.json()))

def atualizar_produto(id_produto, nome, preco):
    r = requests.put(BASE_URL + "/produtos/" + str(id_produto), json={"nome": nome, "preco": preco})
    print("[PUT /produtos/" + str(id_produto) + "] " + str(r.status_code) + " -> " + str(r.json()))

def deletar_produto(id_produto):
    r = requests.delete(BASE_URL + "/produtos/" + str(id_produto))
    print("[DELETE /produtos/" + str(id_produto) + "] " + str(r.status_code) + " -> " + str(r.json()))


# --- Main com threads simples ---
if __name__ == "__main__":

    print("\n=== 5 x GET /produtos ===")
    threads = []
    for _ in range(5):
        t = threading.Thread(target=listar_produtos)
        t.start()
        threads.append(t)
    for t in threads: t.join()

    print("\n=== 5 x GET /produtos/1 ===")
    threads = []
    for _ in range(5):
        t = threading.Thread(target=buscar_produto, args=(1,))
        t.start()
        threads.append(t)
    for t in threads: t.join()

    print("\n=== 5 x POST /produtos ===")
    threads = []
    for i in range(5):
        t = threading.Thread(target=adicionar_produto, args=("Produto_" + str(i), 10.0 + i))
        t.start()
        threads.append(t)
    for t in threads: t.join()

    print("\n=== 5 x PUT /produtos/2 ===")
    threads = []
    for i in range(5):
        t = threading.Thread(target=atualizar_produto, args=(2, "Mouse_Atualizado_" + str(i), 80.0 + i))
        t.start()
        threads.append(t)
    for t in threads: t.join()

    print("\n=== 5 x DELETE /produtos/3 ===")
    threads = []
    for _ in range(5):
        t = threading.Thread(target=deletar_produto, args=(3,))
        t.start()
        threads.append(t)
    for t in threads: t.join()
