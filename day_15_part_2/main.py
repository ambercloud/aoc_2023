from typing import List, OrderedDict
from collections import OrderedDict

def parse_input(filename) -> List[str]:
    f = open(filename, 'r', encoding='utf-8')
    output = []
    for line in f:
        output.extend(line.removesuffix('\n').split(','))
    return output

def char_to_int(ch: str) -> int:
    return ch.encode(encoding='ascii')[0]

def calc_hash(input: str) -> int:
    hash = 0
    for ch in input:
        hash = hash + char_to_int(ch)
        hash = hash * 17
        hash = hash % 256
    return hash

def process_instruction(instruction: str, boxes: List[OrderedDict]) -> None:
    if instruction[-1] == '-':
        label = instruction[:-1]
        boxnum = calc_hash(label)
        box = boxes[boxnum]
        if label in box:
            del box[label]
    else:
        label = instruction[:-2]
        focal = int(instruction[-1])
        boxnum = calc_hash(label)
        box = boxes[boxnum]
        box[label] = focal

def run_hashmap(input: List[str], boxes: List[OrderedDict]) -> None:
    for instruction in input:
        process_instruction(instruction, boxes)

def calc_powers(boxes:List[OrderedDict]) -> List[int]:
    box_powers = []
    for boxnum, box in enumerate(boxes):
        lens_focals = box.values()
        lens_powers = [(boxnum + 1) * lensnum * focal for lensnum, focal in enumerate(lens_focals, 1)]
        box_powers.append(sum(lens_powers))
    return box_powers

input = parse_input('input.txt')
boxes = [OrderedDict() for x in range(256)]
run_hashmap(input, boxes)
box_powers = calc_powers(boxes)
print(sum(box_powers))