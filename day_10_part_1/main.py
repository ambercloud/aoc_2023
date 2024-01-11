from typing import List, Dict

class Pipe:
    def __init__(self, x: int, y:int, symbol: str) -> None:
        self.x = x
        self.y = y
        self.value = symbol
        ends = ''
        match self.value:
            case 'F':
                ends = 'se'
            case 'L':
                ends = 'ne'
            case '7':
                ends = 'sw'
            case 'J':
                ends = 'nw'
            case '|':
                ends = 'ns'
            case '-':
                ends = 'we'
            case 'S':
                ends = 'nswe'
            case '.':
                ends = ''
            case '_':
                raise Exception('Symbol not defined')
        self.ends: Dict[str, Pipe | None] = {d: None for d in ends}
    def __repr__(self) -> str:
        return f"Pipe({self.x},{self.y})"

class Map:
    #map filled with pipes, pipes connect into network
    _matches = {'n':'s', 'w':'e', 's':'n', 'e':'w'}
    def __init__(self, data: List[List[str]]) -> None:
        self.pipes = [[Pipe(x, y, symbol) for x, symbol in enumerate(row)] for y, row in enumerate(data)]
        self.xmax = len(self.pipes[0]) - 1
        self.ymax = len(self.pipes) - 1
    def __repr__(self) -> str:
        return f"Map({self.xmax}x{self.ymax})"
    def find_beast(self) -> tuple[int, int]:
        for row, line in enumerate(self.pipes):
            for col, pipe in enumerate(line):
                if pipe.value == 'S':
                    return (col, row)
    def __get_adjacent(self, coords: tuple[int, int], direction: str) -> tuple[int, int] | None:
        x, y = coords
        match direction:
            case 'w':
                return (x - 1, y) if x > 0 else None
            case 'e':
                return (x + 1, y) if x < self.xmax else None
            case 'n':
                return (x, y - 1) if y > 0 else None
            case 's':
                return (x, y + 1) if y < self.ymax else None    
    def pipe_by_coords(self, coords: tuple[int,int]) -> Pipe:
        x, y = coords
        return self.pipes[y][x]
    def connect_pipes(self):
        for row in self.pipes:
            for pipe in row:
                for direction in pipe.ends:
                    adjxy = self.__get_adjacent((pipe.x, pipe.y), direction)
                    if adjxy:
                        adj = self.pipe_by_coords(adjxy)
                        if Map._matches[direction] in adj.ends:
                            pipe.ends[direction] = adj


def parse_input(filename: str) -> List[List[str]]:
    f = open(filename, 'r', encoding='utf-8')
    data = []
    for line in f:
        data.append(list(line.removesuffix('\n')))
    return data

def find_loop(beastxy: tuple[int, int], pipes: Map) -> List[Pipe]:
    beast = pipes.pipe_by_coords(beastxy)
    loop = []
    loop.append(beast)
    curr_pipe = beast
    prev_pipe = beast
    next_pipe = next(pipe for dir, pipe in curr_pipe.ends.items() if pipe and pipe != prev_pipe)
    while next_pipe != beast:
        loop.append(next_pipe)
        prev_pipe = curr_pipe
        curr_pipe = next_pipe
        next_pipe = next(pipe for dir, pipe in curr_pipe.ends.items() if pipe and pipe != prev_pipe)
    return loop
    




field = Map(parse_input('input.txt'))
field.connect_pipes()
beastxy = field.find_beast()
loop = find_loop(beastxy, field)
steps = len(loop)//2
print(steps)