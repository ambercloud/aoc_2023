from typing import List

class Pattern:
    def __init__(self, input: str) -> None:
        self.good = sum(1 << i if x == '.' or x == '?' else 0 for i, x in enumerate(input))
        self.bad = sum(1 << i if x == '#' or x == '?' else 0 for i, x in enumerate(input))

class Record:
    def __init__(self, value: str, chunks: List[int]) -> None:
        self.value = value
        self.chunks = chunks[:]
        self.pattern = Pattern(value)
    
    def __repr__(self) -> str:
        return f"Record({self.pattern}, {self.chunks})"

def parse_input(filename: str) -> List[tuple[str,List[int]]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        springs, _, repdata = line.partition(' ')
        #springs = springs + ('?'+springs)*4
        repdata = repdata.removesuffix('\n')
        #repdata = repdata + (',' + repdata) * 4
        repdata = [int(x) for x in repdata.split(',')]
        output.append(Record(springs, repdata))
    return output

def get_chunks_placements(rec: Record) -> List[List[int]]:
    matching = []
    for i in range(len(rec.chunks)):
        chunk = '1'*rec.chunks[i] if i == 0 else '0'+'1'*rec.chunks[i]
        chunk_len = len(chunk)
        pattern_len = len(rec.pattern)
        placements = [int('0b' + "".join(reversed('0'*i + chunk + '0'*(pattern_len - i - chunk_len)))) << i for i in range(pattern_len - chunk_len + 1)]
        #matching placements are those that are not intersect with any '.'
        valid_placements = [x for x in placements if x == x & ~rec.good]
        matching.append(valid_placements)

    '''print(f'{rec.pattern}, {rec.chunks}\n')
    for v in output:
        l = len(rec.pattern)
        print([f"{x:0{l}b}"[::-1] for x in v])'''
    
    return matching
    

input = parse_input('input.txt')
get_chunks_placements(input[4])
pass
