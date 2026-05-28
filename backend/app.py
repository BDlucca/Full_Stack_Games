from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from blueprints.games import games_bp
from blueprints.swagger import SWAGGER_URL, API_URL, swaggerui_blueprint

app = Flask(__name__)
CORS(app, origins=["http://localhost:5500", "http://127.0.0.1:5500"])

# Swagger
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Blueprints
app.register_blueprint(games_bp, url_prefix='/api/games')

@app.route('/')
def home():
    return jsonify({
        "mensagem": "🎮 Games API rodando!",
        "docs": f"http://localhost:5000{SWAGGER_URL}"
    })

@app.route('/static/swagger.json')
def swagger_json():
    from flask import send_from_directory
    return send_from_directory('static', 'swagger.json')

if __name__ == '__main__':
    app.run(debug=True, port=5000)