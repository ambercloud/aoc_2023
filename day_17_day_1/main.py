from __future__ import annotations
from typing import List
from dataclasses import dataclass, field



@dataclass
class Node:
    x: int
    y: int
    cost: int
    visited: bool = False
    min_cost_to_reach: int|None = None
    neighbours: list[Node] = field(default_factory=list)

#stop debugger from stucking on circular refs
    def __repr__(self, depth = 1) -> str:
        if depth > 0:
            return (f'Node({self.x}:{self.y}, {self.cost}, {'✔' if self.visited else '✖'}, '
                    f'{self.min_cost_to_reach}, {[x.__repr__(depth - 1) for x in self.neighbours]})')
        else:
            return (f'Node({self.x}:{self.y}, {self.cost}, {'✔' if self.visited else '✖'}, '
                    f'{self.min_cost_to_reach}, […])')

def parse_input(filename) -> List[List[int]]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for y, line in enumerate(f):
        output.append([Node(x, y, cost) for x, cost in enumerate(line.removesuffix('\n'))])
    return output

def connect_nodes(nodes: List[List[Node]]) -> None:
    xmax = len(nodes[0])
    ymax = len(nodes)
    for y, row in enumerate(nodes):
        for x, node in enumerate(row):
            around = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            for x, y in around:
                if x in range(0,xmax) and y in range(0,ymax):
                    node.neighbours.append(nodes[y][x])

nodes = parse_input('input.txt')
connect_nodes(nodes)
pass