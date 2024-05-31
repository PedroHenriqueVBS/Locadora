from operacoesbd import *

opcao = 0
connection = criarConexao('127.0.0.1', 'root', '0000', 'locadora')
while opcao != 6:
    print("""
    +-------------------------------+
    |         MENU PRINCIPAL        |
    +-------------------------------+
    | 1: Listar filmes              |
    | 2: Listar por categoria       |
    | 3: Pesquisar por nome         |
    | 4: Adicionar filme            |
    | 5: Excluir filme              |
    | 6: Sair                       |
    +-------------------------------+
    """)
    opcao = int(input('Qual opção deseja? '))
    if opcao == 1:
        # Imprimir todos os filmes do BD
        busca = 'select * from filmes'
        filmes = listarBancoDados(connection, busca)

        if len(filmes) == 0:  #verificador
            print('Nenhum filme disponivel!')

        else:
            print(filmes)

    elif opcao == 2:
        #Insere a categoria do filme como condicao na busca
        tipo = input('Informe a categoria do filme: ')

        sql = 'SELECT * FROM filmes WHERE Categoria = %s'

        filmes = listarBancoDados(connection, sql, (tipo,))

        if len(filmes) == 0:
            print('Nenhum filme nessa categoria!')

        else:
            print(filmes)

    elif opcao == 3:
        # Insere o nome do filme como condicao na busca
        nomeBusca = input('Informe o nome do filme: ')

        sql = 'SELECT * FROM filmes WHERE Nome = %s'

        filmes = listarBancoDados(connection, sql, (nomeBusca,))

        if len(filmes) == 0:
            print('Nenhum filme nessa categoria!')

        else:
            print(filmes)

    elif opcao == 4:

        nome = input('Informe o nome do filme: ')
        ano = int(input('Informe o ano do filme: '))
        diretor = input('Informe o diretor do filme: ')
        categoria = input('Informe o categoria do filme: ')
        dados = (nome, ano, diretor, categoria)

        sql = ' INSERT INTO filmes (Nome, Ano, Diretor, Categoria) VALUES (%s, %s, %s, %s)'
        insertNoBancoDados(connection, sql, dados)

    elif opcao == 5:
        nomeFilme = input('Informe o nome do filme que voce gostaria de excluir')
        sql = 'DELETE FROM filmes WHERE Nome = %s'

        excluirBancoDados(connection, sql, (nomeFilme,))




    elif opcao != 6:
        print('Opcao invalida!')
    else:
        encerrarBancoDados(connection)
