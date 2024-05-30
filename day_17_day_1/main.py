from __future__ import annotations
from typing import List, NamedTuple, Iterator
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

class Coords(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

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
        return f'Edge:{self.origin}, {self.destination}, {self.distance}, {self.direction}'

@dataclass
class Node:
    xy: Coords
    min_distance_from: dict[Coords, int] = field(default_factory=dict)

class EdgeCollection:
    def __init__(self) -> None:
        self._orig_dest: dict[tuple[Coords,Coords], Edge] = {}
        self._orig: defaultdict[Coords, List[Edge]] = defaultdict(list)
        self._dest: defaultdict[Coords, List[Edge]] = defaultdict(list)

    def add(self, edge: Edge) -> None:
        self._orig_dest[(edge.origin, edge.destination)] = edge
        self._orig[edge.origin].append(edge)
        self._dest[edge.destination].append(edge)

    def get_by_orig_dest(self, orig_dest: tuple[Coords, Coords]) -> Edge:
        return self._orig_dest[orig_dest]
    
    def get_by_orig(self, orig: Coords) -> List[Edge]:
        return self._orig[orig]
    
    def get_by_dest(self, dest: Coords) -> List[Edge]:
        return self._dest[dest]
    
    def delete(self, orig_dest: tuple[Coords, Coords]) -> None:
        if orig_dest in self._orig_dest:
            del self._orig_dest[orig_dest]

class Graph(NamedTuple):
    nodes: dict[Coords, Node]
    edges: EdgeCollection

def gen_neighbours(xo: int, yo: int, xrange: range, yrange: range) -> Iterator[tuple[int, int, Direction]]:
    dir = Direction
    around = ((xo, yo - 1, dir.n), (xo + 1, yo, dir.e), (xo, yo + 1, dir.s), (xo - 1, yo, dir.w))
    for x, y, d in around:
        if x in xrange and y in yrange:
            yield x, y, d

def parse_input(filename: str) -> List[List[Node]]:
    f = open(filename, 'r', encoding='utf-8')
    costs = []
    for y, line in enumerate(f):
        costs.append([int(x) for x in line.removesuffix('\n')])
    return costs

def build_graph(costs: List[List[int]]) -> Graph:
    #returns a tuple (nodes, edges)
    nodes: dict[Coords, Node] = {}
    for y, row in enumerate(costs):
        for x, origin_cost in enumerate(row):
            origin = Node((x, y))
            nodes[(x, y)] = origin

    xmax = len(costs[0])
    ymax = len(costs)

    edges = EdgeCollection()
    
    for y, row in enumerate(costs):
        for x, origin_cost in enumerate(row):
            origin = nodes[(x, y)]
            for xn, yn, direction in gen_neighbours(x, y, range(0, xmax), range(0, ymax)):
                destination = nodes[(xn, yn)]
                destination_cost = costs[yn][xn]
                #fill edges
                origin_to_destination = Edge(Coords(x,y), Coords(xn, yn), destination_cost, direction)
                edges.add(origin_to_destination)
    
    return Graph(nodes, edges)

def find_path(graph: Graph, start: Coords, end: Coords, max_straight: int) -> List[Edge]:
    nodes, edges = graph
    for i in range(len(nodes)):
        for edge in edges:
            if
    

costs = parse_input('input.txt')
graph = build_graph(costs)
start = (0,0)
finish = (len(costs[0]) - 1, len(costs) - 1)
max_straight = 4
shortest = find_path(graph, start, finish, max_straight)
pass