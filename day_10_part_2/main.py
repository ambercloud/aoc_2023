from typing import List, Dict

class Pipe:
    def __init__(self, x: int, y:int, symbol: str) -> None:
        self.x = x
        self.y = y
        self.value = symbol
        self.vdir = 0
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

def find_loop(beastxy: tuple[int, int], field: Map) -> List[Pipe]:
    beast = field.pipe_by_coords(beastxy)
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
    
def find_inner_cells(loop: List[Pipe], field: Map) -> List[Pipe]:
    #use Sunday's algorithm to find cells inside the loop
    #go through the loop marking vertical direction we're going in
    #iterate through every pipe but the first and the last, last one we compare manually to avoid out of bounds situation
    for i in range(1, len(loop) - 2):
        #(0,0) point is top left.
        #vdir <0 means we go up, vdir>0 means we go down. 0 is horizontal
        loop[i].vdir = loop[i+1].y - loop[i-1].y
    loop[-1].vdir = loop[0].y - loop[-2].y
    loop[0].vdir = loop[1].y - loop[-1].y
    #finding top, bottom, left and right boundaries of the loop and ignore all the cells
    #outside the range to limit number of cells checked
    ymin = min([pipe.y for pipe in loop])
    ymax = max([pipe.y for pipe in loop])
    xmin = min([pipe.x for pipe in loop])
    xmax = max([pipe.x for pipe in loop])
    #find all the cells falling into the boundaries and not belonging to the loop itself
    #(we need only those inside the loop, loop is the border)
    candidates: List[Pipe] = []
    for row in field.pipes:
        candidates.extend([pipe for pipe in row if pipe.y >= ymin and pipe.y <= ymax and pipe.x >= xmin and pipe.x <= xmax and not pipe in loop])
    #for each candidate cast a ray to the right counting winding number
    inners: List[Pipe] = []
    for cand in candidates:
        wnum = 0
        if cand.x == field.xmax:
            #we're at the right border of the field, there's nowhere to cast the ray
            continue
        ray = field.pipes[cand.y][cand.x + 1:]
        for cell in ray:
            wnum += cell.vdir
        #if wnum is not zero the cell is inside the loop
        if wnum:
            inners.append(cand)
    return inners

def write_debug(loop: List[Pipe], inners: List[Pipe], field: Map):
    dbg = open('debug.txt', 'w', encoding='utf-8')
    for row in field.pipes:
        line = ""
        for pipe in row:
            m = 0
            m = m + 0b01 if pipe in loop else m
            m = m + 0b10 if pipe in inners else m
            match m:
                case 0b00:
                    line += '.'
                case 0b01:
                    if pipe.vdir < 0:
                        line += '↑'
                    elif pipe.vdir > 0:
                        line += '↓'
                    else:
                        line += '-'
                case 0b10:
                    line += 'x'
                case 0b11:
                    line += '*'
                case _:
                    raise Exception('Huh?')
        line += '\n'
        dbg.write(line)
            
field = Map(parse_input('input.txt'))
field.connect_pipes()
beastxy = field.find_beast()
loop = find_loop(beastxy, field)
inners = find_inner_cells(loop, field)
#write_debug(loop, inners, field)

print(len(inners))