import streamlit as st
from conexao_ora import conectar_oracle

SQL_BUSCAR_LIVROS = """
    SELECT title, price, rating, availability
    FROM books
    WHERE UPPER(title) LIKE UPPER(:termo)
    ORDER BY title
"""

# O site salva a avaliação por extenso ("Three"); convertemos para número
ESTRELAS = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}


def consultar(sql, termo=''):
    conn = conectar_oracle()
    if not conn:
        st.error('Não foi possível conectar ao Oracle.')
        return []

    with conn, conn.cursor() as cursor:
        cursor.execute(sql, termo=f'%{termo}%')
        return cursor.fetchall()


def montar_livros(linhas):
    return [
        {
            'Título': titulo,
            'Preço (£)': preco,
            'Avaliação': ESTRELAS[avaliacao],
            'Disponibilidade': disponibilidade,
        }
        for titulo, preco, avaliacao, disponibilidade in linhas
    ]


def mostrar(livros):
    if not livros:
        st.info('Nenhum dado encontrado')
        return

    st.caption(f'Encontrados {len(livros)} livros')

    preco_medio = sum(l['Preço (£)'] for l in livros) / len(livros)
    avaliacao_media = sum(l['Avaliação'] for l in livros) / len(livros)

    c1, c2, c3 = st.columns(3)
    c1.metric('Livros', len(livros))
    c2.metric('Preço médio', f'£ {preco_medio:.2f}')
    c3.metric('Avaliação média', f'{avaliacao_media:.1f} ★')

    st.dataframe(
        livros,
        hide_index=True,
        use_container_width=True,
        column_config={
            'Preço (£)': st.column_config.NumberColumn(format='£ %.2f'),
            'Avaliação': st.column_config.NumberColumn(format='%d ★'),
        },
    )


st.set_page_config(page_title='Livros', page_icon='📚', layout='wide')
st.title('📚 Catálogo de Livros')
st.write('Dados coletados de books.toscrape.com e armazenados no Oracle.')

with st.sidebar:
    st.header('Filtros')
    termo = st.text_input('Buscar por título')
    estrelas_min = st.slider('Avaliação mínima', 1, 5, 1)
    preco_max = st.slider('Preço máximo (£)', 0, 100, 100)

livros = montar_livros(consultar(SQL_BUSCAR_LIVROS, termo))

# Buscando por título, mostra tudo que bater; sem busca, aplica os filtros
if termo:
    st.caption('Filtros de avaliação e preço ignorados durante a busca.')
else:
    livros = [
        l for l in livros
        if l['Avaliação'] >= estrelas_min and l['Preço (£)'] <= preco_max
    ]

mostrar(livros)