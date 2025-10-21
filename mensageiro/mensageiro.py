from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)
ARQUIVO_MSG = "mensagens.txt"
PORTA_LOCAL = 5000
SERVIDOR_DESTINO = "http://44.203.247.157:5000/descoberta"

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Mensageiro Flask</title>
    <style>
        body { font-family: Arial; margin: 24px; background-color: #f7f7f7; }
        h2 { color: #333; margin: 0 0 8px 0; }
        textarea, input { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
        textarea { height: 120px; resize: none; }
        button { padding: 8px 14px; margin-top: 10px; cursor: pointer; }
        .box { background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 0 6px #ccc; margin-bottom: 18px; }
        .row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
        #status { margin-top: 8px; font-weight: bold; }
        pre { background:#fafafa; padding:10px; border-radius:6px; max-height:200px; overflow:auto; }
        #ip-local { color: #007700; font-weight: bold; }
    </style>
</head>
<body onload="mostrarMeuIP()">
    <div class="box">
        <h2>Mensageiro Flask</h2>
        <p>Seu endereço público: <span id="ip-local">(detectando...)</span></p>
    </div>

    <div class="box">
        <h2>Enviar Mensagem</h2>
        <label>Destino (ex: 127.0.0.1:5000)</label>
        <input type="text" id="destino" placeholder="endereco:porta"><br>
        <label>Mensagem</label>
        <textarea id="mensagem" placeholder="Digite sua mensagem aqui"></textarea>
        <div class="row">
            <button onclick="enviarMensagem()">Enviar</button>
            <button onclick="atualizarMensagens()">Atualizar Mensagens</button>
            <button onclick="buscarIPs()">Buscar IPs</button>
        </div>
        <div id="status"></div>
    </div>

    <div class="box">
        <h2>Mensagens Recebidas</h2>
        <textarea id="mensagens" readonly placeholder="Nenhuma mensagem ainda."></textarea>
    </div>

    <div class="box">
        <h2>IPs Descobertos (servidor)</h2>
        <pre id="ips">Nenhuma busca realizada.</pre>
    </div>

<script>
function mostrarMeuIP() {
    const host = window.location.hostname;
    const port = window.location.port ? ":" + window.location.port : "";
    document.getElementById("ip-local").innerText = host + port;
}

async function enviarMensagem() {
    const destino = document.getElementById('destino').value.trim();
    const mensagem = document.getElementById('mensagem').value.trim();
    const status = document.getElementById('status');

    status.style.color = 'black';
    status.innerText = 'Enviando...';

    if (!destino || !mensagem) {
        status.style.color = 'red';
        status.innerText = "Preencha destino e mensagem.";
        return;
    }

    try {
        const resp = await fetch('/enviar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({destino, mensagem})
        });
        const data = await resp.json();
        status.style.color = resp.ok ? 'green' : 'red';
        status.innerText = data.resultado;
    } catch (e) {
        status.style.color = 'red';
        status.innerText = "Erro ao enviar: " + e;
    }
}

async function atualizarMensagens() {
    try {
        const resp = await fetch('/mensagens');
        const data = await resp.json();
        document.getElementById('mensagens').value = data.mensagens;
        document.getElementById('status').innerText = 'Mensagens atualizadas.';
        document.getElementById('status').style.color = 'green';
    } catch (e) {
        document.getElementById('status').innerText = 'Erro ao atualizar mensagens: ' + e;
        document.getElementById('status').style.color = 'red';
    }
}

async function buscarIPs() {
    const ipsEl = document.getElementById('ips');
    ipsEl.innerText = 'Buscando...';
    try {
        const resp = await fetch('/buscar_ips');
        const data = await resp.json();
        if (resp.ok) {
            if (Array.isArray(data.ips) && data.ips.length) {
                ipsEl.innerText = data.ips.join('\\n');
            } else {
                ipsEl.innerText = '(nenhum IP retornado)';
            }
            document.getElementById('status').innerText = 'Busca de IPs concluída.';
            document.getElementById('status').style.color = 'green';
        } else {
            ipsEl.innerText = 'Erro: ' + (data.error || 'Resposta inválida');
            document.getElementById('status').innerText = 'Erro na busca de IPs.';
            document.getElementById('status').style.color = 'red';
        }
    } catch (e) {
        ipsEl.innerText = 'Erro ao contatar servidor de descoberta: ' + e;
        document.getElementById('status').innerText = 'Erro na busca de IPs.';
        document.getElementById('status').style.color = 'red';
    }
}
</script>
</body>
</html>
"""

# ---------------- ROTAS ----------------

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/mensagens")
def listar_mensagens():
    if os.path.exists(ARQUIVO_MSG):
        with open(ARQUIVO_MSG, "r", encoding="utf-8") as f:
            conteudo = f.read()
    else:
        conteudo = "(Nenhuma mensagem recebida ainda.)"
    return jsonify({"mensagens": conteudo})

@app.route("/enviar", methods=["POST"])
def enviar():
    dados = request.get_json(force=True)
    destino = dados.get("destino", "").strip()
    mensagem = dados.get("mensagem", "").strip()
    if not destino or not mensagem:
        return jsonify({"resultado": "Destino e mensagem são obrigatórios."}), 400

    try:
        resp = requests.post(f"http://{destino}/mensagem", data=mensagem.encode(), timeout=5)
        return jsonify({"resultado": f"Mensagem enviada para {destino} (status {resp.status_code})."})
    except Exception as e:
        return jsonify({"resultado": f"Erro ao enviar: {e}"}), 500

@app.route("/mensagem", methods=["POST"])
def receber():
    msg = request.get_data(as_text=True)
    ip1 = request.headers.getlist('X-Forwarded-For')[0] if request.headers.getlist('X-Forwarded-For') else ''
    ip2 = request.remote_addr or ''
    ip = ip1 if ip1 else ip2

    with open(ARQUIVO_MSG, "a", encoding="utf-8") as f:
        f.write(f"{ip}: {msg}\n")
    print(f">>> MENSAGEM RECEBIDA de {ip}: {msg}")
    return "OK", 200

@app.route("/buscar_ips")
def buscar_ips():
    try:
        r = requests.get(SERVIDOR_DESTINO, timeout=5)
        if r.ok:
            ips = r.json()
            if isinstance(ips, list):
                return jsonify({"ips": ips})
            else:
                return jsonify({"error": "Resposta inesperada do servidor de descoberta."}), 500
        else:
            return jsonify({"error": f"Servidor de descoberta respondeu com status {r.status_code}."}), 502
    except Exception as e:
        return jsonify({"error": f"Erro ao contatar servidor de descoberta: {e}"}), 502

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print(f"Servidor iniciado em http://0.0.0.0:{PORTA_LOCAL}")
    print(f"Servidor de descoberta configurado em: {SERVIDOR_DESTINO}")
    app.run(host="0.0.0.0", port=PORTA_LOCAL, debug=False, use_reloader=False)