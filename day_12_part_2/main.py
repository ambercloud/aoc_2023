from typing import List, Iterator
import re

class Record:
    def __init__(self, value: str) -> None:
        self.value = value
        self.bad = int(value.replace('.', '0').replace('?', '0').replace('#', '1'), 2)
        self.good = int(value.replace('.', '1').replace('?', '0').replace('#', '0'), 2)
        self.unknown = int(value.replace('.', '0').replace('?', '1').replace('#', '0'), 2)

def parse_input(filename: str) -> List[tuple[str,List[int]]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        springs, _, repdata = line.partition(' ')
        #springs = springs + ('?'+springs)*4
        repdata = repdata.removesuffix('\n')
        #repdata = repdata + (',' + repdata) * 4
        repdata = [int(x) for x in repdata.split(',')]
        output.append((Record(springs), repdata))
    return output


def count_placements(rec: Record, chunks: List[int]) -> List[str]:
    


input = parse_input('input.txt')
