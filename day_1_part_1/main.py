def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]

with open('input.txt', 'r', encoding="utf-8") as f:
    my_sum = 0
    for line in f:
        numbers = set('0123456789')
        number = 0
        for symbol in line:
            if symbol in numbers:
                number += int(symbol) * 10
                break
        reversed = reverse(line)
        for symbol in reversed:
            if symbol in numbers:
                number += int(symbol)
                break
        my_sum += number
    print(my_sum)