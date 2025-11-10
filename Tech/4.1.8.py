import math

def f(x):
    return math.acos(x) + math.asin(2*x) + math.atan(3*x)

# Демонстрация
for x in [-0.5, -0.2, 0, 0.2, 0.5]:
    print(f"x = {x}, y = {f(x):.4f}")


print(sum([ord(s) for s in "DanilMannanov"])%10)

