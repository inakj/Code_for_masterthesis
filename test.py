import numpy as np

d = 0.9
b = 0.3
e = 0.4
a = 0.262
netta = 13.9
ro = 0.0052


coefficients = [d / (6 * (e + a)), 0.5 * (1 - d / (e + a)), netta * ro, - netta * ro] 
roots = np.roots(coefficients)

print(roots)
for num in roots:
    if 0 < num < 1:
        answer = num
print(float(answer))
