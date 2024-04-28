from __future__ import annotations
from typing import List, NamedTuple, Iterator
from enum import Enum
from collections import deque, defaultdict
from functools import cache


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
    distance: int
    direction: Direction

def parse_input(filename: str) -> List[List[int]]:
    f = open(filename, mode='r', encoding='utf-8')
    output = []
    for line in f:
        output.append([int(char) for char in line.removesuffix('\n')])
    return output

def build_graph(costs: List[List[int]]) -> tuple[List[Coords], List[Edge]]:
    xmax = len(costs[0])
    ymax = len(costs)
    def neighbours(coords: Coords) -> Iterator[tuple[Coords, Direction]]:
        ox, oy = coords
        around = (ox, oy - 1, Direction.n), (ox + 1, oy, Direction.e), (ox, oy + 1, Direction.s), (ox - 1, oy, Direction.w)
        for x, y, dir in around:
            if x in range(xmax) and y in range(ymax):
                yield (Coords(x, y), dir)

    nodes: List[Coords] = []
    edges: List[Edge] = []

    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            xy = Coords(x, y)
            nodes.append(xy)
            for nxy, dir in neighbours(xy):
                edge = Edge(xy, nxy, costs[nxy.y][nxy.x], dir)
                edges.append(edge)

    return nodes, edges

def find_shortest_distance(nodes: List[Coords], edges: List[Edge], start: Coords, finish: Coords) -> List[List[Edge]]:
    #calc min distances first, then restore the path of minimal distance (or multiple paths if there are more than one)
    #for a path of every length(in number of edges it consists of) we calculate minimal distance we can reach every node and last edge in the path (or multiple edges)
    #obviously not every node is reachable in arbitrary amount of steps
    max_straight = 4

    node_inputs: dict[Coords, List[Edge]] = defaultdict(list)
    for edge in edges:
        node_inputs[edge.destination].append(edge)

    INF = float('inf')
    previous: dict[Coords, int|float] = defaultdict(lambda: INF)
    pre_previous: dict[Coords, int|float] = defaultdict(lambda: INF)
    shortest: dict[Coords, int|float] = defaultdict(lambda: INF)
    backlog: deque[dict[Coords, List[Coords]]] = deque([], maxlen=max_straight)
    previous[start] = 0

    def backtrack(node: Coords, depth: int, current_index = -1) -> List[Coords]:
        #return list of predecessors of given level of recursion
        prevs = backlog[current_index][node]
        if depth + current_index == 0:
            return prevs
        else:
            return [xy for elem in map(lambda n: backtrack(n, depth, current_index - 1), prevs) for xy in elem]

    @cache
    def is_straight(a: Coords, b: Coords, max_straight = max_straight) -> bool:
        return ((abs(a.x - b.x) == max_straight + 1) or (abs(a.y - b.y) == max_straight + 1))

    def is_valid(edge: Edge, max_straight = max_straight) -> bool:
        #check for 180-turn
        if len(backlog) < 1:
            return True
        test = backtrack(edge.origin, 1)
        if all(x == edge.destination for x in backtrack(edge.origin, 1)):
            return False
        #check if straight
        if len(backlog) == max_straight:
            if all(is_straight(edge.destination, last) for last in backtrack(edge.origin, max_straight)):
                return False
        return True
    
    for i in range(1,len(nodes)):
        print(i)
        current = defaultdict(lambda: INF)
        previous_nodes: dict[Coords, List[Coords]] = {}
        is_shortest_changed = False
        for edge in edges:
            curr_distance = current[edge.destination]
            new_distance = previous[edge.origin] + edge.distance
            if new_distance > curr_distance:
                continue
            if new_distance < curr_distance:
                if not is_valid(edge):
                    continue
                current[edge.destination] = new_distance
                previous_nodes[edge.destination] = [edge.origin]
                if new_distance < shortest[edge.destination]:
                    shortest[edge.destination] = new_distance
                    is_shortest_changed = True
            if new_distance != INF and new_distance == curr_distance:
                if is_valid(edge):
                    previous_nodes[edge.destination].append(edge.origin)
        backlog.append(previous_nodes)
        #if distances haven't changed we can stop trying further
        if not is_shortest_changed:
            break
        previous = current

    return shortest[finish]


costs = parse_input('input.txt')
nodes, edges = build_graph(costs)
start = Coords(0,0)
finish = Coords(len(costs[0]) - 1, len(costs) - 1)
shortest = find_shortest_distance(nodes, edges, start, finish)
print(shortest)
pass