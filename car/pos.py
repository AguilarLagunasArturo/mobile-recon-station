import numpy as np
import matplotlib.pyplot as plt

with open('13-6-2021_1-40-50.csv', 'r') as f:
    lines = f.read().split('\n')

lines = lines[0:-1]
print( len(lines) )
values = []

for line in lines:
    if line:
        values.append(line.split(','))

v = np.array(values, np.float64)
print(v.shape)
print(v[:,0].shape)

t = v[:, 0]
dt =  v[:, 1]
px = v[:, 2] * dt
py = v[:, 3] * dt
pz = v[:, 4] * dt

with open('test-pos.csv', 'a') as f:
	for a, b, c, d in zip(t, px*dt, py*dt, pz*dt):
		f.write( '\n{},{},{},{}'.format(a, b, c, d) )
