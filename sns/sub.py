import json
import boto3
import requests
from flask import Flask, request

app = Flask(__name__)

# Substitua pelo ARN do seu tópico SNS
TOPIC_ARN = 'arn:aws:sns:us-east-1:844072903278:meu-topico'

# Cliente SNS
sns_client = boto3.client("sns", region_name="us-east-1")


def subscribe_to_sns():
    endpoint_url = 'http://18.214.15.141:5000/'  # IP público da EC2 subscriber

    try:
        response = sns_client.subscribe(
            TopicArn=TOPIC_ARN,
            Protocol='http',
            Endpoint=endpoint_url
        )
        subscription_arn = response.get("SubscriptionArn", "pending confirmation")
        print(f'Subscriber registrado. Subscription ARN: {subscription_arn}')
    except ClientError as e:
        print("Erro ao inscrever no SNS:", e)



@app.route('/', methods=['POST'])
def listener():
    try:
        # Captura o corpo bruto da requisição (em texto)
        data = request.data.decode('utf-8')
        message = json.loads(data)

        # Trata mensagem do tipo SubscriptionConfirmation
        if message['Type'] == 'SubscriptionConfirmation':
            subscribe_url = message['SubscribeURL']
            print("Confirmação de inscrição recebida. Acessando:", subscribe_url)

            r = requests.get(subscribe_url)
            if r.status_code == 200:
              print("Inscricao confirmada!")
            

        elif message['Type'] == 'Notification':
            print("Mensagem recebida:", message['Message'])

        return '', 200
    except Exception as e:
        print("Erro:", e)
        return '', 400


def main():
    # Inscreve o subscriber no SNS
    subscribe_to_sns()

    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()