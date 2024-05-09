import cv2
import numpy as np
from vanishingPoints import *



vanishing_point_viz_base_path = 'vp/'
goalDirection = 'right'


imageForVanishingPoints = cv2.imread('30.jpg')
vertical_vanishing_point = get_vertical_vanishing_point(imageForVanishingPoints, goalDirection)
horizontal_vanishing_point = get_horizontal_vanishing_point(imageForVanishingPoints)
cv2.imwrite(vanishing_point_viz_base_path+'30.jpg', imageForVanishingPoints)

