from typing import List
from dataclasses import dataclass

class Record:
    def __init__(self, value: str, chunks: List[int]) -> None:
        self.pattern = value
        self.chunks = chunks[:]
    
    def __repr__(self) -> str:
        return f"Record({self.pattern}, {self.chunks})"
    
@dataclass
class ChunkPlacements:
    placements: List[str]
    chunk: str

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

def is_char_matches(value: str, pattern: str) -> bool:
    #first argument is the tested value, second - is the value to be matched against
    match value:
        case '?':
            return True
        case '#':
            return False if pattern == '.' else True
        case '.':
            return False if pattern == '#' else True
        case _:
            raise Exception('Unrecognised match value')

def get_matching_placements(pattern: str, chunk: str) -> List[str]:
    #takes pattern string and a chunk string, returns every possible placement matching the string
    patternlen = len(pattern)
    chunklen = len(chunk)
    output = []
    for i in range(patternlen - chunklen + 1):
        p = pattern[i:i+chunklen]
        if all([is_char_matches(v,p) for v,p in zip(chunk, p)]):
            fullstring = '?'*i + chunk + '?'*(patternlen - chunklen - i)
            output.append(fullstring)
    return (output)

def get_valid_placements(rec: Record) -> List[List[str]]:
    #return list of possible placements for each chunk matching the pattern and leaving place for other chunks
    output: List[List[str]] = []
    #first we get every possible placement for each chunk independedly
    for i in range(len(rec.chunks)):
        #first chunk is just ###, every chunk after is .### because chunks must be separated by at least one .
        chunk = '#'*rec.chunks[i] if i == 0 else '.' + '#'*rec.chunks[i]
        output.append(get_matching_placements(rec.pattern, chunk))
    #next we set limits on each chunk leftmost and rightmost boundary since we always want to leave space for other chunks
    left_boundary = 0
    for i in range(len(rec.chunks)):
        #first chunk is just ###, every chunk after is .### because chunks must be separated by at least one .
        chunk = '#'*rec.chunks[i] if i == 0 else '.' + '#'*rec.chunks[i]
        #remove every placement violating left boundary
        output[i] = [x for x in output[i] if x.find(chunk) >= left_boundary]
        #update left boundary for next chunk based on leftmost position of the current chunk
        left_boundary = output[i][0].find(chunk) + len(chunk)
    #same for the right boundary but we're moving backwards
    right_boundary = len(rec.pattern)
    for i in range(len(rec.chunks) - 1, -1, -1):
        chunk = '#'*rec.chunks[i] if i == 0 else '.' + '#'*rec.chunks[i]
        output[i] = [x for x in output[i] if x.rfind(chunk) + len(chunk) <= right_boundary]
        right_boundary = output[i][-1].rfind(chunk)
    return output

def trim_from_left(placements: List[List[str]], cutoff_index) -> List[List[str]]:
    #for each chunk remove placements that cross certain boundary
    output = [[placement for placement in chunklist if ] for chunklist in placements]

def count_placements(rec: Record) -> int:
    placements = get_valid_placements(rec)
    left_boundary = placements[0][-1].find('#'*rec.chunks[0]) + rec.chunks[0] - 1
    count = len(placements[0])
    for i in range(1, len(placements)):
        #count placements independent from previous chunk
        chunk = '.'+'#'*rec.chunks[i]
        indep = len([x for x in placements[i] if x.find(chunk) > left_boundary])
        dep = len(placements[i]) - indep
        dep = sum([x for x in range(dep+1)])
        #update count
        count = count*indep + dep
        left_boundary = placements[i][-1].find(chunk) + rec.chunks[i] - 1
    return count


input = parse_input('input.txt')
counts = []
for x in input:
    count = count_placements(x)
    counts.append(count)
print(sum(counts))
k = open('incorrect.txt', 'w', encoding='utf-8')
for x in counts:
    k.write(f'{x}\n')
k.write(f'{sum(counts)}\n')
