import oracledb
import json

def carregar_config(caminho="config.json"):
    try:
        with open(caminho) as json_file:
            config = json.load(json_file)
        return config['user'], config['dsn'], config['password']
    except FileNotFoundError:
        return None

def conectar_oracle():
    user, dsn, password = carregar_config()

    if not password:
        password = input('Informe a sua senha: ')

    try:
        conn = oracledb.connect(user=user, dsn=dsn, password=password)
        print('Conectado com sucesso!')
        return conn
    except Exception as erro:
        print(f'Erro ao conectar: {erro}')
        return None

def testar_conexao():
    conn = conectar_oracle()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT sysdate FROM dual')
        resultado = cursor.fetchone()
        print(f'Teste ok: {resultado[0]}')
        cursor.close()
        conn.close()


if __name__ == '__main__':
    print('Teste')
    testar_conexao()