from __future__ import annotations
from typing import List, NamedTuple, Iterator
from dataclasses import dataclass, field
from enum import Enum
import heapq
import itertools

class PQueue:
    REMOVED = '<removed-task>'      # placeholder for a removed task

    def __init__(self) -> None:
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
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
        entry[-1] = PQueue.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not PQueue.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

class Coords(NamedTuple):
    x: int
    y: int

class Direction(Enum):
    n = 1
    e = 2
    s = 3
    w = 4

@dataclass
class Node:
    xy: Coords
    min_distance_from: dict[Coords: int] = field(default_factory=dict)
    #edges: node, distance, direction
    outs: list[tuple[Node, int, Direction]] = field(default_factory=list) #outward edge: node, distance, direction
    ins: list[tuple[Node, int, Direction]] = field(default_factory=list) #inward edge: node, distance, direction
    
    #stop debugger from stucking on circular refs
    def __repr__(self) -> str:
        return (f'Node({self.xy})')

def gen_neighbours(xo: int, yo: int, xrange: range, yrange: range) -> Iterator[tuple[int, int, Direction]]:
    dir = Direction
    around = ((xo, yo - 1, dir.n), (xo + 1, yo, dir.e), (xo, yo + 1, dir.s), (xo - 1, yo, dir.w))
    for x, y, d in around:
        if x in xrange and y in yrange:
            yield x, y, d

def parse_input(filename) -> List[List[Node]]:
    f = open(filename, 'r', encoding='utf-8')
    costs = []
    for y, line in enumerate(f):
        costs.append([int(x) for x in line.removesuffix('\n')])

    nodes: dict[Coords, Node] = {}
    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            node = Node((x, y))
            nodes[(x, y)] = node

    xmax = len(costs[0])
    ymax = len(costs)
    
    for y, row in enumerate(costs):
        for x, cost in enumerate(row):
            node = nodes[(x, y)]
            for xn, yn, d in gen_neighbours(x, y, range(0, xmax), range(0, ymax)):
                neighbour = nodes[(xn, yn)]
                neighbour_cost = costs[yn][xn]
                #create edges: outward edge in current node to every neighbour and inward edge from current node to every neighbour
                node.outs.append((neighbour, neighbour_cost, d))
                neighbour.ins.append((node, cost, d))

    return nodes

def mark_min_cost_to_reach(nodes: dict[Coords, Node], origin: Node) -> None:
    #marks min distance from origin to every other node, modified Dijkstra algorithm
    nodes_to_check = PQueue()
    visited: set[Coords] = set()
    o_xy = origin.xy
    origin.min_distance_from[o_xy] = 0
    current = origin
    while current:
        visited.add(current.xy)
        unchecked = [(neighbour, distance, direction) for neighbour, distance, direction in current.outs if not neighbour.xy in visited]
        for neighbour, distance, direction in unchecked:
            if not o_xy in neighbour.min_distance_from or (current.min_distance_from[o_xy] + distance) < neighbour.min_distance_from[o_xy]:
                neighbour.min_distance_from[o_xy] = current.min_distance_from[o_xy] + distance
            try:
                nodes_to_check.remove_task(neighbour.xy)
            except KeyError:
                pass
            nodes_to_check.add_task(neighbour.xy, neighbour.min_distance_from[o_xy])
        try:
            next_xy = nodes_to_check.pop_task()
            current = nodes[next_xy]
        except KeyError:
            break

nodes = parse_input('input.txt')
mark_min_cost_to_reach(nodes, nodes[(0,0)])
pass