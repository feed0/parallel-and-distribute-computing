from flask import Flask, request, jsonify
import os

app = Flask(__name__)
ARQUIVO_IPS = "ips.txt"


@app.route('/descoberta', methods=['GET'])
def descoberta():
    # Determinar a origem da requisição (proxy ou não)
    ip1 = request.headers.getlist('X-Forwarded-For')[0] if request.headers.getlist('X-Forwarded-For') else ''
    ip2 = request.remote_addr or ''
    ip = ip1 if ip1 else ip2

    # Garantir que o arquivo existe
    if not os.path.exists(ARQUIVO_IPS):
        open(ARQUIVO_IPS, "w", encoding="utf-8").close()

    # Ler IPs já registrados
    with open(ARQUIVO_IPS, "r", encoding="utf-8") as f:
        ips = [linha.strip() for linha in f.readlines() if linha.strip()]

    # Registrar o IP somente se ainda não existir
    if ip and ip not in ips:
        with open(ARQUIVO_IPS, "a", encoding="utf-8") as f:
            f.write(ip + "\n")
        ips.append(ip)

    return jsonify(ips)


if __name__ == '__main__':
    print("Servidor de descoberta iniciado em http://0.0.0.0:5000/descoberta")
    app.run(host='0.0.0.0', port=5000)