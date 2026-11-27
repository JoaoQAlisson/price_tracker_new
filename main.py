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
        "url": "https://www.amazon.com.br/gp/product/B0GWNKJDCZ/ref=ewc_pr_img_4?smid=APJANL1RGWUHD&psc=1",
        "alvo": 3800.00,
        "tag": "span",
        "classe": "highlight-total-line-desktop"
    },
    {
        "nome": "PS5 Slim Dig 825Gb + GTA VI + AstroBot + Gran ",
        "url": "https://www.amazon.com.br/gp/product/B0H6LVH152/ref=ewc_pr_img_2?smid=A1ZZFT5FULY4LN&psc=1",
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
