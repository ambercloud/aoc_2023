from __future__ import annotations
from typing import List
from functools import reduce


class Combination(str):

    __order = '23456789TJQKA'
    __types = [(1, 1, 1, 1, 1), (2, 1, 1, 1), (2, 2, 1), (3, 1, 1), (3, 2), (4, 1), (5, )]

    def __init__(self, value: str) -> None:
        super().__init__()
        counts = dict.fromkeys(value, 0)
        for card in value:
            counts[card] += 1
        counts = tuple(sorted(counts.values(), reverse=True))
        self.value = value
        self.type = Combination.__types.index(counts)
    def __repr__(self) -> str:
        return str((super().__repr__(), self.type))
    def __lt__(self, other: Combination) -> bool:
        if self.type == other.type:
            for s, o in zip(self.value, other.value):
                if Combination.__order.index(s) == Combination.__order.index(o):
                    continue
                return True if Combination.__order.index(s) < Combination.__order.index(o) else False
            return False
        return True if self.type < other.type else False


def parse_input(filename: str) -> List[tuple[str, int]]:
    f = open('input.txt', 'r', encoding='utf-8')
    return  [(Combination(cards), int(bet)) for cards, bet in [line.split() for line in f]]

data = parse_input('input.txt')
sorted_data = (sorted(data))
print(reduce(lambda acc,val: acc + val[0] * val[1][1], enumerate(sorted_data, start = 1), 0))