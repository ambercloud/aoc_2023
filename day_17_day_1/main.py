from __future__ import annotations
from typing import List
from dataclasses import dataclass, field, fields
from math import inf as INF
from functools import total_ordering
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

@dataclass
@total_ordering
class Node:
    x: int
    y: int
    cost: int
    visited: bool = False
    min_cost_to_reach: int|float = INF
    neighbours: list[Node] = field(default_factory=list)

    def __hash__(self) -> int:
        return f'{self.x}:{self.y}'.__hash__()
    
    #stop debugger from stucking on circular refs
    def __repr__(self, depth = 1) -> str:
        if depth > 0:
            return (f'Node({self.x}:{self.y}, {self.cost}, {'✔' if self.visited else '✖'}, '
                    f'{self.min_cost_to_reach}, {[x.__repr__(depth - 1) for x in self.neighbours]})')
        else:
            return (f'Node({self.x}:{self.y}, {self.cost}, {'✔' if self.visited else '✖'}, '
                    f'{self.min_cost_to_reach}, […])')            
        
    def __lt__(self, other: Node) -> bool:
        return (self.min_cost_to_reach, self.cost) < (other.min_cost_to_reach, other.cost)
    
    def __eq__(self, other: Node) -> bool:
        return fields(self) == fields(other)


def parse_input(filename) -> List[List[Node]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for y, line in enumerate(f):
        output.append([Node(x, y, int(cost)) for x, cost in enumerate(line.removesuffix('\n'))])
    return output

def gen_neighbours(xo: int, yo: int, xrange: range, yrange: range):
    around = ((xo - 1, yo), (xo + 1, yo), (xo, yo - 1), (xo, yo + 1))
    for x, y in around:
        if x in xrange and y in yrange:
            yield x, y

def connect_nodes(nodes: List[List[Node]]) -> None:
    xrange = range(len(nodes[0]))
    yrange = range(len(nodes))
    for y_origin, row in enumerate(nodes):
        for x_origin, node in enumerate(row):
            for x_neighbor, y_neighbor in gen_neighbours(x_origin, y_origin, xrange, yrange):
                node.neighbours.append(nodes[y_neighbor][x_neighbor])

def mark_min_cost_to_reach(nodes: List[List[Node]], start: Node) -> None:
    nodes_to_check = PQueue()
    start.min_cost_to_reach = 0
    current = start
    while current:
        current.visited = True
        unchecked = [x for x in current.neighbours if not x.visited]
        for n in unchecked:
            n.min_cost_to_reach = min(n.min_cost_to_reach, current.min_cost_to_reach + n.cost)
            try:
                nodes_to_check.remove_task(n)
            except KeyError:
                pass
            nodes_to_check.add_task(n, n.min_cost_to_reach)
        try:
            current = nodes_to_check.pop_task()
        except KeyError:
            break
    pass

def mark_path(nodes: List[List[Node]], finish: Node) -> List[List[str]]:
    marked_output = [[str(node.cost) for node in row] for row in nodes]
    current = finish
    while not current.min_cost_to_reach == 0:
        marked_output[current.y][current.x] = 'x'
        current = min(current.neighbours, key = lambda node: node.min_cost_to_reach)
    return marked_output

def print_debug(input: List[List[str]]) -> None:
    d = open('debug.txt', 'w', encoding='utf-8')
    for row in input:
        line = ''.join(row) + '\n'
        d.write(line)

nodes = parse_input('input.txt')
connect_nodes(nodes)
mark_min_cost_to_reach(nodes, nodes[0][0])
print_debug(mark_path(nodes, nodes[-1][-1]))

pass