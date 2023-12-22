import re
from typing import NamedTuple

class Coords(NamedTuple):
    def __repr__(self) -> str:
        return f"Coords({self.line}, {self.pos})"
    line: int
    pos: int

class Token:
    def __init__(self, string: str, xy: Coords) -> None:
        self.string: str = string
        self.line = xy.line
        self.start = xy.pos
        self.end = self.start + len(self.string)
    def __repr__(self) -> str:
        return f"Token('{self.string}', {self.line}-{self.start})"
    def list_pos(self) -> list[Coords]:
        positions = [Coords(self.line, pos) for pos in range(self.start, self.end)]        
        return positions
    
class Symbol(Token):
    def __init__(self, string: str, xy: Coords) -> None:
        super().__init__(string, xy)

class Number(Token):
    def __init__(self, string: str, xy: Coords) -> None:
        super().__init__(string, xy)
        self.value = int(self.string)

def list_adjacent(token: Token, tokenmap: dict[Coords, Token]) -> set[Token]:
    pos_list = [Coords(token.line - 1, pos) for pos in range(token.start - 1, token.end + 1)]
    pos_list += [Coords(token.line, token.start - 1), Coords(token.line, token.end)]
    pos_list += [Coords(token.line + 1, pos) for pos in range(token.start - 1, token.end + 1)]
    pos_list = filter(lambda pos: pos in tokenmap, pos_list)
    token_list = [tokenmap[pos] for pos in pos_list]
    return set(token_list)

def is_part_number(num: Number, tokenmap: dict[Coords, Token]) -> bool:
    token_list = list_adjacent(num, tokenmap)
    for token in token_list:
        if isinstance(token, Symbol):
            return True
    return False
    

#let's build a map of symbols and numbers

re_num = re.compile(r'(\d++)')
re_sym = re.compile(r'([^.\d\n])')

tokenmap = {}
numbers = []
symbols = []

f = open('input.txt', 'r', encoding='utf-8')

for line_num, line in enumerate(f):
    for match in re_sym.finditer(line):
        xy = Coords(line_num, match.start(1))
        sym = Symbol(match[1], xy)
        tokenmap.update([(pos, sym) for pos in sym.list_pos()])
        symbols.append(sym)
    for match in re_num.finditer(line):
        xy = Coords(line_num, match.start(1))
        num = Number(match[1], xy)
        tokenmap.update([(pos, num) for pos in num.list_pos()])
        numbers.append(num)

# find all the part_numbers
        
part_numbers = [x for x in filter(lambda x: is_part_number(x, tokenmap), numbers)]
print(sum([x.value for x in part_numbers]))

#now to the gears
        
asterisks = filter(lambda x: x.string == "*", symbols)
gears = []
for ast in asterisks:
    adj = list_adjacent(ast, tokenmap)
    # count all tokens in adj that also in part numbers
    adj_parts = [x for x in filter(lambda x: x in part_numbers, adj)]
    if len(adj_parts) == 2:
        gears.append((ast, adj_parts))
ratios = [parts[0].value * parts[1].value for gear, parts in gears]
answer = sum(ratios)
print(answer)