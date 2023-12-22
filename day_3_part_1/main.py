import re
from collections import namedtuple

Linepos = namedtuple('Linepos', 'line pos')
Number = namedtuple('Number', 'value line start end')

f = open('input.txt', 'r', encoding='utf-8')

#let's build a map of symbols and numbers

re_num = re.compile(r'(\d++)')
re_sym = re.compile(r'[^.\d\n]')

numbers = []
symbols = set()

for line_num, line in enumerate(f):
    for match in re_sym.finditer(line):
        sym = Linepos(line_num, match.start())
        symbols.add(sym)
    for match in re_num.finditer(line):
        value = int(match[1])
        number = Number(value, line_num, match.start(1), match.end(1))
        numbers.append(number)

'''for each number construct a set of positions of surrounding characters
 and check if it intersects with set of symbols positions'''

def is_symbol_nearby(num: Number, symbols: set) -> bool:
    adjacent = set()
    #fill with positions line above
    adjacent.update({Linepos(num.line - 1, pos) for pos in range(num.start - 1, num.end + 1)})
    #fill with positions left and right
    adjacent.update({Linepos(num.line, num.start - 1), Linepos(num.line, num.end)})
    #fill with positions line below
    adjacent.update({Linepos(num.line + 1, pos) for pos in range(num.start - 1, num.end + 1)})
    return not adjacent.isdisjoint(symbols)

part_numbers = [num.value for num in numbers if is_symbol_nearby(num, symbols)]
print(sum(part_numbers))