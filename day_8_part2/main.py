from __future__ import annotations
from typing import List
from dataclasses import dataclass
from typing import NamedTuple

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

def prepare_network(nodes: List[Node], data: dict[str, tuple[str,str]]) -> None:
    # populate network with Node objects
    for n in data:
        node = Node()
        node.value = n
        nodes.append(node)
    #interconnect Nodes    
    for n in nodes:
        left, right = data[n.value]
        #connect left
        for l in nodes:
            if l.value == left:
                n.left = l
                break
        else:
            raise Exception(f'left item not found for ({n.value}, {n.left}, {n.right})')
        #connect right
        for r in nodes:
            if r.value == right:
                n.right = r
                break
        else:
            raise Exception(f'right item not found for ({n.value}, {n.left}, {n.right})')
        
class Loop:
    class LoopStep(NamedTuple):
        directions_index: int
        node: Node

    directions: str = ''

    def __init__(self, header: List[LoopStep], loop: List[LoopStep]) -> None:
        self.header = header
        self.loop = loop
        self._steps = 0

    def get_pos(self) -> int:
        return self._steps
    
    def cycle(self, steps_num: int) -> int:
        '''Cycle through a number of steps. Returns total number of steps cycled'''
        self._steps += steps_num
        return self._steps
    

        
def find_loops(directions: str, walkers: List[Node]) -> List[Loop]:
    loops = []
    for walker in walkers:
        backtrack: List[tuple[int, str]] = []
        steps = 0
        while True:
            for i, step in enumerate(directions):
                if (i, walker) in backtrack:
                    loop_start = backtrack.index((i, walker))
                    loop_length = len(backtrack) - loop_start
                    print(f'loop found! Node: {walker}, loop_length: {loop_length}, directions position: {i}, {step}, loop start position: {loop_start}')
                    loop_header = backtrack[:loop_start]
                    loop = backtrack[loop_start:]
                    loops.append(Loop(loop_header, loop))
                    break
                else:
                    backtrack.append((i, walker))
                walker = walker.left if step =='L' else walker.right
                steps += 1
            else:
                continue
            break
    return loops

directions, data = parse_input('input.txt')
Loop.directions = directions


network = list()
prepare_network(network, data)

#every walker fall into the loop of cycled nodes. We find those loops and their length to
#calculate the periods in which each of them loop over
walkers: List[Node] = list(filter(lambda x: x.value[2] == 'A', network))
loops = find_loops(directions, walkers)

loop = loops[0]
