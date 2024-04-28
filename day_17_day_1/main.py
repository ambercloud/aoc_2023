from __future__ import annotations
from typing import List, NamedTuple, Iterator
from enum import Enum
from collections import deque, defaultdict
from itertools import groupby

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

class Node:
    def __init__(self, data: Coords) -> None:
        super().__init__()
        self.data: Coords = data
        self.children: set[Node] = set()
        self.parent: Node = None

class Tree:
    def __init__(self, data: Coords) -> None:
        super().__init__()
        node = Node(data)
        self.root = node
        self.leafs = {node}
        self.length = 1

    def append(self, child: Tree) -> None:
        #we only append to the root and all trees we append are the same length
        self.root.children.add(child.root)
        #if there's only root in the tree - remove it from list of leaves
        if self.length == 1:
            self.leafs.remove(self.root)
        child.root.parent = self.root
        self.leafs.update(child.leafs)
        self.length = child.length + 1

    def trim(self) -> None:
        #remove last nodes in the tree
        new_leafs = {leaf.parent for leaf in self.leafs}
        for leaf in new_leafs:
            leaf.children = {}
        self.leafs = new_leafs
        self.length -= 1

        

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
    max_straight = 3

    node_inputs: dict[Coords, List[Edge]] = defaultdict(list)
    for edge in edges:
        node_inputs[edge.destination].append(edge)

    INF = float('inf')
    previous: dict[Coords, int|float] = defaultdict(lambda: INF)
    shortest: dict[Coords, int|float] = defaultdict(lambda: INF)
    backlog: dict[Coords, Tree[Coords]] = {}
    previous[start] = 0
    backlog[start] = Tree(start)

    def is_valid(edge: Edge, backlogdict: dict[Coords, Tree[Coords]], max_straight = max_straight) -> bool:
        backlog = backlogdict[edge.origin]
        #check for 180-turns
        if backlog.length > 1 and all((edge.destination == prevprevnode.data for prevprevnode in backlog.root.children)):
            return False
        #check for straight routes
        if backlog.length >= max_straight:
            if all((abs(edge.destination.x - lastnode.data.x) == max_straight + 1) or (abs(edge.destination.y - lastnode.data.y) == max_straight + 1) for lastnode in backlog.leafs):
                return False
        return True
    
    for i in range(1,len(nodes)):
        print(i)
        current = defaultdict(lambda: INF)
        newbacklog: dict[Coords, Tree[Coords]] = {}
        for node, inputs in node_inputs.items():
            valid_inputs = (edge for edge in inputs if not (previous[edge.origin] == INF) and is_valid(edge, backlog))
            new_dist_by_input = sorted(((previous[edge.origin] + edge.distance, edge) for edge in valid_inputs), key = lambda x: x[0])
            try:
                min_dist, min_edges = next(groupby(new_dist_by_input, key = lambda x: x[0]))
            except StopIteration:
                continue
            current[node] = min_dist
            shortest[node] = min(shortest[node], min_dist)
            tree = Tree(node)
            for dist, edge in min_edges:
                tree.append(backlog[edge.origin])
            newbacklog[node] = tree
        backlog = newbacklog
        previous = current

    return shortest[finish]


costs = parse_input('input.txt')
nodes, edges = build_graph(costs)
start = Coords(0,0)
finish = Coords(len(costs[0]) - 1, len(costs) - 1)
shortest = find_shortest_distance(nodes, edges, start, finish)
print(shortest)
pass