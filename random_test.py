import random
steps = 1000000
sum = 0
for i in range(steps):
    sum += round(random.random())
print(sum / steps)
#[print(round(random.random())) for i in range(100)]