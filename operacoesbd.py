import mysql.connector

def criarConexao(endereco,usuario, senha, bancodedados):
      return mysql.connector.connect(
  host=endereco,user=usuario, password=senha,database=bancodedados)

def encerrarBancoDados(connection):
      connection.close()

def insertNoBancoDados(connection,sql,params):
      cursor = connection.cursor()
      cursor.execute(sql, params)
      connection.commit()
      id = cursor.lastrowid
      cursor.close()
      return id

def listarBancoDados(conexao, sql, params=None):
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, params)
        resultado = cursor.fetchall()
        return resultado
    except mysql.connector.Error as err:
        print(f"Erro ao executar a consulta: {err}")
    finally:
        cursor.close()

def atualizarBancoDados(connection,sql, params):
      cursor = connection.cursor()
      cursor.execute(sql, params)
      connection.commit()
      linhasAfetadas = cursor.rowcount
      cursor.close()
      return linhasAfetadas

def excluirBancoDados(connection,sql, params):
      cursor = connection.cursor()
      cursor.execute(sql, params)
      connection.commit()
      linhasAfetadas = cursor.rowcount
      cursor.close()
      return linhasAfetadas
