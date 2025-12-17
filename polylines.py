import cv2
import numpy as np

image = np.zeros((400,400,3),dtype=np.uint8)

points = np.array([[100,200],[200,100],[300,200],[250,300],[150,300]],dtype=np.int32)

cv2.polylines(image, [points], isClosed=True, color=(255,0,0),thickness=3)

cv2.imshow("poly", image)
cv2.waitKey(0)
cv2.destroyAllWindows()