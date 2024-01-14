from typing import List, Iterator
import re

def parse_input(filename: str) -> List[tuple[str,List[int]]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        springs, _, repdata = line.partition(' ')
        #springs = springs + ('?'+springs)*4
        repdata = repdata.removesuffix('\n')
        #repdata = repdata + (',' + repdata) * 4
        repdata = [int(x) for x in repdata.split(',')]
        output.append((springs, repdata))
    return output

def find_gaps(springs: str, search_start = 0) -> List[tuple[int,int]]:
    #takes a string for springs condition and returns a list of (pos, length) for every contigious chunk of [#?]
    gaps = []
    start = next((x for x in range(search_start, len(springs)) if springs[x] == '#' or springs[x] == '?'), None)
    if start is not None:
        pos = springs.find('.', start)
        end = len(springs) if pos == -1 else pos
        gaps.append((start, end - start))
        gaps.extend(find_gaps(springs, end))
    return gaps
    

def get_first_chunk_placements(conditions: str, chunks: List[int]) -> int:
    gaps = []
    flag = False
    length = 0


    right_bound = min(\
            len(conditions) - (sum(chunks[1:]) + len(chunks[1:])),\
            len(conditions) if conditions.find('#') == -1 else (conditions.find('#') + chunks[0])\
        )
    re_string = '(?=([#?]{'+str(chunks[0])+'}))'
    matches = re.finditer(re_string, conditions[:right_bound])
    return [(x[1], x.pos) for x in matches]

input = parse_input('input.txt')
a,b = input[2]
print(a)
print(find_gaps(a))