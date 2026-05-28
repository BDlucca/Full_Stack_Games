const API_URL = 'http://localhost:5000/api/games';

async function carregarGames() {
    try {
        const response = await fetch(API_URL + '/');
        const data = await response.json();
        
        const container = document.getElementById('gamesList');
        
        if (!data.jogos || data.jogos.length === 0) {
            container.innerHTML = '<div class="text-center text-gray-500 py-8">Nenhum jogo ainda...</div>';
            return;
        }
        
        container.innerHTML = data.jogos.map(game => `
            <div class="game-card bg-gray-700 rounded-lg p-3 border border-gray-600">
                <div class="flex justify-between items-start">
                    <div>
                        <h3 class="font-bold text-white">${escapeHtml(game.nome)}</h3>
                        <div class="flex gap-2 mt-1 text-xs">
                            <span class="text-purple-300">🎭 ${game.genero}</span>
                            <span class="text-blue-300">🎮 ${game.plataforma}</span>
                            <span class="text-yellow-300">📅 ${game.ano_lancamento}</span>
                            <span class="text-pink-300">⭐ ${game.nota_pessoal}</span>
                        </div>
                    </div>
                    <button onclick="deletarGame(${game.id})" class="text-red-400 hover:text-red-300">
                        🗑️
                    </button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        document.getElementById('gamesList').innerHTML = `
            <div class="text-center text-red-400 py-8">
                ⚠️ Erro ao carregar<br>
                <span class="text-sm">Backend rodando? python app.py</span>
            </div>
        `;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function mostrarFeedback(mensagem, tipo) {
    const feedback = document.getElementById('feedback');
    const bg = tipo === 'sucesso' ? 'bg-green-900 border-green-700' : 'bg-red-900 border-red-700';
    feedback.className = `mt-4 p-2 rounded-lg border ${bg} text-white text-sm block`;
    feedback.innerHTML = tipo === 'sucesso' ? `✅ ${mensagem}` : `❌ ${mensagem}`;
    setTimeout(() => feedback.classList.add('hidden'), 3000);
}

async function deletarGame(id) {
    if (!confirm('Tem certeza?')) return;
    
    try {
        const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        const data = await response.json();
        
        if (response.ok) {
            mostrarFeedback(data.mensagem, 'sucesso');
            carregarGames();
        } else {
            mostrarFeedback(data.erro || 'Erro ao deletar', 'erro');
        }
    } catch (error) {
        mostrarFeedback('Erro de conexão', 'erro');
    }
}

document.getElementById('gameForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const novoGame = {
        nome: document.getElementById('nome').value,
        genero: document.getElementById('genero').value,
        plataforma: document.getElementById('plataforma').value,
        ano_lancamento: parseInt(document.getElementById('ano_lancamento').value),
        nota_pessoal: parseFloat(document.getElementById('nota_pessoal').value)
    };
    
    try {
        const response = await fetch(API_URL + '/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(novoGame)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarFeedback(data.mensagem, 'sucesso');
            document.getElementById('gameForm').reset();
            carregarGames();
        } else {
            mostrarFeedback(data.erro || 'Erro ao adicionar', 'erro');
        }
    } catch (error) {
        mostrarFeedback('Erro de conexão', 'erro');
    }
});

document.getElementById('refreshBtn').addEventListener('click', () => carregarGames());

carregarGames();