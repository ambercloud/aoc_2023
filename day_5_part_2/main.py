from __future__ import annotations
from typing import NamedTuple
from typing import List
from dataclasses import dataclass
from functools import reduce

    
class Range:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end if end > start else start
    def __repr__(self) -> str:
        return f"Range({self.start}, {self.end})"
    def __len__(self) -> int:
        return self.end - self.start if self.end > self.start else 0
    def __lt__(self, x: Range) -> bool:
        return True if self.start < x.start else False
    def __gt__(self, x: Range) -> bool:
        return True if self.end > x.end else False
    def __eq__(self, x: Range) -> bool:
        return True if self.start == x.start and self.end == x.end else False
    def intersect(self, x: Range) -> Range:
        return Range(max(self.start, x.start), min(self.end, x.end))
    def difference(self, x: Range) -> List[Range]:
        result = []
        dif1 = Range(self.start, min(self.end, x.start))
        if dif1:
            result.append(dif1)
        dif2 = Range(max(x.end, self.start), self.end)
        if dif2:
            result.append(dif2)
        return result
    
@dataclass
class Offset:
    dest: int
    source: int
    range: int

    def __contains__(self, x: int) -> bool:
        return True if self.source <= x < self.source + self.range else False
    def translate(self, x: Range) -> (List[Range], List[Range]):
        """Take range as input and translate values with a map, return [translated], [remainder]
        remainder is all values not matched."""
        this = Range(self.source, self.source + self.range)
        translated = []
        remainder = []
        offset = self.dest - self.source
        match = x.intersect(this)
        if match:
            if match.start + offset < 0:
                pass
            translated.append(Range(match.start + offset, match.end + offset))
        remainder.extend(x.difference(this))
        return (translated, remainder)

class Map:
    def __init__(self, offset: List[Offset] = None) -> None:
        self.offsets = [] if offset is None else offset
    def append(self, offset: [int]) -> None:
        self.offsets.append(Offset(*offset))
    def translate(self, input: Range) -> List[Range]:
        output = []
        remainder = [input]
        for offset in self.offsets:
            remainder_old = remainder[:]
            remainder = []
            for rnge in remainder_old:
                res = offset.translate(rnge)
                output.extend(res[0])
                remainder.extend(res[1])
        output.extend(remainder)
        return output

        # join translated and not remapped together
        return output
    
class Mappable(list):
    def map(self, m: Map) -> Mappable:
        output = Mappable()
        for x in self:
            output.extend(m.translate(x))
        return output

def parse_input(seeds: List[int], seed_soil: Map, soil_fert: Map, fert_water: Map, \
                water_light: Map, light_temp: Map, temp_humid: Map, humid_loc: Map) -> None:
    f = open('input.txt', 'r', encoding='utf-8')
    line = f.readline()
    temp = [x for x in map(int, line.removeprefix('seeds: ').split())]
    seeds += [Range(temp[x], temp[x] + temp[x+1]) for x in range(0, len(temp), 2)]
    f.readline()
    #skip header
    f.readline()
    # fill seed to soil map
    while line := f.readline().removesuffix('\n'):
        seed_soil.append(map(int, line.split()))
    # fill soil to fert map
    f.readline()
    while line := f.readline().removesuffix('\n'):
        soil_fert.append(map(int, line.split()))
    # fill fert to water map
    f.readline()
    while line := f.readline().removesuffix('\n'):
        fert_water.append(map(int, line.split()))
    # fill water to light map
    f.readline()
    while line := f.readline().removesuffix('\n'):
        water_light.append(map(int, line.split()))
    # fill light to temp map
    f.readline()
    while line := f.readline().removesuffix('\n'):
        light_temp.append(map(int, line.split()))
    # fill temp to humid map
    f.readline()
    while line := f.readline().removesuffix('\n'):
        temp_humid.append(map(int, line.split()))
    # fill humid to loc map
    f.readline()
    while line := f.readline().removesuffix('\n'):
        humid_loc.append(map(int, line.split()))

seeds = Mappable()

maps = [Map([]) for i in range(7)]

parse_input(seeds, *maps)

seed_soil, soil_fert, fert_water, water_light, light_temp, temp_humid, humid_loc = maps

locations = reduce(lambda prev, next: prev.map(next), maps, seeds)
print(min(locations))