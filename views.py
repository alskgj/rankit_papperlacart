from flask import Flask
from flask import render_template, request, redirect, url_for
from json import loads

from logic import update_elo, player_exists_in_db, write_to_db

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

        data = {}
        for i in range(1, 5):
            player = response['player'+str(i)]
            score = response['score'+str(i)]
            if player:
                data[player] = int(score)

        print(data)
        update_elo(data)

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
        if not player_exists_in_db(playername):
            write_to_db(playername, 1500)
    else:
        print(request.method)

    return render_template('add_user.html')