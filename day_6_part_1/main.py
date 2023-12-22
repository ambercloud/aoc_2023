from functools import reduce

f = open('input.txt', 'r', encoding='utf-8')
time = [ int(x) for x in f.readline().removeprefix('Time:').split() ]
distance = [ int(x) for x in f.readline().removeprefix('Distance:').split() ]
data = [x for x in zip(time, distance)]

ways_to_win = []
for time, record in data:
    count = 0
    for t_charge in range(0, time+1):
        t_run = time - t_charge
        velocity = t_charge
        distance = velocity * t_run
        if distance > record:
            count += 1
    ways_to_win.append(count)
print(ways_to_win)
print(reduce(lambda acc, curr: acc * curr, ways_to_win))