f = open('input.txt', 'r', encoding='utf-8')

def parse_line(line: str) -> tuple[list[int], list[int]]:
    line = line.partition(': ')[2]
    left, _, right = line.partition('|')
    winning = [int(x) for x in left.split()]
    numbers = [int(x) for x in right.split()]
    return (winning, numbers)

def calc_points(winning: list[int], numbers: list[int]) -> int:
    count = sum(num in winning for num in numbers)
    return 2 ** (count - 1) if count > 0 else 0

points = []
for line in f:
    parsed = parse_line(line)
    pts = calc_points(*parsed)
    points.append(pts)
print(sum(points))