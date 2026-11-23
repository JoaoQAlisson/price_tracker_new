import os
import requests
from bs4 import BeautifulSoup

# chave api no git
API_KEY = os.environ.get("SCRAPER_API_KEY")

def extrair_preco(url_produto, tag_html, classe_html):
  
    url_api = "http://api.scraperapi.com"
    
    # enviando parametros
    parametros = {
        'api_key': API_KEY,
        'url': url_produto,
        'render': 'true',        # Liga o navegador invisível para garantir que o site carregue por inteiro
        'country_code': 'br'     # Uso apenas de Ip br
    }
    
    try:
        resposta = requests.get(url_api, params=parametros)
        resposta.raise_for_status() 
        
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        
        # elemento_preco = soup.find('span', class_='a-price-whole') 
        elemento_preco = soup.find(tag_html, class_=classe_html) 
        
        if elemento_preco:            
            preco_texto = elemento_preco.get_text()
            preco_limpo = preco_texto.replace('(total parcelado ', '').replace('R$', '').replace('.', '').replace(',', '.').replace(")", "").strip() #Ajustando texto do valro
            # print(preco_limpo)
            return float(preco_limpo)
            
        else:
            print(f"Erro: A tag {tag_html}, class= {classe_html} de preço não foi encontrada no HTML.")
            print("\n--- INÍCIO DO HTML RETORNADO PARA DEBUG ---")
            print(resposta.text[:2000]) 
            print("--- FIM DO HTML ---\n")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição pela API: {e}")
        return None

# #Ativar para testes!!!
# if __name__ == "__main__":
#     url_teste = "https://www.amazon.com.br/Bundle-GTA-PlayStation-Slim-Digital/dp/B0H6LVH152/ref=sr_1_6?brr=1&dib=eyJ2IjoiMSJ9._FCLhj9XU-hEdG3fD-U35DYTp2GQj492MqboULIQJI3KtyQI_aP48dVU73DoJkKQwKAUALOY_Sn3j1UKom9dj4PtnNVM0Tk16Ghh4l7b2_Fvc5NZ85Y6DvekuAV1PPo90O_e3l4jeAG6AG3ItkwN6GiIOrxYtNEkS5PHVtmsKMj06RfWL-Xdfhez6gIcAKZKS-3aN-78Lg6DdwLxmIjn38KNaA601Wu0OR_oKxxIBMY.JimE7O5nuuGTS8MmwU4rM8Vk8cvKbwCPJsGIjzrDpEk&dib_tag=se&qid=1795444025&rd=1&s=videogames&sr=1-6"
#     tag= "span"
#     classe= "highlight-total-line-desktop"
#     preco_atual = extrair_preco(url_teste,tag,classe)
