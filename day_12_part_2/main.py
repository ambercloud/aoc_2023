from typing import List, Iterator, Generator
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
        springs = springs + ('?'+springs)*4
        repdata = repdata.removesuffix('\n')
        repdata = repdata + (',' + repdata) * 4
        repdata = [int(x) for x in repdata.split(',')]
        output.append((Record(springs), repdata))
    return output

def count_placements(rec: Record, chunks: List[int], is_first: bool = True) -> int:
    #count possible placements for first chunk, then repeat recursively for each placement
    count = 0
    min_left_shift = 0 if len(chunks) == 1 else sum(chunks[1:]) + (len(chunks) - 1)
    #if it's not the first chunk we must leave a gap after previous chunk
    full_width = len(rec.value)
    chunk_width = chunks[0]
    max_left_shift = full_width - chunk_width if is_first else full_width - chunk_width - 1
    for left_shift in range(max_left_shift, -1 + min_left_shift, -1):
        badmap = (2**chunk_width - 1) << left_shift
        is_gap_available = (rec.bad >> (left_shift + chunk_width)) == 0
        if not is_gap_available:
            break
        is_bad_match = badmap & (rec.bad | rec.unknown) == badmap
        if is_bad_match:
            if len(chunks) > 1:
                count += count_placements(Record(rec.value[-left_shift:]), chunks[1:], False)
            else:
                #if it's the last chunk - check if there is clear gap trailing without uncounted '#'
                is_empty_trail = rec.bad & (2**left_shift - 1) == 0
                if is_empty_trail:
                    count += 1
    return count

def print_placements(rec: Record, chunks: List[int], is_first: bool = True) -> List[str]:
    #count possible placements for first chunk, then repeat recursively for each placement
    output = []
    pattern = rec.value
    min_left_shift = 0 if len(chunks) == 1 else sum(chunks[1:]) + (len(chunks) - 1)
    #if it's not the first chunk we must leave a gap after previous chunk
    full_width = len(rec.value)
    chunk_width = chunks[0]
    max_left_shift = full_width - chunk_width if is_first else full_width - chunk_width - 1
    for left_shift in range(max_left_shift, -1 + min_left_shift, -1):
        badmap = (2**chunk_width - 1) << left_shift
        badmap_str = bin(badmap).removeprefix('0b').rjust(full_width, '0')
        is_gap_available = (rec.bad >> (left_shift + chunk_width)) == 0
        if not is_gap_available:
            break
        is_bad_match = badmap & (rec.bad | rec.unknown) == badmap
        if is_bad_match:
            if len(chunks) > 1:
                children = print_placements(Record(rec.value[-left_shift:]), chunks[1:], False)
                header = badmap_str[0:-left_shift]
                output.extend([header + child for child in children])
            else:
                #if it's the last chunk - check if there is clear gap trailing without uncounted '#'
                is_empty_trail = rec.bad & (2**left_shift - 1) == 0
                if is_empty_trail:
                    output.append(badmap_str)
    return output


input = parse_input('input.txt')
counts = []
for x,y in input:
    c = count_placements(x,y)
    print(c)
    counts.append(c)
print(sum(counts))