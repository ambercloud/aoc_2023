from typing import List, NamedTuple, Iterator, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import itertools
import heapq

class Coords(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}:{self.y})'

class Direction(Enum):
    n = 1
    e = 2
    s = 3
    w = 4

class Edge(NamedTuple):
    origin: Coords
    destination: Coords
    distance: int
    direction: Direction

    def __repr__(self) -> str:
        return f'[{self.origin}, {self.destination}, {self.distance}, {self.direction.name}]'

class PriorityQueue:
    def __init__(self) -> None:
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

@dataclass
class Node:
    xy: Coords
    ins: list[Edge]
    outs: list[Edge]

    def __repr__(self) -> str:
        return f'({self.xy.x}:{self.xy.y})'

def parse_input(filename: str) -> List[List[int]]:
    f = open(filename, mode='r', encoding='utf-8')
    output = []
    for line in f:
        output.append([int(char) for char in line.removesuffix('\n')])
    return output

def build_graph(costs: List[List[int]]) -> dict[Coords, Node]:
    xmax = len(costs[0])
    ymax = len(costs)
    def neighbours(coords: Coords) -> Iterator[tuple[Coords, Direction]]:
        ox, oy = coords
        around = (ox, oy - 1, Direction.n), (ox + 1, oy, Direction.e), (ox, oy + 1, Direction.s), (ox - 1, oy, Direction.w)
        for x, y, dir in around:
            if x in range(xmax) and y in range(ymax):
                yield (Coords(x, y), dir)

    nodes: dict[Coords, Node] = {}

    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            xy = Coords(x, y)
            nodes[xy] = Node(xy, [], [])

    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            xy = Coords(x, y)
            this_node = nodes[xy]
            for nxy, dir in neighbours(xy):
                neighbour_node = nodes[nxy]
                edge = Edge(xy, nxy, costs[nxy.y][nxy.x], dir)
                this_node.outs.append(edge)
                neighbour_node.ins.append(edge)

    return nodes

def calc_min_distance(nodes: dict[Coords, Node], origin: Coords) -> dict[Coords, int|float]:
    INF = float('inf')
    visited: set[Coords] = set()
    min_distances: dict[Coords, int|float] = defaultdict(lambda: INF)
    prev_edge: dict[Coords, Edge] = {}
    current_heat: dict[Coords, int] = {}
    origin_node = nodes[origin]
    min_distances[origin] = 0
    queue = PriorityQueue()
    queue.add_task(origin, min_distances[origin])
    while True:
        try:
            current_xy: Coords = queue.pop_task()
        except KeyError:
            break
        current: Node = nodes[current_xy]
        visited.add(current_xy)
        to_check = (edge for edge in current.outs if not edge.destination in visited)
        for edge in to_check:
            dest = nodes[edge.destination]
            current_distance = min_distances[dest.xy]
            new_distance = min_distances[current.xy] + edge.distance
            if new_distance < current_distance:
                min_distances[dest.xy] = new_distance
            queue.add_task(dest.xy, min_distances[dest.xy])
    return min_distances

def find_shortest_path(nodes: dict[Coords, Node], start: Coords, finish: Coords) -> List[Edge]:
    min_distances = calc_min_distance(nodes, start)
    curr = finish
    path = []
    while not curr == start:
        previous = (edge for edge in nodes[curr].ins)
        best_previous = min(previous, key = lambda e: min_distances[e.origin])
        path.append(best_previous)
        curr = best_previous.origin
    path = [x for x in reversed(path)]
    return path


costs = parse_input('input.txt')
nodes = build_graph(costs)
start = (0,0)
finish = (len(costs[0]) - 1, len(costs) - 1)
path = find_shortest_path(nodes, start, finish)
print([start] + [e.destination for e in path])
pass