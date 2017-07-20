from flask import Flask
from flask import render_template, request, redirect, url_for
from json import loads

from logic import update_elo_4players, write_to_db, player_exists

app = Flask(__name__)


@app.route("/")
def index():
    with open('db.json') as fo:
        data = loads(fo.read())

    # convert dict data to a list, sort by second element of
    # every item in list (which is elonumber hoo), then reverse order
    data = sorted(data.items(), key=lambda a: a[1])[::-1]
    data = [(user, round(score)) for user, score in data]
    return render_template('index.html', users=data)


@app.route("/submit", methods=["GET", "POST"])
def submit():
    print(request)
    if request.method == "POST":
        response = request.values
        print(response)

        player1 = response['player1']
        player2 = response['player2']
        player3 = response['player3']
        player4 = response['player4']

        # drunk = response['drunk']
        score1 = int(response['score1'])
        score2 = int(response['score2'])
        score3 = int(response['score3'])
        score4 = int(response['score4'])

        data = {player1: score1, player2: score2, player3: score3, player4: score4}
        update_elo_4players(data)

        return redirect(url_for('index'))
    else:
        print(request.method)

    with open('db.json') as fo:
        data = loads(fo.read())

    return render_template("score_submission.html", users=sorted(list(map(lambda a: a[0], data.items()))))


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == 'POST':
        playername = request.values['name']
        print(request.values, playername)
        if not player_exists(playername):
            write_to_db(playername, 1500)
    else:
        print(request.method)

    return render_template('add_user.html')