function alternarTema() {
    document.body.classList.toggle('tema-claro');
    document.querySelector('header').classList.toggle('tema-claro');
    document.querySelector('#dadosTable').classList.toggle('tema-claro');
    document.querySelectorAll('th').forEach(function (elemento) {
        elemento.classList.toggle('tema-claro');
        
    });
}

function preencherOpcoesSetor(opcoesSetor) {
    var selectSetor = document.getElementById('filtroSetor');

    // Limpar as opções existentes
    selectSetor.innerHTML = '<option value="">Todos</option>';

    // Adicionar as novas opções
    for (var i = 0; i < opcoesSetor.length; i++) {
        var option = document.createElement('option');
        option.value = opcoesSetor[i];
        option.text = opcoesSetor[i];
        selectSetor.add(option);
    }
}
function carregarDadosFiltrados() {
    var filtroLoja = document.getElementById('filtroLoja').value;
    var filtroData = document.getElementById('filtroData').value;
    var filtroSetor = document.getElementById('filtroSetor').value;
    var filtroCategoria = document.getElementById('filtroCategoria').value;

    var url = '/carregar_dados?Loja=' + filtroLoja + '&Data=' + filtroData + '&Setor=' + filtroSetor + '&Categoria=' + filtroCategoria;

    fetch(url)
        .then(response => response.json())
        .then(dadosFiltrados => {
            console.log('Dados carregados:', dadosFiltrados); // Adicionado log para verificar os dados
            atualizarTabela(dadosFiltrados);
        })
        .catch(error => {
            console.error('Erro ao carregar dados:', error);
        });
}

function carregarOpcoesCategoria() {
    var setorSelecionado = document.getElementById('filtroSetor').value;
    var selectCategoria = document.getElementById('filtroCategoria');

    // Limpar as opções existentes
    selectCategoria.innerHTML = '<option value="">Todas</option>';

    // Se setorSelecionado não estiver vazio, faça a solicitação ao backend para obter as categorias
    if (setorSelecionado !== '') {
        var url = '/obter_categorias?Setor=' + setorSelecionado;

        fetch(url)
            .then(response => response.json())
            .then(opcoesCategoria => {
                // Adicionar as novas opções ao seletor de categoria
                for (var i = 0; i < opcoesCategoria.length; i++) {
                    var option = document.createElement('option');
                    option.value = opcoesCategoria[i];
                    option.text = opcoesCategoria[i];
                    selectCategoria.add(option);
                }

                carregarDadosFiltrados();
            })
            .catch(error => {
                console.error('Erro ao obter categorias:', error);
            });
    } else {

        carregarDadosFiltrados();
    }
}

document.getElementById('filtroSetor').addEventListener('change', carregarOpcoesCategoria);

document.getElementById('filtroCategoria').addEventListener('change', carregarDadosFiltrados);

// Defina a função atualizarTabela antes de carregar a página
function atualizarTabela(dadosFiltrados) {
    var tbody = document.querySelector('#dadosTable tbody');
    var totalValorVenda = 0;
    tbody.innerHTML = '';

    if (dadosFiltrados.length === 0) {
        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.colSpan = 7; // Defina o número de colunas na sua tabela
        td.textContent = 'Nenhum resultado encontrado';
        tr.appendChild(td);
        tbody.appendChild(tr);
    } else {
        var colunas = ['Loja', 'Data', 'Setor', 'Categoria','Código do Produto', 'Valor de Venda','Quantidade de Venda'];

        dadosFiltrados.forEach(function (row) {
            var tr = document.createElement('tr');
            tr.classList.add('tema-escuro');

            colunas.forEach(function (coluna) {
                var td = document.createElement('td');
                td.textContent = row[coluna];
                if (coluna === 'Valor de Venda') {
                    var valorFormatado = parseFloat(row[coluna]).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
                    td.textContent = valorFormatado;
                    totalValorVenda += parseFloat(row[coluna]);
                } else {
                    td.textContent = row[coluna];
                }

                tr.appendChild(td);
            });

            tbody.appendChild(tr);
        });

        // Atualiza o elemento HTML no header com a soma calculada
        var valorTotalElement = document.getElementById('valorTotal');
        valorTotalElement.textContent = 'R$ ' + totalValorVenda.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
}