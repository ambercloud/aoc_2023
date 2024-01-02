from typing import List
from functools import reduce

def parse_input(filename: str) -> List[List[int]]:
    f = open(filename, 'r', encoding='utf-8')
    data = []
    for line in f:
        data.append([int(x) for x in line.split()])
    return data

def extrapolate(data: List[List[int]]) -> None:
    def build_diffs(diffs: List[List[int]]) -> None:
        if any(diffs[-1]):
            last = diffs[-1]
            next = [last[x] - last[x-1] for x in range(1, len(last))]
            diffs.append(next)
            build_diffs(diffs)
    for line in data:
        diffs = [line]
        build_diffs(diffs)
        diffs[-1].insert(0, 0)
        for i in range(len(diffs) - 1, 0, -1):
            upper = diffs[i-1][0] - diffs[i][0]
            diffs[i - 1].insert(0, upper)
        line.insert(0, diffs[0][0])

data = parse_input('input.txt')
extrapolate(data)
result = sum(x[0] for x in data)
print(result)