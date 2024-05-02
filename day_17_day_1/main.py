from typing import List, NamedTuple, Iterator
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
import cProfile

class Coords(NamedTuple):
    x: int
    y: int
    def __repr__(self) -> str:
        return f'{self.x}:{self.y}'

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
        return f'({self.origin}-{self.destination},{self.distance},{self.direction.name})'

'''@dataclass
class Node:
    xy: Coords
    ins: list[Edge]
    outs: list[Edge]
    distance_from: defaultdict[Coords, int]'''

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

    #create a list of nodes sorted by their distance from the start point (0,0)
    nodes.append(Coords(0, 0))
    for layer_num in range(1, max(xmax, ymax)):
        if layer_num < ymax:
            nodes.extend([Coords(x, layer_num) for x in range(0, layer_num)])
        if layer_num < xmax:
            nodes.extend([Coords(layer_num, y) for y in range(0, layer_num)])
        if layer_num < xmax and layer_num < ymax:
            nodes.append(Coords(layer_num,layer_num))

    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            xy = Coords(x, y)
            #nodes.append(xy)
            for nxy, dir in neighbours(xy):
                edge = Edge(xy, nxy, costs[nxy.y][nxy.x], dir)
                edges.append(edge)

    return nodes, edges

def find_optimal_path(nodes: List[Coords], edges: List[Edge], start: Coords, finish: Coords) -> List[List[Edge]]:
    #calc min distances first, then restore the path of minimal distance (or multiple paths if there are more than one)
    #for a path of every length(in number of edges it consists of) we calculate minimal distance we can reach every node and last edge in the path (or multiple edges)
    #obviously not every node is reachable in arbitrary amount of steps

    #group edges by their destination:
    edges_by_origin: dict[Coords, List[Edge]] = defaultdict(list)
    for edge in edges:
        edges_by_origin[edge.origin].append(edge)
    distances_by_path_steps: List[dict[Coords, int]] = [{start: 0}]
    predecessors_by_path_steps: List[dict[Coords, List[Coords]]] = [{}]
    shortest_distances: dict[Coords, int] = {}

    def backtrack(last_node: Coords, steps, index = -1) -> List[List[Coords]]:
        if steps == 1:
            return [[p] for p in predecessors_by_path_steps[index][last_node]]
        else:
            predecessors = predecessors_by_path_steps[index][last_node][:]
            paths = []
            for pred in predecessors:
                backtracked = backtrack(pred, steps - 1, index - 1)
                for path in backtracked:
                    paths.append(path + [pred])
            return paths

    for i in range(1, len(nodes)):
        previous_step_distances = distances_by_path_steps[i - 1]
        current_step_distances: dict[Coords, int] = {}
        current_step_predecessors: dict[Coords, List[Coords]] = {}
        is_shortest_changed = False

        for prev_node, prev_distance in previous_step_distances.items():
            outer_edges = edges_by_origin[prev_node]
            for edge in outer_edges:
                new_distance = prev_distance + edge.distance
                curr_distance = current_step_distances.get(edge.destination, None)

                if curr_distance is None or new_distance < curr_distance:
                    current_step_distances[edge.destination] = new_distance
                    current_step_predecessors[edge.destination] = [prev_node]
                    #add shortest distance and trigger for early finish check
                    if not edge.destination in shortest_distances or new_distance < shortest_distances[edge.destination]:
                        shortest_distances[edge.destination] = new_distance
                        is_shortest_changed = True
                    continue
                if new_distance == prev_distance:
                    current_step_predecessors[edge.destination].append(prev_node)

        if not is_shortest_changed:
            break
        distances_by_path_steps.append(current_step_distances)
        predecessors_by_path_steps.append(current_step_predecessors)

    #restore path
    steps_num = [x[finish] if finish in x else None for x in distances_by_path_steps].index(shortest_distances[finish])
    paths = [path + [finish] for path in backtrack(finish, steps_num, steps_num)]
    pass
    return paths



costs = parse_input('input.txt')
nodes, edges = build_graph(costs)
start = Coords(0,0)
finish = (len(costs[0]) - 1, len(costs) - 1)
paths = find_optimal_path(nodes, edges, start, finish)
for path in paths:
    print(path)
pass