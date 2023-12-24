from __future__ import annotations
from typing import List

class Node:

    def __init__(self) -> None:
        self.value: str = ""
        self.left: Node = None
        self.right: Node = None
    def __repr__(self) -> str:
        return f'Node({self.value}, {self.left.value}, {self.right.value})'


def walk(directions:str, network: List[Node]):
    steps = 0
    walkers = list(filter(lambda x: x.value[2] == 'A', network))
    for node in network:
        node.finish = True if node.value[2] == 'Z' else False
    while True:
        for step in directions:
            walkers = list(map(lambda node: node.left if step == 'L' else node.right, walkers))
            steps += 1
            zs = [w.finish for w in walkers]
            if zs.count(True) > 2:
                print(f'{zs.count(True)}, {steps}')
            if all(zs):
                return steps


def parse_input(filename: str) -> tuple[str, dict[str,tuple[str,str]]]:
    f = open(filename, 'r', encoding='utf-8')
    directions = f.readline().removesuffix('\n')
    f.readline()
    data = dict()
    for line in f:
        data[line[0:3]] = (line[7:10], line[12:15])
    return (directions, data)

directions, data = parse_input('input.txt')

network = list()
# populate network with Node objects
for n in data:
    node = Node()
    node.value = n
    network.append(node)
#interconnect Nodes    
for n in network:
    left, right = data[n.value]
    #connect left
    for l in network:
        if l.value == left:
            n.left = l
            break
    else:
        raise Exception(f'left item not found for ({n.value}, {n.left}, {n.right})')
    #connect right
    for r in network:
        if r.value == right:
            n.right = r
            break
    else:
        raise Exception(f'right item not found for ({n.value}, {n.left}, {n.right})')

print(walk(directions, network))