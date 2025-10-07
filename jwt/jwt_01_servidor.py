from flask import request
from flask import Flask
from flask import jsonify

import jwt_lib_api

app = Flask(__name__)
app.secret_key = 'minha_chave_unica'


@app.route('/auth', methods=['POST'])
def auth():
    token = None
    if request.method == 'POST':
        user = request.json['user']
        password = request.json['password']

        if user == 'elsonabreu' and password == '12345':
            token = jwt_lib_api.create_token(user, 5, app.config['SECRET_KEY'])

    return jsonify({"token": str(token)}),200



@app.route("/protect", methods=['POST'])
def protect():
    if request.method == 'POST':
        token_received = request.json['token']

        payload = jwt_lib_api.verify_token(token_received, app.secret_key)

        if payload != None:
            return jsonify({"msg": "Access route protect " + payload['user']}),200
        else:
            return jsonify({"msg": "Access denied"}),403

    else:
        return jsonify({"msg": "Access denied"}),403



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)