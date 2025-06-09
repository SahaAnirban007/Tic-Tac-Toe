from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret'  # Needed for session

def win_check(x_position, z_position):
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]
    for win in wins:
        if sum([x_position[i] for i in win]) == 3:
            return 'player_O'
        if sum([z_position[i] for i in win]) == 3:
            return 'player_o'
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'x_position' not in session:
        session['x_position'] = [0]*9
        session['z_position'] = [0]*9
        session['turn'] = 1
        session['winner'] = None
        session['player_x'] = ''
        session['player_o'] = ''

    if request.method == 'POST':
        if 'player_x' in request.form and 'player_o' in request.form:
            # Save player names
            session['player_x'] = request.form['player_x']
            session['player_o'] = request.form['player_o']
        elif 'cell' in request.form and not session.get('winner'):
            # Handle move
            cell = int(request.form['cell'])
            x_position = session['x_position']
            z_position = session['z_position']

            if x_position[cell] == 0 and z_position[cell] == 0:
                if session['turn'] == 1:
                    x_position[cell] = 1
                else:
                    z_position[cell] = 1

                session['winner'] = win_check(x_position, z_position)
                session['turn'] = 1 - session['turn']
                session['x_position'] = x_position
                session['z_position'] = z_position

        return redirect(url_for('index'))

    return render_template("index.html",
                           x_position=session['x_position'],
                           z_position=session['z_position'],
                           turn=session['turn'],
                           winner=session['winner'],
                           player_x=session.get('player_x', ''),
                           player_o=session.get('player_o', ''))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)