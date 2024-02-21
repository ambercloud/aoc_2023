from typing import List

def parse_input(filename: str) -> List[List[List[str]]]:
    f = open(filename, 'r', encoding='utf-8')
    matrixes = [[]]
    for line in f:
        if not line == '\n':
            matrixes[-1].append([char for char in line.removesuffix('\n')])
        else:
            matrixes.append([])
    return matrixes

def find_vertical_mirror(matrix: List[List[str]]) -> int|None:
    for i in range(1, len(matrix[0])):
        left = [line[:i] for line in matrix]
        right = [line[i:] for line in matrix]
        trimlen = min(len(left[0]), len(right[0]))
        left = [line[-trimlen:] for line in left]
        right = [line[:trimlen] for line in right]
        right = [[x for x in reversed(line)] for line in right]
        left = [''.join(line) for line in left]
        right = [''.join(line) for line in right]
        is_mirrored = all([(l == r) for l,r in zip(left, right)])
        if is_mirrored:
            return i
        else:
            continue
    
def find_horisontal_mirror(matrix: List[List[str]]) -> int|None:
    transposed = []
    for rownum in range(len(matrix[0])):
        transposed.append([line[rownum] for line in matrix])
    return find_vertical_mirror(transposed)

matrixes = parse_input('input.txt')
hormirs = []
vertmirs = []
for m in matrixes:
    vm = find_vertical_mirror(m)
    hm = find_horisontal_mirror(m)
    if not vm is None:
        vertmirs.append(vm)
    if not hm is None:
        hormirs.append(hm)
result = sum(vertmirs) + (100 * sum(hormirs))
print(result)

