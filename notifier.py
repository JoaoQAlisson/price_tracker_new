import requests
import os

#chave do token e id do telegram no git
TOKEN = os.environ.get("TOKEN_KEY")
CHAT_ID = os.environ.get("CHAT_ID_KEY")

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown" # formatar o texto
    }
    
    try:
        resposta = requests.post(url, json=payload)
        resposta.raise_for_status()
        print("Mensagem enviada com sucesso para o Telegram!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")

# # Descomente para testar!
# if __name__ == "__main__":
#    enviar_mensagem("Teste Bot")