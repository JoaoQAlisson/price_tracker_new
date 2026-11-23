# Price Tracker Actions

Rastreador automático de preços da Amazon.com.br com alertas via Telegram, banco de dados PostgreSQL e execução agendada via **GitHub Actions** — sem necessidade de servidor próprio.

---

## 📌 Sobre o projeto

Este projeto monitora periodicamente o preço de produtos selecionados na Amazon Brasil (Pode-se utilizar diversos sites, a escolha da Amazon foi apenas para padronização). Quando um produto atinge ou fica abaixo do valor-alvo definido, uma mensagem de alerta é enviada automaticamente para o Telegram do usuário. Todos os preços capturados são armazenados em banco de dados para futura análise temporal, com foco especial no período da **Black Friday**.

---

## 🚀 Como funciona

```
GitHub Actions (agendado)
        │
        ▼
   main.py  ──► scraper.py  ──► ScraperAPI (contorna bloqueios da Amazon)
        │
        ├──► database.py  ──► PostgreSQL (armazena histórico de preços)
        │
        └──► notifier.py  ──► Telegram Bot (envia alerta se preço ≤ alvo)
```

1. O GitHub Actions executa o pipeline no horário agendado (A cada 12 Horas).
2. `scraper.py` usa a [ScraperAPI](https://www.scraperapi.com/) com renderização de JavaScript e IP brasileiro para extrair o preço de cada produto.
3. O preço capturado é salvo no banco de dados via `database.py` (PostgreSQL com `psycopg2`, utilizando [Neon](https://neon.com)).
4. Se o preço atual for menor ou igual ao valor-alvo, `notifier.py` dispara uma mensagem formatada no Telegram.

---

## 🗂️ Estrutura do projeto

```
Price_Tracker_Actions/
├── .github/
│   └── workflows/         # Workflow do GitHub Actions
├── main.py                # Orquestrador principal: itera sobre os produtos
├── scraper.py             # Web scraping via ScraperAPI + BeautifulSoup
├── database.py            # Conexão e persistência no PostgreSQL
├── notifier.py            # Envio de alertas via Telegram Bot API
├── requirements.txt       # Dependências Python
└── LICENSE                # Licença MIT
```

---

## ⚙️ Configuração

### 1. Pré-requisitos

- Conta na [ScraperAPI](https://www.scraperapi.com/) (para contornar bloqueios anti-bot)
- Bot do Telegram criado via [@BotFather](https://t.me/BotFather)
- Banco de dados PostgreSQL acessível remotamente ([Neon](https://neon.com))

### 2. Secrets do repositório

Acesse **Settings → Secrets and variables → Actions** e adicione:

| Secret | Descrição |
|---|---|
| `SCRAPER_API_KEY` | Chave da ScraperAPI |
| `TOKEN_KEY` | Token do bot do Telegram |
| `CHAT_ID_KEY` | ID do chat/usuário no Telegram |
| `DATABASE_URL` | URL de conexão do PostgreSQL |

### 3. Adicionar produtos monitorados

Edite a lista `LISTA_PRODUTOS` em `main.py`:

```python
LISTA_PRODUTOS = [
    {
        "nome": "Nome do Produto",
        "url": "https://www.amazon.com.br/...", # Ou outro site de vendas
        "alvo": 299.99,       # Preço-alvo para disparo do alerta
        "tag": "span",        # Tag HTML onde o preço aparece
        "classe": "a-offscreen"  # Classe CSS do elemento
    },
]
```

> **Dica:** As classes mais comuns na Amazon Brasil são `a-offscreen` (preço principal) e `a-price-whole` (parte inteira do preço), em alguns casos, apenas `a-price-whole` irá funcionar, atente-se também as páginas com _pop-ups_ pois pode gerar conflito no preço buscado.

---

## 🗄️ Banco de dados

A tabela `registros` é criada automaticamente na primeira execução:

```sql
CREATE TABLE IF NOT EXISTS registros (
    id        SERIAL PRIMARY KEY,
    produto   TEXT NOT NULL,
    preco     REAL NOT NULL,
    data_hora TEXT NOT NULL
);
```

O objetivo é acumular o histórico de preços ao longo do ano para realizar uma análise da evolução temporal após a Black Friday.

---

## 📦 Dependências

```
requests
beautifulsoup4
psycopg2-binary
```

Instale localmente com:

```bash
pip install -r requirements.txt
```

---

## 🔔 Exemplo de alerta no Telegram

```
🚨 *ALERTA DE PREÇO!*

*Kindle Paperwhite* atingiu o alvo!
Valor Atual: *R$ 429,90*
Valor Desejado: R$ 450,01

🔗 [Link para compra](https://www.amazon.com.br/...)
```

---

## 📅 Agendamento (GitHub Actions)

O workflow em `.github/workflows/` executa o script automaticamente no horário configurado via cron. Ao final de cada execução, a máquina virtual do GitHub é desligada — sem custos de infraestrutura contínua.

---

## 📄 Licença

Distribuído sob a licença [MIT](LICENSE). © 2026 João Alisson.

---
## 🙋 Autor

**João Alisson** — [github](https://github.com/JoaoQAlisson) & [website](https://joaoqalisson.github.io/Portifiolio/) 
