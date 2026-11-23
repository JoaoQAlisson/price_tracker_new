import os
import psycopg2
from datetime import datetime

# chave do database no git
DATABASE_URL = os.environ.get("DATABASE_URL")

def inicializar_banco():
    """Inicializa o banco de dados, cria uma tabela se necessário """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id SERIAL PRIMARY KEY,
            produto TEXT NOT NULL,
            preco REAL NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def salvar_preco(nome_produto, preco):
    """Salva os valores no database"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO registros (produto, preco, data_hora)
        VALUES (%s, %s, %s)
    ''', (nome_produto, preco, data_hora_atual)) 
    
    conn.commit()
    cursor.close()
    conn.close()