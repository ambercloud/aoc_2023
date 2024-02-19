from typing import List

def parse_input(filename: str) -> List[tuple[str,List[int]]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        springs, _, repdata = line.partition(' ')
        springs = springs + ('?'+springs)*4
        repdata = repdata.removesuffix('\n')
        repdata = repdata + (',' + repdata) * 4
        repdata = [int(x) for x in repdata.split(',')]
        output.append((springs, repdata))
    return output

def count_placements(rec: str, chunks: List[int], cache: dict|None = None, is_first: bool = True) -> int:
    #count possible placements for first chunk, then repeat recursively for each placement
    if cache is None:
        cache = {}
    count = 0
    chunks_num = len(chunks)
    #if it's not the first chunk we must leave a gap after previous chunk
    full_width = len(rec)
    chunk_width = chunks[0]
    min_pos = 0 if is_first else 1
    max_pos = full_width - (sum(chunks[1:]) + (chunks_num - 1) + chunk_width)
    for pos in range(min_pos, max_pos + 1):
        is_gap_available = rec[:pos].find('#') == -1
        if not is_gap_available:
            break
        is_bad_match = rec[pos:pos+chunk_width].find('.') == -1
        if is_bad_match:
            if chunks_num > 1:
                key = (rec[pos+chunk_width:], str(chunks[1:]))
                if key in cache:
                    remainder = cache[key]
                else:
                    remainder = count_placements(rec[pos+chunk_width:], chunks[1:], cache, False)
                    cache[key] = remainder
                count += remainder
            else:
                #if it's the last chunk - check if there is clear gap trailing without uncounted '#'
                is_empty_trail = rec[pos+chunk_width:].find('#') == -1
                if is_empty_trail:
                    count += 1
    return count

input = parse_input('input.txt')
counts = []
for x,y in input:
    c = count_placements(x,y)
    print(c)
    counts.append(c)
print(sum(counts))
