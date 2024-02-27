from dataclasses import dataclass
from typing import List
from copy import deepcopy

@dataclass
class Ray:
    x: int
    y: int
    x_delta: int
    y_delta: int
    def __hash__(self) -> int:
        return hash(f'{self.x},{self.y},{self.x_delta},{self.y_delta}')
    def __repr__(self) -> str:
        return (f'Ray({self.x},{self.y},{self.x_delta},{self.y_delta})')

class Field:
    @staticmethod
    def _pass(r: Ray) -> List[Ray]:
        r.x = r.x + r.x_delta
        r.y = r.y + r.y_delta
        return [r]
    
    @staticmethod
    def _turn_90(r: Ray) -> List[Ray]:
        r.x_delta, r.y_delta = -r.y_delta, -r.x_delta
        return Field._pass(r)
    
    @staticmethod
    def _turn_minus_90(r: Ray) -> List[Ray]:
        r.x_delta, r.y_delta = r.y_delta, r.x_delta
        return Field._pass(r)
    
    @staticmethod
    def _split(r: Ray) -> List[Ray]:
        r.x_delta, r.y_delta = r.y_delta, r.x_delta
        r2 = Ray(r.x, r.y, -r.x_delta, -r.y_delta)
        return Field._pass(r) + Field._pass(r2)
    
    @staticmethod
    def _v_split(r: Ray) -> List[Ray]:
        if r.x_delta:
            return Field._split(r)
        else:
            return Field._pass(r)
        
    @staticmethod
    def _h_split(r: Ray) -> List[Ray]:
        if r.y_delta:
            return Field._split(r)
        else:
            return Field._pass(r)

    def __init__(self, x: int, y: int, type: str) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.is_energized: bool = False
        self._ray_cache = set()
        match type:
            case '.':
                self._ray_handler = Field._pass
            case '-':
                self._ray_handler = Field._h_split
            case '|':
                self._ray_handler = Field._v_split
            case '/':
                self._ray_handler = Field._turn_90
            case '\\':
                self._ray_handler = Field._turn_minus_90

    def ray_handler(self, r: Ray) -> List[Ray]:
        #if a ray hits mirror second time from the same direction destroy it
        h = hash(r)
        if h in self._ray_cache:
            return []
        else:
            self._ray_cache.add(h)
        return self._ray_handler(r)

    def __repr__(self) -> str:
        return f"'{self.type}'"

def parse_input(filename: str) -> List[List[Field]]:
    output = []
    f = open(filename, 'r', encoding='utf-8')
    for y, line in enumerate(f):
        output.append([Field(x, y, s) for x,s in enumerate(line.removesuffix('\n'))])
    return output

def run_rays(rays: List[Ray], scene: List[List[Field]]) -> None:
    xmax = len(scene[0])
    ymax = len(scene)
    while rays:
        rays_new: List[Ray] = []
        for r in rays:
            current_field = scene[r.y][r.x]
            current_field.is_energized = True
            rays_new.extend(current_field.ray_handler(r))
        rays_new = [r for r in rays_new if r.x in range(xmax) and r.y in range(ymax)]
        rays = rays_new

def count_energized(r: Ray, s: List[List[Field]]):
    scene = deepcopy(s)
    r_id = str(r)
    rays = [r]
    run_rays(rays, scene)
    energized = [[x.is_energized for x in row] for row in scene]
    energized_count = sum([row.count(True) for row in energized])
    print(f'{r_id}, {energized_count}')
    return energized_count

scene = parse_input('input.txt')
rays = []
rays += [Ray(x, 0, 0, 1) for x in range(len(scene[0]))]
rays += [Ray(x, len(scene) - 1, 0, -1) for x in range(len(scene[0]))]
rays += [Ray(0, x, 1, 0) for x in range(len(scene))]
rays += [Ray(len(scene[0]) - 1, x, -1, 0) for x in range(len(scene))]
energized = [count_energized(r, scene) for r in rays]
print(max(energized))
pass