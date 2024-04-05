from typing import List, NamedTuple, Iterator, Any
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

class Coords(NamedTuple):
    x: int
    y: int

class Direction(Enum):
    n = 1
    e = 2
    s = 3
    w = 4

class Edge(NamedTuple):
    origin: Coords
    destination: Coords
    distance: Coords
    direction: Direction

@dataclass
class Node:
    xy: Coords
    ins: list[Edge]
    outs: list[Edge]
    distance_from: defaultdict[Coords, int]

class EdgeCollection:
    def __init__(self) -> None:
        self._orig_dest: dict[tuple[Coords, Coords], Edge] = {}
        self._orig: defaultdict[Coords, set[Edge]] = defaultdict(set)
        self._dest: defaultdict[Coords, set[Edge]] = defaultdict(set)

    def add(self, edge: Edge) -> None:
        self._orig_dest[(edge.origin, edge.destination)] = edge
        self._orig[edge.origin].add(edge)
        self._dest[edge.destination].add(edge)

    def delete(self, orig: Coords, dest: Coords) -> None:
        edge = self._orig_dest[(orig, dest)]
        del self._orig_dest[(orig, dest)]
        self._orig[orig].remove(edge)
        self._dest[dest].remove(edge)

    def get_by_orig_dest(self, orig: Coords, dest: Coords) -> Edge:
        return self._orig_dest[(orig, dest)]

    def get_by_orig(self, orig: Coords) -> List[Edge]:
        return [x for x in self._orig[orig]]

    def get_by_dest(self, dest: Coords) -> List[Edge]:
        return [x for x in self._dest[dest]]

def parse_input(filename: str) -> List[List[int]]:
    f = open(filename, mode='r', encoding='utf-8')
    output = []
    for line in f:
        output.append([int(char) for char in line.removesuffix('\n')])
    return output

def build_graph(costs: List[List[int]]) -> tuple[dict[Coords, Node], dict[tuple[Coords, Coords], Edge]]:
    xmax = len(costs[0])
    ymax = len(costs)
    def neighbours(coords: Coords) -> Iterator[tuple[Coords, Direction]]:
        ox, oy = coords
        around = (ox, oy - 1, Direction.n), (ox + 1, oy, Direction.e), (ox, oy + 1, Direction.s), (ox - 1, oy, Direction.w)
        for x, y, dir in around:
            if x in range(xmax) and y in range(ymax):
                yield (Coords(x, y), dir)

    nodes: dict[Coords, Node] = {}
    edges = EdgeCollection()

    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            xy = Coords(x, y)
            nodes[xy] = Node(xy, [], [], defaultdict(lambda : float('inf')))
            for nxy, dir in neighbours(xy):
                edge = Edge(xy, nxy, costs[nxy.y][nxy.x], dir)
                edges.add(edge)

    return nodes, edges

def find_optimal_path(nodes: dict[Coords, Node], edges: EdgeCollection, start: Coords, finish: Coords) -> List[Edge]:
    #calc min distances first, then restore the path
    distances: dict[Coords, List[int]] = {}
    previous: dict[Coords, List[List[Edge]]] = {}
    for node in nodes.values():
        distances[node.xy] = [float('inf')] * (len(nodes) - 1)
        previous[node.xy] = [[]] * (len(nodes) - 1)
    distances[start][0] = 0
    for i in range(1, len(nodes) - 1):
        for edge in edges._orig_dest.values():
            if distances[edge.destination][i] < distances[edge.origin][i - 1] + edge.distance:
                continue
            elif distances[edge.destination][i] > distances[edge.origin][i - 1] + edge.distance:
                distances[edge.destination][i] = distances[edge.origin][i - 1] + edge.distance
                previous[edge.destination][i] = [edge]
            elif distances[edge.destination][i] == distances[edge.origin][i - 1] + edge.distance:
                previous[edge.destination][i].append(edge)
            else:
                raise Exception('Something wrong')
    #restore path
    steps_num, min_dist = min(enumerate(distances[finish]), key = lambda x: x[1])
    path: List[Edge] = []
    current = finish
    for i in range(steps_num, 0, -1):
        edge = previous[current][i][0]
        path.append(edge)
        current = edge.origin
    path = [x for x in reversed(path)]
    return path



costs = parse_input('input.txt')
nodes, edges = build_graph(costs)
start = (0,0)
finish = (len(costs[0]) - 1, len(costs) - 1)
path = find_optimal_path(nodes, edges, start, finish)
pass