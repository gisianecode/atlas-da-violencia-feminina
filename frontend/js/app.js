const API_URL = 'http://127.0.0.1:5000/api/dados';

// Instâncias globais dos gráficos para podermos destruir/recriar ao filtrar
let chartViolencia = null;
let chartEstados = null;

async function buscarDados(ano = '') {
    try {
        const url = ano ? `${API_URL}?ano=${ano}` : API_URL;
        const response = await fetch(url);
        const dados = await response.json();
        
        processarERenderizarGraficos(dados);
    } catch (error) {
        console.error("Erro ao buscar dados da API:", error);
    }
}

function processarERenderizarGraficos(dados) {
    // 1. Processando dados para Gráfico de Violência Prévia
    const violencias = {};
    const estados = {};

    dados.forEach(item => {
        // Agrupa por tipo de violência
        violencias[item.tipo_violencia_previa] = (violencias[item.tipo_violencia_previa] || 0) + item.casos;
        // Agrupa por estado
        estados[item.estado] = (estados[item.estado] || 0) + item.casos;
    });

    // Renderizar ou atualizar gráfico de pizza (Violência Prévia)
    if (chartViolencia) chartViolencia.destroy();
    const ctxV = document.getElementById('graficoViolencia').getContext('2d');
    chartViolencia = new Chart(ctxV, {
        type: 'pie',
        data: {
            labels: Object.keys(violencias),
            datasets: [{
                data: Object.values(violencias),
                backgroundColor: ['#e01e5a', '#36a2eb', '#ffce56', '#4a154b']
            }]
        }
    });

    // Renderizar ou atualizar gráfico de barras (Estados)
    if (chartEstados) chartEstados.destroy();
    const ctxE = document.getElementById('graficoEstados').getContext('2d');
    chartEstados = new Chart(ctxE, {
        type: 'bar',
        data: {
            labels: Object.keys(estados),
            datasets: [{
                label: 'Número de Casos',
                data: Object.values(estados),
                backgroundColor: '#4a154b'
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
    }
    });
}

// Ouvir alterações no filtro
document.getElementById('filtro-ano').addEventListener('change', (e) => {
    buscarDados(e.target.value);
});

// Inicializa carregando todos os dados
buscarDados();