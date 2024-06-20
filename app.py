from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Инициализация игрового поля
game_field = [[' ' for _ in range(3)] for _ in range(3)]

# Функция для рендеринга игрового поля
@app.route('/')
def index():
    return render_template('index.html', game_field=game_field)

# Функция для обработки хода игрока
@app.route('/make_move', methods=['POST'])
def make_move():
    row = int(request.form['row'])
    col = int(request.form['col'])
    player = request.form['player']

    if game_field[row][col] == ' ':
        game_field[row][col] = player
        return jsonify({'result': 'ok', 'game_field': game_field})
    else:
        return jsonify({'result': 'error', 'message': 'Cell is already occupied'})

# Функция для проверки победы
@app.route('/check_win', methods=['GET'])
def check_win():
    filled_cells = 0
    for i in range(3):
        if game_field[i][0] != ' ' and game_field[i][1] != ' ' and game_field[i][2] != ' ':  filled_cells += 3
        if game_field[i][0] == game_field[i][1] == game_field[i][2] != ' ':
            return jsonify({'result': 'win', 'player': game_field[i][0]})
        if game_field[0][i] == game_field[1][i] == game_field[2][i] != ' ':
            return jsonify({'result': 'win', 'player': game_field[0][i]})
    if game_field[0][0] == game_field[1][1] == game_field[2][2] != ' ':
        return jsonify({'result': 'win', 'player': game_field[0][0]})
    if game_field[0][2] == game_field[1][1] == game_field[2][0] != ' ':
        return jsonify({'result': 'win', 'player': game_field[0][2]})

    if filled_cells == 9: return jsonify({'result': 'draw'})

    return jsonify({'result': 'no_win'})

# Функция для сброса состояния игры
@app.route('/reset', methods=['GET'])
def reset_game():
    global game_field
    game_field = [[' ' for _ in range(3)] for _ in range(3)]
    return jsonify({'result': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)