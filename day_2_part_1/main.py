from functools import reduce

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

def get_max_cubes(first: dict, second: dict) -> dict:
    result = {}
    result['red'] = first['red'] if first['red'] > second['red'] else second['red']
    result['green'] = first['green'] if first['green'] > second['green'] else second['green']
    result['blue'] = first['blue'] if first['blue'] > second['blue'] else second['blue']
    return result

def calc_game_power(game: dict) -> int:
    maxed =  reduce(get_max_cubes, game['tests'])
    return reduce(lambda acc, next: acc * next, maxed.values())

games = parse_input()
powers = map(calc_game_power, games)
mysum = sum(powers)
print(mysum)