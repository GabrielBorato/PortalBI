import cx_Oracle
import pandas as pd

dados_conexao = {
    "user": "consinco",
    "password": "K0chC0n5",
    "dsn": "oraconsincoprd.superkoch.com.br:1521/consinco"}

caminho_arquivo_csv = "C:/Users/gabriel.borato/Documents/Dev/Portal BI/dados_exportados.csv"

try:
    conexao = cx_Oracle.connect(**dados_conexao)
    cursor = conexao.cursor()
    query = """
SELECT
A.NROEMPRESA AS EMPRESA,
TO_CHAR(A.DTAENTRADASAIDA, 'DD-MM-YYYY') AS DATA,
A.SEQPRODUTO AS COD_PRODUTO,
fcategoriafamilianivel(B.SEQFAMILIA, 1, 1, 'M') AS NIVEL1,
fcategoriafamilianivel(B.SEQFAMILIA, 1, 2, 'M') AS NIVEL2,
A.VLRTOTALVDA AS VL_VENDA,
A.QTDVDA AS QT_VENDA
FROM MRL_CUSTODIA A
JOIN MAP_PRODUTO B ON B.SEQPRODUTO = A.SEQPRODUTO
WHERE 0=0
AND TO_CHAR(A.DTAENTRADASAIDA, 'DD-MM-YYYY') = '24-12-2023'
"""  
    cursor.execute(query)
    colunas = [desc[0] for desc in cursor.description]
    resultados = pd.DataFrame(cursor.fetchall(), columns=colunas)

    resultados = resultados.rename(columns={
        'EMPRESA': 'Loja',
        'DATA': 'Data',
        'COD_PRODUTO': 'Código do Produto',
        'NIVEL1': 'Setor',
        'NIVEL2': 'Categoria',
        'VL_VENDA': 'Valor de Venda',
        'QT_VENDA': 'Quantidade de Venda'
    })

    resultados.to_csv(caminho_arquivo_csv, index=False)

except cx_Oracle.DatabaseError as ex:
    print(f"Falha na conexão: {ex}")

finally:
    if conexao:
        conexao.close()
        print("Conexão fechada.")

if conexao:
    print(resultados)