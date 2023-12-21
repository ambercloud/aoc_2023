from __future__ import annotations
from typing import NamedTuple
from typing import List
from dataclasses import dataclass


@dataclass
class Offset():
    dest: int
    source: int
    range: int

    def __contains__(self, x: int) -> bool:
        return True if self.source <= x < self.source + self.range else False
    def translate(self, x: int) -> int:
        return x + self.dest - self.source if x in self else None

class Map:
    def __init__(self, offset: List[Offset] = None) -> None:
        self.offsets = [] if offset is None else offset
    def append(self, offset: [int]) -> None:
        self.offsets.append(Offset(*offset))
    def translate(self, input: int) -> int:
        for offset in self.offsets:
            output = offset.translate(input)
            if output:
                return output
        # we didn't found mapped values, return as is
        return input
    
class Mappable(list):
    def map(self, m: Map) -> Mappable:
        return Mappable([m.translate(x) for x in self])

def parse_input(seeds: List[int], seed_soil: Map, soil_fert: Map, fert_water: Map, \
                water_light: Map, light_temp: Map, temp_humid: Map, humid_loc: Map) -> None:
    f = open('input.txt', 'r', encoding='utf-8')
    line = f.readline()
    seeds += map(int, line.removeprefix('seeds: ').split())
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

locations = seeds.map(seed_soil).map(soil_fert).map(fert_water).map(water_light)\
.map(light_temp).map(temp_humid).map(humid_loc)

print(min(locations))