from typing import List
from enum import Enum

def parse_input(filename: str) -> List[List[List[str]]]:
    f = open(filename, 'r', encoding='utf-8')
    matrixes = [[]]
    for line in f:
        if not line == '\n':
            matrixes[-1].append([char for char in line.removesuffix('\n')])
        else:
            matrixes.append([])
    return matrixes

def check_mirrored_list(input: List[str], split_point: int) -> List[bool]:
    reflected_width = min(split_point, len(input) - split_point)
    #create empty array with match results
    result = [None] * len(input)
    #match every list cell respectively to suggested line of reflection (split_point)
    for i in range(reflected_width):
        left_index = split_point - i - 1
        right_index = split_point + i
        is_match = (input[left_index] == input[right_index])
        result[left_index] = result[right_index] = is_match
    return result

Direction = Enum('Direction', ['h', 'v'])

def check_mirrored_matrix(input: List[List[str]], split_point: int, direction: str) -> List[List[bool]]:
    output = [[None for x in line] for line in input]
    if direction == 'v':
        for i in range(len(input)):
            matches = check_mirrored_list(input[i], split_point)
            for j in range(len(output[0])):
                output[i][j] = matches[j]
        return output
    if direction == 'h':
        for i in range(len(input[0])):
            matches = check_mirrored_list([line[i] for line in input], split_point)
            for j in range(len(output)):
                output[j][i] = matches[j]
        return output
    raise Exception('Direction not recognized')

def find_smudged_reflection_h(input: List[List[str]]) -> int|None:
    for i in range(1, len(input)):
        matches = check_mirrored_matrix(input, i, 'h')
        c = sum([line.count(False) for line in matches])
        if c == 2:
            return i
    pass
        
def find_smudged_reflection_v(input: List[List[str]]) -> int|None:
    for i in range(1, len(input[0])):
        matches = check_mirrored_matrix(input, i, 'v')
        c = sum([line.count(False) for line in matches])
        if c == 2:
            return i
    pass

matrixes = parse_input('input.txt')

reflections_v = []
reflections_h = []

for i, m in enumerate(matrixes):
    h = find_smudged_reflection_h(m)
    v = find_smudged_reflection_v(m)
    if h is None and v is None:
        raise Exception('smudge not found')
    if not h is None and not v is None:
        raise Exception('Sumdge is both in horisontal and vertical')
    if not h is None:
        reflections_h.append(h)
    if not v is None:
        reflections_v.append(v)
result = sum(reflections_v) + 100 * sum(reflections_h)
print(result)