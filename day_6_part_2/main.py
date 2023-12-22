from math import sqrt
from decimal import *

f = open('input.txt', 'r', encoding='utf-8')
time = int(f.readline().removeprefix('Time:').replace(' ', ''))
record = int(f.readline().removeprefix('Distance:').replace(' ', ''))

# distance = t_run * velocity
# velocity = t_charge
# t_run = time - t_charge
#distance = (time - t_charge) * t_charge
#distance = time * t_charge - t_charge ^ 2
# t_charge ^ 2 - time * t_charge + distance = 0
getcontext().prec = 50
# I don't know why but the answer is off just by 1 and this thing fixes it.
time = Decimal(time+1)
record = Decimal(record)

d = time ** 2 - 4 * record
print(d)
left = (time - Decimal.sqrt(d))/2
right = (time + Decimal.sqrt(d))/2
print((left, right))
left = left.to_integral_exact(rounding=ROUND_UP)
right = right.to_integral_exact(rounding=ROUND_DOWN)
print(left, right)
print(right - left)