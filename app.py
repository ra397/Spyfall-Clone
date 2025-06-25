from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
from models.game_manager import GameManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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
    return redirect(url_for('view_lobby', code=game.code) + f'?name={name}')

@app.route('/join')
def join_game_form():
    return render_template('join_game.html')

@app.route('/games/join', methods=['POST'])
def join_game():
    name = request.form['name']
    code = request.form['code']

    try:
        game, error = manager.join_game(code, name)
        if game is None:
            return f"Error: {error}"

        socketio.emit('player_joined', {'name': name}, to=code)
        return redirect(url_for('view_lobby', code=code) + f'?name={name}')
    except ValueError as e:
        return f"Error: {e}"

@app.route('/games/<code>/lobby')
def view_lobby(code):
    name = request.args.get('name', '')
    game = manager.get_game(code)
    players = game.get_player_names()
    is_owner = (game.owner.name == name)
    return render_template('lobby.html', code=code, players=players, is_owner=is_owner, name=name)

@app.route('/games/<code>/start')
def game_page(code):
    name = request.args.get('name', '')
    game = manager.get_game(code)

    current_player = next((p for p in game.players if p.name == name), None)
    if not current_player:
        return "Error: player not in game"

    occupation = current_player.get_occupation()
    is_spy = current_player.is_spy()
    location = game.current_location if not is_spy else None
    start_time = int(game.get_start_time())
    is_owner = (game.owner.name == name)

    return render_template(
        'game.html',
        code=code,
        name=name,
        occupation=occupation,
        location=location,
        is_spy=is_spy,
        start_time=start_time,
        is_owner=is_owner
    )

@socketio.on('join_lobby')
def handle_join_lobby(data):
    join_room(data['code'])

@socketio.on('start_game')
def handle_start_game(data):
    code = data['code']
    game = manager.get_game(code)
    if game and not game.has_started():
        game.start()
        emit('start_game', to=code)


@socketio.on('end_round')
def handle_end_round(data):
    code = data['code']
    print(f"End round for game {code}")
    game = manager.get_game(code)
    if game:
        game.reset()
        emit('round_ended', {'code': code}, to=code)

if __name__ == '__main__':
    socketio.run(app, debug=True)