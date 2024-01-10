from typing import List

class Pipe:
    def __init__(self, x, y, symbol: str) -> None:
        self.x = x
        self.y = y
        self.value = symbol
        match symbol:
            case 'F':
                self.openings = set('se')
            case 'L':
                self.openings = set('ne')
            case '7':
                self.openings = set('sw')
            case 'J':
                self.openings = set('nw')
            case '|':
                self.openings = set('ns')
            case '-':
                self.openings = set('we')
            case 'S':
                self.openings = set('nswe')
            case '.':
                self.openings = set()
            case '_':
                raise Exception('Symbol not defined')
    def __contains__(self, direction: str) -> bool:
        return direction in self.openings

class Map:
    def __init__(self, data: List[List[str]]) -> None:
        self.data = [list(x) for x in data]
        self.xmax = len(self.data[0])
        self.ymax = len(self.data)
    def find_beast(self) -> tuple[int, int]:
        for y, line in enumerate(self.data):
            if 'S' in line:
                return (line.index('S'), y)
    def get_adjacent(self, coords, direction) -> Pipe | None:
        x, y = coords
        match direction:
            case 'w':
                return x-1 if x > 0 else None
            case 'e':
                return s(x + 1, y) if x < 0 else None
            case 'w':
                return (x - 1, y) if x > 0 else None
            case 'w':
                return (x - 1, y) if x > 0 else None
    def __get_connected(self, coords: tuple[int, int]) -> List[Pipe]:
        origin = self[coords]



def parse_input(filename: str) -> List[List[str]]:
    f = open(filename, 'r', encoding='utf-8')
    data = []
    for line in f:
        data.append(list(line.removesuffix('\n')))
    return data

field = parse_input('input.txt')
print(field.find_beast())