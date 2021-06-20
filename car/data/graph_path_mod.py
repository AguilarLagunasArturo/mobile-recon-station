import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import random

if len(sys.argv) < 2:
    raise Exception('Missing args')
    exit()

with open(sys.argv[1], 'r') as f:
    lines = f.read().split('\n')

values = [];
for line in lines:
    if line:
        values.append( [val for val in line.split(',')] )

values = np.longdouble(values)

t = values[:, 0]
dt = values[:, 1]
dir = values[:, 2]
wz = values[:, -1]

theta = dt * wz
theta = np.cumsum(theta)

sx = dt * dir * np.cos(theta * np.pi/180)
sx = np.cumsum(sx)
sy = dt * dir * np.sin(theta * np.pi/180)
sy = np.cumsum(sy)
sz = [ np.sin(x * 1/120) for x in range( len(sy) )]

ax = plt.figure().add_subplot(projection='3d')
ax.plot(sx, sy, sz)
ax.axes.set_zlim3d(bottom=-15, top=15)
plt.show()
