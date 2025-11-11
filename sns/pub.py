import boto3
import json
import time
from datetime import datetime

# Configurar cliente SNS (ajuste a região conforme necessário)
sns = boto3.client('sns', region_name='us-east-1')

# ARN do seu tópico SNS
TOPIC_ARN = 'arn:aws:sns:us-east-1:844072903278:meu-topico'  # Substitua pelo seu

def enviar_keep_alive():
    timestamp = datetime.utcnow().isoformat()
    mensagem = {
        "type": "keep_alive",
        "timestamp": timestamp
    }
    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps(mensagem)
    )
    print(f"[{timestamp}] Keep alive enviado. MessageId: {response['MessageId']}")

if __name__ == "__main__":
    print("Iniciando publisher de keep alive a cada 60s...")
    while True:
        enviar_keep_alive()
        time.sleep(60)