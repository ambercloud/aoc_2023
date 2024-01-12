from typing import List,TypeVar

def parse_input(filename: str) -> List[List[str]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        output.append(list(line.removesuffix('\n')))
    return output

def expand_universe(input: List[List[str]]):
    output = []
    for row in input:
        output.append(row)
        #if row is empty - double it
        if not '#' in row:
            output.append(row)
    temp = output
    output = [[] for _ in temp]
    #copy matrix column by column
    for i in range(len(temp[0])):
        col = [row[i] for row in temp]
        for j in range(len(col)):
            output[j].append(col[j])
        #if the column is empty - double it
        if not '#' in col:
            for j in range(len(col)):
                output[j].append(col[j])
    return output

def write_debug(input: List[List[str]]):
    file = open('debug.txt', 'w', encoding='utf-8')
    for row in input:
        line = ''.join(row)+'\n'
        file.write(line)

def get_galaxies_list(input: List[List[str]]) -> List[tuple[int,int]]:
    output = []
    for y,row in enumerate(input):
        for x, cell in enumerate(row):
            if cell == '#':
                output.append((y,x))
    return output

P = TypeVar('P')
def get_pairs(input: List[P]) -> List[tuple[P,P]]:
    output = []
    for i in range(len(input) - 1):
        first = input[i]
        for second in input[i+1:]:
            output.append((first,second))
    return output


input = parse_input('input.txt')
universe = expand_universe(input)
galalist = get_galaxies_list(universe)
pairs = get_pairs(galalist)
distances = [abs(x[0] - y[0]) + abs(x[1] - y[1]) for x,y in pairs]
print(sum(distances))
#write_debug(universe)