import os

# Obtém o caminho da pasta atual onde o script está sendo executado
pasta_atual = os.getcwd()

# Percorre todos os arquivos na pasta atual
for nome_arquivo in os.listdir(pasta_atual):
    if nome_arquivo.endswith('.webp'):
        novo_nome = nome_arquivo

        # Substitui o primeiro underline por um espaço
        partes = novo_nome.split('_', 1)
        if len(partes) > 1:
            novo_nome = partes[0] + ' ' + partes[1]

        # Inicializa o sufixo a ser adicionado ao final do nome do arquivo
        sufixo = ""

        if '_environment' in novo_nome:
            novo_nome = novo_nome.replace('_environment', '')
            sufixo = '_layer1'

        if '_juliaskin1' in novo_nome:
            novo_nome = novo_nome.replace('_juliaskin1', '')
            sufixo = '_layer2'

        elif '_juliaskin2' in novo_nome:
            novo_nome = novo_nome.replace('_juliaskin2', '')
            sufixo = '_layer2_julia2'

        if '_simonskin2' in novo_nome:
            novo_nome = novo_nome.replace('_simonskin2', '')
            sufixo = '_layer3_simon2'

        elif '_simonskin1' in novo_nome:
            novo_nome = novo_nome.replace('_simonskin1', '')
            sufixo = '_layer3_simon1'

        elif '_simonskin' in novo_nome:
            novo_nome = novo_nome.replace('_simonskin', '')
            sufixo = '_layer3'

        # Adiciona o sufixo antes da extensão .webp
        if sufixo:
            novo_nome = novo_nome.replace('.webp', f'{sufixo}.webp')

        # Renomeia o arquivo
        caminho_antigo = os.path.join(pasta_atual, nome_arquivo)
        caminho_novo = os.path.join(pasta_atual, novo_nome)
        os.rename(caminho_antigo, caminho_novo)
        print(f'Renomeado: {nome_arquivo} -> {novo_nome}')
