from typing import List, NamedTuple, Iterator, TypeAlias
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
    distance: int
    direction: Direction

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

    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            xy = Coords(x, y)
            nodes.append(xy)
            for nxy, dir in neighbours(xy):
                edge = Edge(xy, nxy, costs[nxy.y][nxy.x], dir)
                edges.append(edge)

    return nodes, edges

def find_optimal_path(nodes: List[Coords], edges: List[Edge], start: Coords, finish: Coords) -> List[Edge]:
    #calc min distances first, then restore the path
    #for a path of every length(in number of edges it consists of) we calculate minimal distance we can reach every node and last edge in the path (or multiple edges)
    #obviously not every node is reachable in arbitrary amount of steps
    INF = float('inf')
    NodeData = tuple[int|float, List[Edge]]

    def backtrack(min_dist_by_path_length: List[dict[Coords, NodeData]], path_length: int, steps_back: int, last_node: Coords) -> List[List[Edge]]:
        paths_list = [[edge] for edge in min_dist_by_path_length[path_length][last_node][1]]
        path_length = path_length - 1
        steps_back = steps_back - 1
        if path_length and steps_back:
            extended_paths = []
            for path in paths_list:
                edge = path[-1]
                previous_paths = backtrack(min_dist_by_path_length, path_length, steps_back, edge.origin)
                extended_paths.extend([path + prev_path for prev_path in previous_paths])
            paths_list = extended_paths
        return paths_list

    max_path_length = len(nodes) - 1
    min_dist_by_path_length: List[dict[Coords, NodeData]] = [{xy: (INF, []) for xy in nodes} for _ in range(max_path_length + 1)]
    min_dist_by_path_length[0][start] = (0, [None])
    for i in range(1, max_path_length + 1):
        for edge in edges:
            current_distance = min_dist_by_path_length[i][edge.destination][0]
            new_distance = min_dist_by_path_length[i - 1][edge.origin][0] + edge.distance
            if new_distance == INF and current_distance == INF:
                continue
            if new_distance < current_distance:
                min_dist_by_path_length[i][edge.destination] = (new_distance, [edge])
            elif new_distance == current_distance:
                min_dist_by_path_length[i][edge.destination][1].append(edge)
    
    #restore the shortest path
    finish_distances = [x[finish] for x in min_dist_by_path_length]
    index, shortest = min(enumerate(finish_distances), key = lambda x: x[1][0])
    shortest_paths = backtrack(min_dist_by_path_length, index, index, finish)
    shortest_paths = [[y for y in reversed(x)] for x in shortest_paths]
    pass



costs = parse_input('input.txt')
nodes, edges = build_graph(costs)
start = (0,0)
finish = (len(costs[0]) - 1, len(costs) - 1)
path = find_optimal_path(nodes, edges, start, finish)
pass