import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
JSON_PATH = os.path.join(os.path.dirname(__file__), 'data', 'dados_iniciais.json')

def iniciar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Criando a tabela de ocorrências
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ano INTEGER,
            estado TEXT,
            cidade TEXT,
            tipo_violencia_previa TEXT,
            casos INTEGER
        )
    ''')
    
    # Verifica se o banco já tem dados, se não tiver, popula com o JSON
    cursor.execute("SELECT COUNT(*) FROM ocorrencias")
    if cursor.fetchone()[0] == 0:
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for item in dados:
                    cursor.execute('''
                        INSERT INTO ocorrencias (ano, estado, cidade, tipo_violencia_previa, casos)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (item['ano'], item['estado'], item['cidade'], item['tipo_violencia_previa'], item['casos']))
            conn.commit()
            print("Dados inseridos no banco com sucesso!")
        else:
            print("Aviso: Arquivo JSON não encontrado para popular o banco.")
    
    conn.close()

if __name__ == '__main__':
    iniciar_banco()
    print("Banco de dados inicializado!")