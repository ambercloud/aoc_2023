from __future__ import annotations
from typing import List
from typing import NamedTuple
import math

class Node:
    def __init__(self) -> None:
        self.value: str = ""
        self.left: Node = None
        self.right: Node = None
    def __repr__(self) -> str:
        return f'Node({self.value}, {self.left.value}, {self.right.value})'

class Walker:
    def _find_loop(self, start: Node, directions: str) -> tuple[List[Node], List[Node]]:
        backtrack: List[tuple[int, Node]] = []
        walker = start
        while True:
            for i, step in enumerate(directions):
                if (i, walker) in backtrack:
                    loop_start = backtrack.index((i, walker))
                    loop_length = len(backtrack) - loop_start
                    print(f'loop found! Node: {walker}, loop_length: {loop_length}, directions position: {i}, {step}, loop start position: {loop_start}')
                    backtrack_stripped = [x[1] for x in backtrack]
                    loop_header = backtrack_stripped[:loop_start]
                    loop = backtrack_stripped[loop_start:]
                    return (loop_header, loop)
                else:
                    backtrack.append((i, walker))
                    walker = walker.left if step =='L' else walker.right

    def __init__(self, start: Node, directions:str) -> None:
        self.start = start
        self._directions = directions
        self.step = 0
        self.header, self.loop = self._find_loop(self.start, self._directions)
        self.loop_offset = len(self.header)
        self.loop_length = len(self.loop)
    def __repr__(self) -> str:
        return f"Walker(start: '{self.start.value}', offset: {self.loop_offset}, loop_length: {self.loop_length})"

    def walk_at(self, steps_num: int) -> Node:
        "Returns a node walker arrives at after number of steps"
        if steps_num < self.loop_offset:
            return self.header[steps_num]
        else:
            position_in_loop = (steps_num - self.loop_offset) % self.loop_length
            return self.loop[position_in_loop]
    def find(self, f: function):
        "Returns values found in the header and the loop body of Walker and their respective positions"
        h = filter(lambda x: f(x[1]), enumerate(self.header))
        l = filter(lambda x: f(x[1]), enumerate(self.loop))
        return ([x for x in h], [x for x in l])

def parse_input(filename: str) -> tuple[str, dict[str,tuple[str,str]]]:
    f = open(filename, 'r', encoding='utf-8')
    directions = f.readline().removesuffix('\n')
    f.readline()
    data = dict()
    for line in f:
        data[line[0:3]] = (line[7:10], line[12:15])
    return (directions, data)

def prepare_network(nodes: dict[str, Node], data: dict[str, tuple[str,str]]) -> None:
    # populate network with Node objects
    for key in data:
        node = Node()
        node.value = key
        nodes[key] = node
    #interconnect Nodes    
    for key, node in nodes.items():
        left, right = data[key]
        #connect left
        node.left = nodes[left]
        #connect right
        node.right = nodes[right]

def calc_steps_to_finish(walkers: List[Walker]):
    #sort walkers by loop length first
    walkers = sorted(walkers, key = lambda x: x.loop_length, reverse=True)
    #set starting point for cycling for first walker
    big = walkers[0]
    h, l = big.find(lambda x: x.value[2] == 'Z')
    #we know that all Zs are in the loop, no need to check for header
    #calculate offset by summing header length and index of found value in the loop
    steps = big.loop_offset + l[0][0]
    cycle_size = big.loop_length
    print(f'first walker, steps: {steps}, {big.walk_at(steps)}')
    for w in walkers[1:]:
        print(f'walker initial, steps: {steps}, {w.walk_at(steps)}')
        while w.walk_at(steps).value[2] != 'Z':
            steps = steps + cycle_size
        print(f'walker final, steps: {steps}, {w.walk_at(steps)}')
        cycle_size = math.lcm(cycle_size, w.loop_length)
    return steps
        

directions, data = parse_input('input.txt')
network = dict()
prepare_network(network, data)

#every walker fall into the loop of cycled nodes. We find those loops and their length to
#calculate the periods in which each of them loop over
walkers: List[Walker] = [Walker(node, directions) for key, node in network.items() if key[2] == 'A']
steps = calc_steps_to_finish(walkers)
print(f'steps: {steps}')
for w in walkers:
    print(w.walk_at(steps))