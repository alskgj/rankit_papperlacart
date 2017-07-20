from json import loads, dumps


def write_to_db(name: str, score: float):
    with open('db.json') as fo:
        data = loads(fo.read())

    data[name] = score

    with open('db.json', 'w') as fo:
        fo.write(dumps(data))


def player_exists(name: str):
    with open('db.json') as fo:
        data = loads(fo.read())
    return name in data


def update_elo_4players(data: dict):
    """http://sradack.blogspot.ch/2008/06/elo-rating-system-multiple-players.html

    First we calculate the score of each player,
    for example in a 2 player game the winner gets score 1 and the looser gets score 0.
    In a 4 player game first place gets score 1/2 and second place gets score 1/3

    The obtained score is then compared with the expected score and elo is updated accordingly

    :param data: {'dimitri': 100, 'lukboe': 20, 'mario': 50}
    :return: None
    """

    # sorting players by their score to determine place
    # we shuffle data.items() to randomize who gets advantage on same score (which should happen rarely)
    data = sorted(data.items(), key=lambda a: a[1])[::-1]
    playeronly = [e[0] for e in data] # makes finding place (==index) easy
    playercount = len(data)

    number_of_games = ((playercount*(playercount-1))/2)
    for playername, score in data:
        # score is the amount of points entered in the website
        # actual_score is the value used by the elo function as explained in the docstring
        place = playeronly.index(playername) + 1  # array index starts at 0, so we add one
        actual_score = (playercount - place) / number_of_games

        rating_player = get_elo(playername)
        estimator = 0
        for playername_iter, _ in data:
            if playername_iter != playername:
                rating_other = get_elo(playername_iter)
                estimator += 1/(1+10**((rating_other - rating_player)/400))/number_of_games

        new_rating = rating_player + 42*(actual_score - estimator)

        write_to_db(playername, new_rating)

    return None


def get_elo(player: str):
    with open('db.json') as fo:
        data = loads(fo.read())

    return data[player]


def _update_elo(playera: str, playerb: str, scorea: int):
    """
    :param playera: name of a player
    :param playerb: name of his mortal enemy
    :param scorea: 0 for loose of playera, 1 for win of playera
    """
    if playera == playerb:
        return

    # don't even ask
    K = 42
    K_DRUNK = 10

    with open('db.json') as fo:
        data = loads(fo.read())

    old_eloa = data[playera]
    old_elob = data[playerb]

    expected_resulta = 1/(1+10**((old_elob-old_eloa)/400))
    expected_resultb = 1-expected_resulta

    scoreb = 1-scorea
    new_eloa = old_eloa + K*(scorea-expected_resulta)
    new_elob = old_elob + K*(scoreb-expected_resultb)

    print(f'player {playera} with old eloscore {old_eloa} has new elo {new_eloa}')
    print(f'player {playerb} with old eloscore {old_elob} has new elo {new_elob}')
    print(f'total points: {new_eloa+new_elob}')
    print()

    data[playera] = new_eloa
    data[playerb] = new_elob

    with open('db.json', 'w') as fo:
        fo.write(dumps(data))

if __name__ == '__main__':
    get_elo('dimitri')
    update_elo_4players({'dimitri': 100, 'lukboe': 20, 'Superzwerg': 50, 'BEN': 12})
