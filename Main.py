from operacoesbd import *

opcao = 0
connection = criarConexao('127.0.0.1', 'root', '0000', 'ouvidoria')
while opcao != 7:
    print("""
    +---------------------------------------+
    |             MENU PRINCIPAL            |
    +---------------------------------------+
    | 1: Listar Manifestações               |
    | 2: Listar por categoria               |
    | 3: Criar Manifestação                 |
    | 4: Exibir quantidade de manifestações |
    | 5: Pesquisar manifestação por código  |
    | 6: Excluir Manifestação pelo Código   |                    
    | 7: Sair do Sistema                    |
    +---------------------------------------+
    """)
    opcao = int(input('Qual opção deseja? '))

    if opcao == 1:
        # Imprimir todas as manifestacoes do BD
        busca = 'select * from manifestacoes'
        manifestacoes = listarBancoDados(connection, busca)

        if manifestacoes is None or len(manifestacoes) == 0:
            print('Nenhuma manifestação encontrada!')
        else:
            # f-string para deixar com aparência de tabela
            print(f"{'Codigo|':<6} {'Descricao':<50} {'|Categoria':<15}")
            print("=" * 70)
            for manifestacao in manifestacoes:
                Codigo, Descricao, Categoria = manifestacao
                print(f"{Codigo:<6} {Descricao:<52} {Categoria:<15}")

    elif opcao == 2:
        # Listar por categoria
        # Sempre usando PlaceHolders para evitar SQL injection
        tipo = input('Informe a categoria da manifestação: ').capitalize()
        sql = 'SELECT * FROM manifestacoes WHERE Categoria = %s'
        manifestacoes = listarBancoDados(connection, sql, (tipo,))

        if len(manifestacoes) == 0:
            print('Nenhuma manifestação encontrada nessa categoria!')
        else:
            # f-string para deixar com aparência de tabela
            print(f"{'Codigo|':<6} {'Descricao':<50} {'|Categoria':<15}")
            print("=" * 70)
            for manifestacao in manifestacoes:
                Codigo, Descricao, Categoria = manifestacao
                print(f"{Codigo:<6} {Descricao:<52} {Categoria:<15}")

    elif opcao == 4:
        # Comando que seleciona todas as colunas e conta a quantidade de linhas
        sql = 'SELECT COUNT(*) FROM `ouvidoria`.`manifestacoes`;'
        qtdManifestacoes = listarBancoDados(connection, sql, )
        # variavel para acessar a primeira posicao dentro da tupla
        numTotal = str(qtdManifestacoes[0][0])
        if numTotal == 0:
            print('Nenhuma manifestação encontrada!')
        else:
            print('Existem um total de ' + numTotal + ' manifestações cadastradas!')


    elif opcao == 3:
        # Adicionar manifestacao
        categoria = input('Informe a categoria da manifestação: (Crítica, Elogio, Sugestão) ').capitalize()

        descricoesValidas = ['Crítica', 'Elogio', 'Sugestão']
        #verificador para parametrizar as categorias
        if categoria not in descricoesValidas:
            print('Categoria inválida!')

        else:
            descricao = input('Descreva em seguida sua manifestação: ').capitalize()
        # Após capturar os dados da manifestacao agrupa-os em uma tupla para inserir no BD
        # Respeitando a ordem pra funcionar nos placeholders
            dados = (categoria, descricao)
            sql = 'INSERT INTO manifestacoes (Categoria, Descricao) VALUES (%s, %s)'
            insertNoBancoDados(connection, sql, dados)
            print('Manifestação adicionada com sucesso!')

    elif opcao == 6:
        # Excluir manifestação
        codManifestacao = input('Informe o código da manifestação que você gostaria de excluir: ').capitalize()
        busca = 'SELECT Codigo FROM manifestacoes'
        manifestacoes = listarBancoDados(connection, busca)

        # verificacao para ver se existe uma manifestacao correspondente ao codigo
        if manifestacoes is None or len(manifestacoes) == 0:
            print('Nenhuma manifestação encontrada!')
        else:

            # Extrai os codigos de manifestacoes da lista de tuplas e converter para strings
            codigosManifestacoes = [str(manifestacao[0]) for manifestacao in manifestacoes]

        if codManifestacao not in codigosManifestacoes:
                print('Manifestação não encontrada!')
        else:
            sql = 'DELETE FROM manifestacoes WHERE Codigo = %s'

            excluirBancoDados(connection, sql, (codManifestacao,))
            print('Manifestação excluida com sucesso!')

    elif opcao == 5:
        # Captura o codigo e passa na busca como parametro usando placeholders
        codigo = input('Informe o codigo da manifestação: ').capitalize()
        sql = 'SELECT * FROM manifestacoes WHERE Codigo = %s'
        manifestacoes = listarBancoDados(connection, sql, (codigo,))

        if len(manifestacoes) == 0:
            print('Nenhuma manifestação encontrada com esse codigo!')
        else:
            # f-string para deixar com aparencia de tabela
            print(f"{'Codigo|':<6} {'Descricao':<50} {'|Categoria':<15}")
            print("=" * 70)
            for manifestacao in manifestacoes:
                Codigo, Descricao, Categoria = manifestacao
                print(f"{Codigo:<6} {Descricao:<52} {Categoria:<15}")

    elif opcao == 7:
        encerrarBancoDados(connection)
        break

    else:
        print('Opção inválida!')
