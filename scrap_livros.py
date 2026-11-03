import requests
from bs4 import BeautifulSoup
from conexao_ora import conectar_oracle
from urllib.parse import urljoin


def coletar_livros():
    url = 'https://books.toscrape.com/'
    dados = []

    while url:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        livros = soup.find_all('article', class_='product_pod')

        for livro in livros:
            if len(dados) >= 40:
                break

            titulo = livro.h3.a['title']

            preco = float(
                livro.find('p', class_='price_color').text.strip().replace('£', '')
            )

            avaliacao = livro.find('p', class_='star-rating')['class'][1]

            disponibilidade = livro.find(
                'p', class_='instock availability'
            ).text.strip()

            dados.append((
                titulo,
                preco,
                avaliacao,
                disponibilidade
            ))

        if len(dados) >= 40:
            break

        proxima = soup.find('li', class_='next')

        if proxima:
            proxima_pagina = proxima.a['href']
            url = urljoin(url, proxima_pagina)
        else:
            url = None

    return dados


def salvar_oracle(dados):
    conn = conectar_oracle()

    if not conn:
        print('Não foi possível conectar ao Oracle.')
        return

    try:
        sql = '''
            INSERT INTO books
            (title, price, rating, availability)
            VALUES (:1, :2, :3, :4)
        '''

        cursor = conn.cursor()
        cursor.execute('DELETE FROM books')
        cursor.executemany(sql, dados)
        conn.commit()

        print(f'{len(dados)} livros inseridos com sucesso!')

    except Exception as e:
        print(f'Erro ao inserir dados: {e}')
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    dados = coletar_livros()

    for titulo, preco, avaliacao, disponibilidade in dados:
        print(f'{titulo} | {preco} | {avaliacao} | {disponibilidade}')

    salvar_oracle(dados)