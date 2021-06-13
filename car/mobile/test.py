import numpy as np

def get_acc():
	return np.array([np.random.rand(1)[0], np.random.rand(1)[0], np.random.rand(1)[0]])

def get_gyro():
	return np.array([np.random.rand(1)[0], np.random.rand(1)[0], np.random.rand(1)[0]])

ax_off = 0.0
ay_off = 0.0
az_off = 0.0

gx_off = 0.0
gy_off = 0.0
gz_off = 0.0

def calibrate(iterations):
	a = np.array([0.0, 0.0, 0.0])
	w = np.array([0.0, 0.0, 0.0])
	for n in range(iterations):
		a = a + get_acc()
		w = w + get_gyro()
	return [a/iterations, w/iterations]

a_off, w_off = calibrate(1000)

print('a off', a_off)
print('w off', w_off)

while True:
	a = get_acc() - a_off
	w = get_gyro() - w_off
	print('acc\t', a)
	print('gyro\t', w)
	print()

	with open('output.log', 'a') as f:
		f.write('\n{},{}'.format(a, w))
