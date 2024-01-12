from typing import List,TypeVar

def parse_input(filename: str) -> List[List[str]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        output.append(list(line.removesuffix('\n')))
    return output

def write_debug(input: List[List[str]]):
    file = open('debug.txt', 'w', encoding='utf-8')
    for row in input:
        line = ', '.join([str(x) for x in row])+'\n'
        file.write(line)

def get_galaxies_list(input: List[List[str]], coords: List[List[tuple[int, int]]]) -> List[tuple[int,int]]:
    output = []
    for y,row in enumerate(input):
        for x, cell in enumerate(row):
            if cell == '#':
                output.append(coords[y][x])
    return output

P = TypeVar('P')
def get_pairs(input: List[P]) -> List[tuple[P,P]]:
    output = []
    for i in range(len(input) - 1):
        first = input[i]
        for second in input[i+1:]:
            output.append((first,second))
    return output

def calc_coords(input: List[List[str]]) -> List[List[tuple[int, int]]]:
    #rows offsets
    ys = [0]
    offset = 0
    for row in input[:-1]:
        offset = offset + 1 if '#' in row else offset + 1000000
        ys.append(offset)
    xs = [0]
    offset = 0
    for i in range(len(input[0]) - 1):
        col = [x[i] for x in input]
        offset = offset + 1 if '#' in col else offset + 1000000
        xs.append(offset)
    coords = [[(y,x) for x in xs] for y in ys]
    return coords

input = parse_input('input.txt')
coords = calc_coords(input)
galaxies = get_galaxies_list(input, coords)
pairs = get_pairs(galaxies)
distances = [abs(x[0] - y[0]) + abs(x[1] - y[1]) for x,y in pairs]
print(sum(distances))