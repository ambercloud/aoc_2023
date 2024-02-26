from typing import List

def parse_input(filename) -> List[str]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        output.extend(line.removesuffix('\n').split(','))
    return output

def char_to_int(ch: str) -> int:
    return ch.encode(encoding='ascii')[0]

def calc_hash(input: str) -> int:
    hash = 0
    for ch in input:
        hash = hash + char_to_int(ch)
        hash = hash * 17
        hash = hash % 256
    return hash

input = parse_input('input.txt')
hashes = [calc_hash(s) for s in input]
print(sum(hashes))