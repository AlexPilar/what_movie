import streamlit as st
import google.generativeai as genai
import ast

st.set_page_config(layout='wide')
chave = st.secrets['GEMINI_KEY']

st.title("Qual filme devo assistir?")

filmes_assist = []
def pesquisar_filme(chave, genero, streaming, lista):
    genai.configure(api_key=chave)
    modelo = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f''' Liste os 5 principais filmes do {genero} do {streaming} streaming com uma breve descrição até 40 palavras.
    A string de resposta deve estar na forma de duas listas: 
    ['filme1 (ano)', 'filme2 (ano)', 'filme3 (ano)', 'filme4 (ano)', 'filme5 (ano)']
    |['descricao1', 'descricao2', 'descricao3', 'descricao4', 'descriacao5']
    
    Recomendar 1 filme clássico, 1 dos anos 2000 e 3 mais recentes, a partir de 2010.
    
    Os filmes não devem estar presentes na {lista}. Se estiver vazia, sugira os melhores possíveis
    
    Não quero observação nenhuma, apenas o nome e descrição, como solicitado. Nenhuma instrução adicional, apenas
    retornar o dicionário.
    Sem espaços antes e depois de começar as listas. Apenas quero elas separadas por |.
    '''
    resposta = modelo.generate_content(prompt)
    return resposta.text


# Opções de gênero
opcoes_genero = ["Selecione uma opção", "Ação", "Terror", "Comédia"]
opcoes_streamings = ["Selecione uma opção", "Netflix", "Amazon Prime", "Max", "Disney", "Qualquer um"]

# Escolhas do usuário
escolha_genero = st.selectbox("Escolha uma opção:", opcoes_genero)
escolha_stream = st.selectbox("Escolha uma opção:", opcoes_streamings)

# Verifica se o gênero e o streaming foram selecionados
if escolha_genero != 'Selecione uma opção' and escolha_stream != 'Selecione uma opção':
    st.markdown(f'Aqui estão as 5 principais opções de filmes de {escolha_genero} para assistir:')

    # Obter filmes escolhidos
    filmes_escolhidos = pesquisar_filme(chave, escolha_genero, escolha_stream, filmes_assist)
    titulos, descricoes = filmes_escolhidos.split("|")

    # Converter as strings de títulos e descrições para listas
    titulos = ast.literal_eval(titulos)
    descricoes = ast.literal_eval(descricoes)

    # Exibir os primeiros 5 filmes
    for i in range(5):
        titulo = titulos[i]
        descricao = descricoes[i]

        # Exibe o título e a descrição
        st.subheader(titulo)
        st.write(descricao)

        # Adiciona o título à lista de filmes assistidos
        filmes_assist.append(titulo)

    # Exibir o botão para gerar mais opções
    if st.button("Gerar mais opções", key="gerar_opcoes"):
        # Gerar mais filmes enquanto o botão for clicado
        filmes_escolhidos = pesquisar_filme(chave, escolha_genero, escolha_stream, filmes_assist)
        titulos, descricoes = filmes_escolhidos.split("|")

        # Converter as strings de títulos e descrições para listas
        titulos = ast.literal_eval(titulos)
        descricoes = ast.literal_eval(descricoes)

        # Exibir novos filmes
        for i in range(len(titulos)):
            titulo = titulos[i]
            descricao = descricoes[i]

            # Verifica se o título já foi assistido
            if titulo not in filmes_assist:
                filmes_assist.append(titulo)  # Adiciona o título aos assistidos
                st.subheader(titulo)  # Exibe o título
                st.write(descricao)  # Exibe a descrição