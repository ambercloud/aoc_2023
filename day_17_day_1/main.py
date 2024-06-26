from typing import List, NamedTuple, Iterator, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import itertools
import heapq

#dropping for now

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

def calc_min_distance(nodes: dict[Coords, Node], start: Coords) -> tuple[dict[Coords, int|float], dict[Coords, Edge]]:
    INF = float('inf')
    visited: set[Coords] = set()
    min_distances: dict[Coords, int|float] = defaultdict(lambda: INF)
    prev_edge: dict[Coords, Edge] = {}
    min_distances[start] = 0
    prev_edge[start] = Edge(start, start, 0, 0)
    current = start
    queue = PriorityQueue()
    queue.add_task(current, min_distances[current])
    while True:
        try:
            current_xy: Coords = queue.pop_task()
        except KeyError:
            break
        current: Node = nodes[current_xy]
        visited.add(current_xy)
        to_check = [edge for edge in current.outs if not edge.destination in visited]
        to_check = [edge for edge in sorted(to_check, key = lambda e: min_distances[e.destination])]
        for edge in to_check:
            origin = current_xy
            destination = edge.destination
            current_distance = min_distances[destination]
            new_distance = min_distances[origin] + edge.distance
            if new_distance < current_distance:
                min_distances[destination] = new_distance
                prev_edge[destination] = edge
            queue.add_task(destination, min_distances[destination])
    return min_distances, prev_edge

def find_shortest_path(nodes: dict[Coords, Node], start: Coords, finish: Coords) -> tuple[int, List[Edge]]:
    min_distances, previous_edge = calc_min_distance(nodes, start)
    curr = finish
    path = []
    while not curr == start:
        previous = previous_edge[curr]
        path.append(previous)
        curr = previous.origin
    path = [x for x in reversed(path)]
    return min_distances[finish], path

def find_optimal_path(nodes: dict[Coords, Node], start: Coords, finish: Coords, max_straight = 3) -> List[Edge]:
    def find_straight_chunk(path: List[Edge]) -> int:        
        for i in range(0, len(path) - too_straight + 1):
            chunk = path[i:i + too_straight]
            if all(edge.direction == chunk[0].direction for edge in chunk):
                return i
        return -1

    too_straight = max_straight + 1

    optimal_path = []
    total_distance, path = find_shortest_path(nodes, start, finish)
    while True:
        #find start of a straight chunk
        straight_start = find_straight_chunk(path)
        if straight_start == -1:
            optimal_path += path
            break
        #put everythink before it into optimal path, rest in new path
        optimal_path += path[:straight_start]
        path = path[straight_start:]
        #remove an edge in a straight chunk, find new shortest path, save it, restore the edge
        #try it for every edge in straight chunk, then save shortest path as new path
        path_candidates: List[tuple[int, list[Edge]]] = []
        for i in range(too_straight):
            edge = path[i]
            node = nodes[edge.origin]
            node.outs.remove(edge)
            path_candidates.append(find_shortest_path(nodes, path[0].origin, finish))
            node.outs.append(edge)
        total_distance, path = min(path_candidates, key = lambda dist_path: dist_path[0])
    return optimal_path

costs = parse_input('test.txt')
nodes = build_graph(costs)
start = (0,0)
finish = (len(costs[0]) - 1, len(costs) - 1)
'''distance, path = find_shortest_path(nodes, start, finish)
print(path)
print(distance)'''
path = find_optimal_path(nodes, start, finish)
print(path)
print(sum([edge.distance for edge in path]))
pass