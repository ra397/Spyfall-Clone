from flask import Flask, render_template, request, redirect, url_for
from models.game_manager import GameManager

app = Flask(__name__)

manager = GameManager()

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create_game_form():
    return render_template('create_game.html')

@app.route('/games', methods=['POST'])
def create_game():
    name = request.form['name']
    game = manager.create_game(name)
    return redirect(url_for('view_lobby', code=game.code))

@app.route('/join')
def join_game_form():
    return render_template('join_game.html')

@app.route('/games/join', methods=['POST'])
def join_game():
    name = request.form['name']
    code = request.form['code']
    joined = manager.join_game(code, name)
    if joined is None:
        return f"Game not found"
    return redirect(url_for('view_lobby', code=code))

@app.route('/games/<code>/lobby')
def view_lobby(code):
    game = manager.get_game(code)
    players = game.get_player_names()
    return render_template('lobby.html', code=code, players=players)