import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from itertools import count
from time import sleep
import threading
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

sx_data = []
sy_data = []
sz_data = []

ax = plt.figure().add_subplot(projection='3d')

c = count()

def updateData():
	global sx_data, sy_data, sz_data, t, c
	while True:
		i = next(c)
		sleep(0.005)
		sx_data.append(sx[i])
		sy_data.append(sy[i])
		sz_data.append(0)
		if i == len(t) - 2:
			break
t_data = threading.Thread(target=updateData, args=())
t_data.start()

def animate(i):
	global sx_data, sy_data, sz_data
	ax.cla()
	ax.plot(sx_data, sy_data, sz_data)
	ax.axes.set_zlim3d(bottom=-15, top=15)

ani = FuncAnimation(plt.gcf(), animate, interval=0.5)
plt.show()

#for k in range(len(dt)):
	#print(k)
	#animate(k)
