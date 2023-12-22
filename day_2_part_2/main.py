def parse_input() -> list:
    f = open('input.txt', 'r', encoding="utf-8")
    games = []

    for line in f:
        #game format: {'id': int, 'tests': []}
        #test format: {'red': int, 'green': int, 'blue': int}
        game = {}

        id_part, data_part = line.removesuffix('\n').split(': ')
        game['id'] = int(id_part.removeprefix('Game '))
        tests = data_part.split('; ')
        game['tests'] = []
        for test_data in tests:
            test = {'red': 0, 'green': 0, 'blue': 0}
            cubes_data = test_data.split(', ')
            for cube_data in cubes_data:
                number, color = cube_data.split(' ')
                test[color] = int(number)
            game['tests'].append(test)
        games.append(game)
    return games

def check_game(game: dict) -> bool:
    for test in game['tests']:
        if test['red'] > 12:
            return False
        elif test['green'] > 13:
            return False
        elif test['blue'] > 14:
            return False
    return True

games = parse_input()
mysum = sum([game['id'] for game in games if check_game(game)])
print(mysum)