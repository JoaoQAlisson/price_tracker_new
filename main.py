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
        "url": "https://www.amazon.com.br/PlayStation®5-Slim-Digital-825GB-Turismo/dp/B0FPGF9J2J/ref=sr_1_2?brr=1&dib=eyJ2IjoiMSJ9._FCLhj9XU-hEdG3fD-U35DYTp2GQj492MqboULIQJI3KtyQI_aP48dVU73DoJkKQwKAUALOY_Sn3j1UKom9dj4PtnNVM0Tk16Ghh4l7b2_Fvc5NZ85Y6DvekuAV1PPo90O"
        "_e3l4jeAG6AG3ItkwN6GiIOrxYtNEkS5PHVtmsKMj06RfWL-Xdfhez6gIcAKZKS-3aN-78Lg6DdwLxmIjn38KNaA601Wu0OR_oKxxIBMY.JimE7O5nuuGTS8MmwU4rM8Vk8cvKbwCPJsGIjzrDpEk&dib_tag=se&qid=1795441523&rd=1&s=videogames&sr=1-2&ufe=app_do%3Aamzn1.fos.9e6a115c-05b9-4b96-8e1c-b1f9ce2ac1a6",
        "alvo": 4000.00,
        "tag": "span",
        "classe": "highlight-total-line-desktop"
    },
    {
        "nome": "PS5 Slim Dig - 825Gb - S/Jogos",
        "url": "https://www.amazon.com.br/Sony-PlayStation-Edição-Digital-Controle/dp/B0GWNKJDCZ/ref=pd_vtp_d_sccl_1_3/143-7284309-0532402?pd_rd_w=ak6n8&content-id=amzn1.sym.8151f597-9f36-4832-b1b2-97e67c93d249&pf_rd_p=8151f597-9f36-4832-b1b2-97e67c93d249&pf_"
        "rd_r=XR09GGCKJX7MC82D1Y0F&pd_rd_wg=IqUo6&pd_rd_r=c7fb6a86-984f-4c8c-a437-d2d16cd7f172&pd_rd_i=B0GWNKJDCZ&psc=1",
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
