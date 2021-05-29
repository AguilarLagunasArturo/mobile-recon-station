import cv2
import numpy as np

''' Capture video from default webcam '''

# base, dimentions for grid, list of images, scale
def stacking(base, dim, grid, scale=0.5):
	# 1. ESCALAR
	base = cv2.resize(base, (0, 0), fx=scale, fy=scale)
	grid = [cv2.resize(image, (0, 0), fx=scale, fy=scale) for image in grid]
	# 2. COMPLETAR DIMENCIONES
	for index, img in enumerate(grid):
		if len(img.shape) < 3:
			grid[index] = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	# 2.2. CREANDO GRID
	missing = dim[0]*dim[1] - len(grid)
	if missing < 0:
		raise Exception('Wrong dimentions to create grid')
	for i in range(missing):
		grid.append(np.zeros(base.shape, dtype=np.uint8))
	new_grid = np.array(grid);
	new_grid = new_grid.reshape( (dim[0], dim[1], base.shape[0], base.shape[1], base.shape[2]) )
	# 3. UNIR
	return np.vstack( [ np.hstack(row[:]) for row in new_grid] )

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()	# current frame

	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blur_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)
	edge_frame = cv2.Canny(blur_frame, 100, 100)

	cv2.imshow('cam', stacking(frame, (2, 2), [frame, blur_frame, edge_frame, gray_frame]))

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

''' close webcam and windows '''
cap.release()
cv2.destroyAllWindows()
