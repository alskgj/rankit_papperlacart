from json import loads, dumps
from elo import Match


def write_to_db(name: str, score: float):
    """Writes a new eloscore to memory

    :param name: playername
    :param score: eloscore
    """
    score = float(score)

    with open('db.json') as fo:
        data = loads(fo.read())

    data[name] = score

    with open('db.json', 'w') as fo:
        fo.write(dumps(data))


def player_exists_in_db(name: str):
    """Checks if a player is saved

    :param name: playername
    """
    with open('db.json') as fo:
        data = loads(fo.read())
    return name in data


def calculate_placing(data: dict):
    """
    >>> calculate_placing({'dimitri': 100, 'lukboe': 20, 'mario': 50, 'luigi': 50})
    {'dimitri': 1, 'mario': 2, 'luigi': 2, 'lukboe': 3}

    :param data: takes a dict[str: int]
    :return: dict[str: inst] with placing
    """

    sortedlist = sorted(data.items(), key=lambda a: int(a[1]), reverse=True)

    placing = {}
    last = None
    lastplace = 0

    for name, score in sortedlist:
        if score != last:
            lastplace += 1
            last = score
        placing[name] = lastplace

    return placing


def update_elo(data: dict):
    """ Gets 'raw' data and updates elo accordingly

    :param data: dict like {'dimitri': 100, 'lukboe': 20, 'mario': 50, 'luigi': 50}
    :return:
    """

    # just to make sure all scores are ints, or subclasses of int
    for element in data:
        data[element] = int(data[element])

    # transform dict from {name:score} to {name:placing}
    data = calculate_placing(data)
    match = Match()
    for name, placing in data.items():
        match.add_player(name, placing, get_elo_from_db(name))

    match.calculate_elo()
    for player in match.players:
        print(f'{player.name}: {player.elo_pre} -> {player.elo_post}')
        write_to_db(player.name, player.elo_post)


def get_elo_from_db(player: str):
    """ Elo lookup on database

    :param player:
    """
    with open('db.json') as fo:
        data = loads(fo.read())

    return data[player]
