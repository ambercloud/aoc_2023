from typing import List, Callable
from hashlib import sha256

def parse_input(filename: str) -> List[List[str]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        output.append([x for x in line.removesuffix('\n')])
    return output

def process_column[T](matrix: List[List[T]], col_i: int, callback: Callable[[List[T]], List[T]]) -> None:
    col = [row[col_i] for row in matrix]
    col = callback(col)
    for row, new_value in zip(matrix, col):
        row[col_i] = new_value

def shift_to_end[T](input: List[T], shiftable: T, stopper: T, empty: T) -> List[T]:
    #takes a list of items and shift all the shiftables to the right while they hit a stopper if there is an empty to the right available
    chunks = [[]]
    #split list in a chunks of shiftables+empties with stoppers in-betweens
    for x in input:
        if x == stopper:
            chunks.append([stopper])
            chunks.append([])
        else:
            chunks[-1].extend(x)
    output = []
    for x in chunks:
        if x:
            if x[0] == stopper:
                output.append(stopper)
            else:
                sc = x.count(shiftable)
                y = [empty]*(len(x) - sc) + [shiftable] * sc
                output.extend(y)
    return output

def shift_to_start[T](input: List[T], shiftable: T, stopper: T, empty: T) -> List[T]:
    r_input = [x for x in reversed(input)]
    r_output = shift_to_end(r_input, shiftable, stopper, empty)
    return [x for x in reversed(r_output)]

def tilt_to_north(matrix: List[List[str]]) -> None:
    shift = lambda x: shift_to_start(x, 'O', '#', '.')
    for i in range(len(matrix[0])):
        process_column(matrix, i, shift)

def tilt_to_west(matrix: List[List[str]]) -> None:
    for i in range(len(matrix)):
        matrix[i] = shift_to_start(matrix[i], 'O', '#', '.')

def tilt_to_south(matrix: List[List[str]]) -> None:
    shift = lambda x: shift_to_end(x, 'O', '#', '.')
    for i in range(len(matrix[0])):
        process_column(matrix, i, shift)

def tilt_to_east(matrix: List[List[str]]) -> None:
    for i in range(len(matrix)):
        matrix[i] = shift_to_end(matrix[i], 'O', '#', '.')

def calc_load(matrix: List[List[str]]) -> int:
    output = 0
    for i, row in enumerate(matrix):
        output += row.count('O') * (len(matrix) - i)
    return output

def rotate(matrix: List[List[str]], cyclenum) -> None:
    log = {}
    i = 0
    #detect repeating loop of cycles and skip loops until the end, then rotate only remainded number of cycles
    for i in range(cyclenum):
        key = sha256(str(matrix).encode()).hexdigest()
        if key in log:
            period = i - log[key]
            remainder = cyclenum - i
            remainder = remainder % period
            for j in range(remainder):
                tilt_to_north(boulders)
                tilt_to_west(boulders)
                tilt_to_south(boulders)
                tilt_to_east(boulders)
            return
        else:
            log[key] = i
            tilt_to_north(boulders)
            tilt_to_west(boulders)
            tilt_to_south(boulders)
            tilt_to_east(boulders)        

boulders = parse_input('input.txt')
rotate(boulders, 1000000000)
print(calc_load(boulders))