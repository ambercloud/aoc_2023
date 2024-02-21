f = open('input.txt', 'r', encoding='utf-8')

def parse_line(line: str) -> tuple[int, list[int], list[int]]:
    id, _, line = line.partition(': ')
    id = int(id.removeprefix('Card').lstrip())
    left, _, right = line.partition('|')
    winning = [int(x) for x in left.split()]
    numbers = [int(x) for x in right.split()]
    return (id, winning, numbers)

# count cards recursivly second parameter is full card table to lookup for copies
def count_cards(cards: list[tuple[int, list[int], list[int]]], cards_ref):
    count = 0
    for card in cards:
        count += 1
        id, winning, numbers = card
        matches = sum(num in winning for num in numbers)
        #copy required amount of cards from ref respecting boundaries
        copies = cards_ref[id:min(id + matches, len(cards_ref))]
        count += count_cards(copies, cards_ref)
    return count


cards = []
for line in f:
    card = parse_line(line)
    cards.append(card)

#process cards

print(count_cards(cards, cards))