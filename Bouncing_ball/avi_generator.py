import cv2
from os import listdir

n = len(listdir("screenshot"))

img_array = [cv2.imread("screenshot/img_{}.png".format(i)) for i in range(1, n+1)]

h, w, s = img_array[0].shape
out = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc(*'DIVX'), 60, (w, h))

for img in img_array: out.write(img)
out.release()