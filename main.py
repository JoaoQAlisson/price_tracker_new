import os
import time
from scraper import extrair_preco
from database import salvar_preco, inicializar_banco
from notifier import enviar_mensagem

""" 
Os valores são salvos em um banco de dados, ao fim do ano (após a Black Friday) pretende-se fazer uma análise da evolução temporal dos preços 
"""

LISTA_PRODUTOS = [
    {
        "nome": "PS5 Slim Dig - 825Gb - Pct AstroBot+Gran",
        "url": "https://www.amazon.com.br/gp/product/B0FPGF9J2J/ref=ox_sc_act_title_1?smid=A1ZZFT5FULY4LN&psc=1",
        "alvo": 4000.00,
        "tag": "span",
        "classe": "highlight-total-line-desktop"
    },
    {
        "nome": "PS5 Slim Dig - 825Gb - S/Jogos",
        "url": "https://www.amazon.com.br/Sony-PlayStation-Edição-Digital-Controle/dp/B0GWNKJDCZ/ref=sr_1_2?__mk_pt_BR=ÅMÅŽÕÑ&crid=3MQ5MI6DS8I6X&dib=eyJ2IjoiMSJ9.0TWYKganEp-3_8_Isg7DEBPhBv9oj7clyYGDf1WiySoVbw-6Mwov2k2bddyf4TafO05kF7aJCwUxJUmEsBRUHReUmkTtYja9vHr"
        "_H4dkETXX6k1CDVGAvW4iYkRImw1_eL_IcIwfNjKsKiEujNA24dPiT2vL69AqOuMsNjZu-eWsAJ1BvFDR0psMEmlUliroqQFKtDK0_I_bKreg_373l9Rkgkrz42nfvRzhmrmuwZTYsT9r6B74RvYqFPn3tYecAzR3lgxXzs4SG2_5YRefWnpabr_TQplM0Yg7Xiv_J70.otpCYdPPQ9HjUjafITXa0Xo1w6bQSoE4OSjO-xswLhs&dib_tag=se&keywords=sony+playstation+5+slim&qid=1795611934&sprefix=sony+playstation+5+slim+%2Caps%2C270&sr=8-2&ufe=app_do%3Aamzn1.fos.95de73c3-5dda-43a7-bd1f-63af03b14751",
        "alvo": 3800.00,
        "tag": "span",
        "classe": "highlight-total-line-desktop"
    },
    {
        "nome": "PS5 Slim Dig 825Gb + GTA VI + AstroBot + Gran ",
        "url": "https://www.amazon.com.br/Bundle-GTA-PlayStation-Slim-Digital/dp/B0H6LVH152/ref=sr_1_6?brr=1&dib=eyJ2IjoiMSJ9._FCLhj9XU-hEdG3fD-U35DYTp2GQj492MqboULIQJI3KtyQI_aP48dVU73DoJkKQwKAUALOY_Sn3j1UKom9dj4PtnNVM0Tk16Ghh4l7b2_Fvc5NZ85Y6DvekuAV1PPo90O_"
        "e3l4jeAG6AG3ItkwN6GiIOrxYtNEkS5PHVtmsKMj06RfWL-Xdfhez6gIcAKZKS-3aN-78Lg6DdwLxmIjn38KNaA601Wu0OR_oKxxIBMY.JimE7O5nuuGTS8MmwU4rM8Vk8cvKbwCPJsGIjzrDpEk&dib_tag=se&qid=1795444025&rd=1&s=videogames&sr=1-6",
        "alvo": 4500.00,
        "tag": "span",
        "classe": "highlight-total-line-desktop"
    }
    
]

# iniciando o programa!! 
inicializar_banco()
print(f"Iniciando varredura de {len(LISTA_PRODUTOS)} produtos...")

for produto in LISTA_PRODUTOS:
    nome = produto["nome"]
    url = produto["url"]
    alvo = produto["alvo"]
    tag = produto["tag"]       
    classe = produto["classe"]
    
    print(f"\n--- Checando: {nome} ---")
    
    preco_atual = extrair_preco(url, tag, classe)
    
    if preco_atual is not None:
        print(f"Preço capturado: R$ {preco_atual:.2f}")

        # salvar no banco de dados
        salvar_preco(nome, preco_atual)
        print("Salvo no banco de dados.")
        
        # Dispara alerta no instagram (se bater corretamente o preço)
        if preco_atual <= alvo:
            mensagem = f"\U0001F6A8 *ALERTA DE PREÇO!*\n\n" \
                        f"*{nome}* atingiu o alvo!\n" \
                        f"Valor Atual: *R$ {preco_atual:.2f}*\n" \
                        f"Valor Desejado: R$ {alvo:.2f}\n\n" \
                        f"\U0001F517 [Link para compra]({url})"
            enviar_mensagem(mensagem)
            print("Alerta enviado para o Telegram.")
        else:
            print(f"Preço ainda acima do alvo (R$ {alvo:.2f}).")
    else:
        print(f"Falha ao extrair preço de: {nome}")
        
    time.sleep(5) 

print("\nVarredura múltipla finalizada. O GitHub desligará a máquina agora.")
