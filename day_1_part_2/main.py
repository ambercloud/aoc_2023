from functools import reduce

def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]

with open('input.txt', 'r', encoding="utf-8") as f:
    my_sum = 0
    for line in f:
        enumerated = [x for x in enumerate(line)]
        digits = set('0123456789')
        digit_words = [x for x in enumerate(['zero','one','two','three','four','five','six','seven','eight','nine'])]
        entries_found_left = []
        entries_found_right = []

        for pos, symbol in enumerated:
            if symbol in digits:
                entries_found_left.append((pos, int(symbol)))
                break
        for digit, dword in digit_words:
            pos = line.find(dword)
            if pos == -1:
                continue
            entries_found_left.append((pos, digit))

        reversed = reverse(enumerated)
        for pos, symbol in reversed:
            if symbol in digits:
                entries_found_right.append((pos, int(symbol)))
                break
        for digit, dword in digit_words:
            pos = line.rfind(dword)
            if pos == -1:
                continue
            entries_found_right.append((pos, digit))

        lpos, left = reduce(lambda acc, next: min(acc, next), entries_found_left)
        rpos, right = reduce(lambda acc, next: max(acc, next), entries_found_right)
        value = left * 10 + right
        my_sum += value

    print(my_sum)