from flask import Blueprint, request, jsonify
from schemas.game import GameCreate, GameResponse

games_bp = Blueprint('games', __name__)

# Banco em memória (porque sim, é mais fácil)
games_db = []
next_id = 1

@games_bp.route('/', methods=['GET'])
def listar_games():
    """GET /api/games/ - Lista todos os jogos"""
    return jsonify({
        "total": len(games_db),
        "jogos": games_db
    }), 200

@games_bp.route('/<int:game_id>', methods=['GET'])
def buscar_game(game_id):
    """GET /api/games/{id} - Busca um jogo específico"""
    game = next((g for g in games_db if g['id'] == game_id), None)
    if game:
        return jsonify(game), 200
    return jsonify({"erro": "Jogo não encontrado"}), 404

@games_bp.route('/', methods=['POST'])
def criar_game():
    """POST /api/games/ - Adiciona um novo jogo (com validação Pydantic)"""
    global next_id
    
    try:
        dados = request.get_json()
        validado = GameCreate(**dados)
        
        novo_game = GameResponse(
            id=next_id,
            **validado.dict()
        )
        
        games_db.append(novo_game.dict())
        next_id += 1
        
        return jsonify({
            "mensagem": f"✅ {novo_game.nome} adicionado!",
            "jogo": novo_game.dict()
        }), 201
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@games_bp.route('/<int:game_id>', methods=['DELETE'])
def deletar_game(game_id):
    """DELETE /api/games/{id} - Remove um jogo da lista"""
    global games_db
    game = next((g for g in games_db if g['id'] == game_id), None)
    
    if not game:
        return jsonify({"erro": "Jogo não encontrado"}), 404
    
    games_db = [g for g in games_db if g['id'] != game_id]
    return jsonify({"mensagem": f"🗑️ {game['nome']} removido!"}), 200