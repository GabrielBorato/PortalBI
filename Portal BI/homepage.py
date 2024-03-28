from flask import Flask, render_template, request, jsonify
import pandas as pd
import locale

app = Flask(__name__)
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

# Leitura do CSV e dados iniciais
caminho_csv = "C:\\Users\\gabriel.borato\\Documents\\Dev\\Portal BI\\dados_exportados.csv"
dados_iniciais = pd.read_csv(caminho_csv)

@app.route('/')
def index():
    opcoes_setor = dados_iniciais['Setor'].unique().tolist()
    return render_template('portal.html', dados_filtrados=[], opcoes_setor=opcoes_setor)

@app.route('/obter_categorias', methods=['GET'])
def obter_categorias():
    setor_selecionado = request.args.get('Setor', default='', type=str)
    categorias = dados_iniciais[dados_iniciais['Setor'].astype(str).str.strip().str.lower() == setor_selecionado.strip().lower()]['Categoria'].unique().tolist()

    return jsonify(categorias)


@app.route('/carregar_dados')
def carregar_dados():
    filtro_loja = request.args.get('Loja', default='', type=str)
    filtro_data = request.args.get('Data', default='', type=str)
    filtro_codProd = request.args.get('Código do Produto', default='', type=str)
    filtro_setor = request.args.get('Setor', default='', type=str)
    filtro_categoria = request.args.get('Categoria', default='', type=str)
    filtro_valorVenda = request.args.get('Valor de Venda', default='', type=float)
    filtro_quantVenda = request.args.get('Quantidade de Venda', default='', type=int)

    dados_filtrados = filtrar_dados(
        dados_iniciais, filtro_loja, filtro_data, filtro_codProd, 
        filtro_setor, filtro_categoria, filtro_valorVenda, filtro_quantVenda
    )

    return jsonify(dados_filtrados.to_dict(orient='records'))
    

def filtrar_dados(dados, filtro_loja, filtro_data, filtro_codProd, filtro_setor, filtro_categoria, filtro_valorVenda, filtro_quantVenda):
    dados_filtrados = dados.copy()

    if filtro_loja:
        dados_filtrados = dados_filtrados[dados_filtrados['Loja'].astype(str) == filtro_loja]
    if filtro_data:
        dados_filtrados = dados_filtrados[dados_filtrados['Data'].astype(str).str.contains(filtro_data, case=False)]
    if filtro_codProd:
        dados_filtrados = dados_filtrados[dados_filtrados['Código do Produto'].astype(str).str.contains(filtro_codProd, case=False)]
    if filtro_setor:
        dados_filtrados = dados_filtrados[dados_filtrados['Setor'].astype(str).str.strip().str.lower() == filtro_setor.strip().lower()]
    if filtro_categoria:
        dados_filtrados = dados_filtrados[dados_filtrados['Categoria'].astype(str).str.contains(filtro_categoria, case=False)]
    if filtro_valorVenda:
        dados_filtrados = dados_filtrados[dados_filtrados['Valor de Venda'].astype(float).float.contains(filtro_valorVenda, case=False)]
    if filtro_quantVenda:
        dados_filtrados = dados_filtrados[dados_filtrados['Quantidade de Venda'].astype(int) == filtro_quantVenda]

    return dados_filtrados




if __name__ == '__main__':
    app.run(debug=True)
