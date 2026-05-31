from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def obter_conexao_banco():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/dados', methods=['GET'])
def obter_dados():
    conn = obter_conexao_banco()
    cursor = conn.cursor()
    
    ano_filtro = request.args.get('ano')
    if ano_filtro:
        cursor.execute("SELECT * FROM ocorrencias WHERE ano = ?", (ano_filtro,))
    else:
        cursor.execute("SELECT * FROM ocorrencias")
        
    linhas = cursor.fetchall()
    conn.close()
    
    resultado = [dict(linha) for linha in linhas]
    return jsonify(resultado)

if __name__ == '__main__':
    from database import iniciar_banco
    iniciar_banco()
    app.run(debug=True, port=5000)