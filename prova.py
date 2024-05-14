import cv2
import numpy as np
from vanishingPoints import *



vanishing_point_viz_base_path = 'vp/'
goalDirection = 'right'
nomeFile = '82.jpg'

imageForVanishingPoints = cv2.imread(nomeFile)
imageres = cv2.resize(imageForVanishingPoints, (1280, 720))
cv2.imshow('image', imageres)
cv2.imwrite('s.jpg', imageres)
cv2.waitKey(0)

'''
vertical_vanishing_point = get_vertical_vanishing_point(imageForVanishingPoints, goalDirection)
horizontal_vanishing_point = get_horizontal_vanishing_point(imageForVanishingPoints)
cv2.line(imageForVanishingPoints, (int(vertical_vanishing_point[0]) , int(vertical_vanishing_point[1])) , (int(1450),int(710)), (0,255,0) , 2) 
print(int(vertical_vanishing_point[0]) , int(vertical_vanishing_point[1]))
cv2.imwrite(vanishing_point_viz_base_path+nomeFile, imageForVanishingPoints)
'''

print('ciao')