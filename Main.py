from operacoesbd import *

opcao = 0
connection = criarConexao('127.0.0.1', 'root', '0000', 'locadora')
while opcao != 7:
    print("""
    +-------------------------------+
    |         MENU PRINCIPAL        |
    +-------------------------------+
    | 1: Listar filmes              |
    | 2: Listar por categoria       |
    | 3: Pesquisar por nome         |
    | 4: Adicionar filme            |
    | 5: Excluir filme              |
    | 6: Alterar filme              |
    | 7: Sair                       |
    +-------------------------------+
    """)
    opcao = int(input('Qual opção deseja? '))

    if opcao == 1:
        # Imprimir todos os filmes do BD
        busca = 'select Nome, Ano, Diretor, Categoria from filmes'
        filmes = listarBancoDados(connection, busca)

        if len(filmes) == 0:
            print('Nenhum filme disponível!')
        else:
            # f-string para deixar com aparência de tabela
            print(f"{'Nome':<30} {'Ano':<5} {'Diretor':<20} {'Categoria':<15}")
            print("=" * 70)
            for filme in filmes:
                nome, ano, diretor, categoria = filme
                print(f"{nome:<30} {ano:<5} {diretor:<20} {categoria:<15}")

    elif opcao == 2:
        # Listar por categoria
        # Sempre usando PlaceHolders para evitar SQL injection
        tipo = input('Informe a categoria do filme: ').capitalize()
        sql = 'SELECT Nome, Ano, Diretor, Categoria FROM filmes WHERE Categoria = %s'
        filmes = listarBancoDados(connection, sql, (tipo,))

        if len(filmes) == 0:
            print('Nenhum filme nessa categoria!')
        else:
            print(f"{'Nome':<30} {'Ano':<5} {'Diretor':<20} {'Categoria':<15}")
            print("=" * 70)
            for filme in filmes:
                nome, ano, diretor, categoria = filme
                print(f"{nome:<30} {ano:<5} {diretor:<20} {categoria:<15}")

    elif opcao == 3:
        # Pesquisar por nome, passando por parâmentro sempre
        nomeBusca = input('Informe o nome do filme: ')
        sql = 'SELECT * FROM filmes WHERE Nome LIKE %s'
        filmes = listarBancoDados(connection, sql, (nomeBusca,))

        if len(filmes) == 0:
            print('Nenhum filme encontrado!')
        else:
            print(f"{'Nome':<30} {'Ano':<5} {'Diretor':<20} {'Categoria':<15}")
            print("=" * 70)
            for filme in filmes:
                nome, ano, diretor, categoria = filme
                print(f"{nome:<30} {ano:<5} {diretor:<20} {categoria:<15}")

    elif opcao == 4:
        # Adicionar filme
        nome = input('Informe o nome do filme: ').capitalize()
        ano = int(input('Informe o ano do filme: '))
        diretor = input('Informe o diretor do filme: ').capitalize()
        categoria = input('Informe a categoria do filme: ').capitalize()
        # Após capturar os dados do filme agrupa-os em uma tupla para inserir no BD
        # Respeitando a ordem pra funcionar nos placeholders

        dados = (nome, ano, diretor, categoria)
        sql = 'INSERT INTO filmes (Nome, Ano, Diretor, Categoria) VALUES (%s, %s, %s, %s)'
        insertNoBancoDados(connection, sql, dados)

    elif opcao == 5:
        # Excluir filme
        nomeFilme = input('Informe o nome do filme que você gostaria de excluir: ').capitalize()
        sql = 'DELETE FROM filmes WHERE Nome = %s'

        excluirBancoDados(connection, sql, (nomeFilme,))

    elif opcao == 6:
        # Alterar filme
        # Pergunta o nome e depois mostra as informações do filme
        altNomeFilme = input('Digite o nome do filme que você gostaria de alterar: ').capitalize()
        sqlNome = 'SELECT Nome, Ano, Diretor, Categoria FROM filmes WHERE Nome LIKE %s'
        filmes = listarBancoDados(connection, sqlNome, (altNomeFilme,))

        if len(filmes) == 0: #verificador
            print('Filme não encontrado!')
        else:
            print(f"{'Nome':<30} {'Ano':<5} {'Diretor':<20} {'Categoria':<15}")
            print("=" * 70)
            for filme in filmes:
                nome, ano, diretor, categoria = filme
                print(f"{nome:<30} {ano:<5} {diretor:<20} {categoria:<15}")

            # Pergunta qual informação o usuário quer alterar
            altFilme = input('O que você gostaria de alterar? ').capitalize()
            #verificador para que o usuário insira apenas colunas válidas
            colunas_validas = ['Nome', 'Ano', 'Diretor', 'Categoria']
            if altFilme not in colunas_validas:
                print("Coluna inválida.")
            else:
                # Solicita o novo valor para o campo selecionado
                # apenas a coluna está sendo passada diretamente na consulta pois não é possivel usar PlaceHolder
                # Atualiza e exibe mensagem de sucesso
                altThis = input(f'Qual é o novo valor para {altFilme}? ')
                sql = f'UPDATE filmes SET {altFilme} = %s WHERE Nome = %s'
                atualizarBancoDados(connection, sql, (altThis, altNomeFilme))
                print(f"Filme '{altNomeFilme}' atualizado com sucesso.")

    elif opcao == 7:
        encerrarBancoDados(connection)
        break

    else:
        print('Opção inválida!')
