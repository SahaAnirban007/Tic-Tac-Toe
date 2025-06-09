from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret'  # Needed for session

def checkWin(xState, zState):
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]
    for win in wins:
        if sum([xState[i] for i in win]) == 3:
            return 'X'
        if sum([zState[i] for i in win]) == 3:
            return 'O'
    return None

@app.route('/')
def index():
    if 'xState' not in session:
        session['xState'] = [0]*9
        session['zState'] = [0]*9
        session['turn'] = 1
        session['winner'] = None

    return render_template("index.html",
                           xState=session['xState'],
                           zState=session['zState'],
                           turn=session['turn'],
                           winner=session['winner'])

@app.route('/play/<int:cell>')
def play(cell):
    if session.get('winner'):
        return redirect(url_for('index'))

    xState = session['xState']
    zState = session['zState']
    turn = session['turn']

    if xState[cell] == 0 and zState[cell] == 0:
        if turn == 1:
            xState[cell] = 1
        else:
            zState[cell] = 1
        winner = checkWin(xState, zState)
        session['xState'] = xState
        session['zState'] = zState
        session['turn'] = 1 - turn
        session['winner'] = winner
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
