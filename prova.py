import cv2
import numpy as np
from vanishingPoints import *



vanishing_point_viz_base_path = 'vp/'
goalDirection = 'right'
nomeFile = '479.jpg'

imageForVanishingPoints = cv2.imread(nomeFile)
print(imageForVanishingPoints.shape[:2])
vertical_vanishing_point = get_vertical_vanishing_point(imageForVanishingPoints, goalDirection)
horizontal_vanishing_point = get_horizontal_vanishing_point(imageForVanishingPoints)
cv2.line(imageForVanishingPoints, (int(vertical_vanishing_point[0]) , int(vertical_vanishing_point[1])) , (int(1450),int(710)), (0,255,0) , 2) 
cv2.imwrite(vanishing_point_viz_base_path+nomeFile, imageForVanishingPoints)

def calculate_x_coordinate(van, point, targetx):
    # Coordonate del punto di convergenza (punto di fuga)
    x1,y1 = van[:2]
    x2,y2 = point[:2]
    return round(((-x1/(x2-x1))*(y2-y1))+y1)

# Example usage:
y_coordinate = calculate_x_coordinate((vertical_vanishing_point[0], vertical_vanishing_point[1]), (1450, 710), 0)
print(y_coordinate)
cv2.line(imageForVanishingPoints, (1450,710) , (0, y_coordinate), (0,255,255) , 2)
cv2.imwrite(vanishing_point_viz_base_path+nomeFile, imageForVanishingPoints)



'''
def rectify_vertical_lines(image, vertical_lines):
    # Estrai i punti delle linee verticali
    src_points = np.array(vertical_lines, dtype=np.float32)
    
    # Definisci i punti di destinazione rettificati
    dst_points = np.array([[0, 0], [image.shape[1], 0], [0, image.shape[0]], [image.shape[1], image.shape[0]]], dtype=np.float32)

    # Calcola la matrice di omografia
    H, _ = cv2.findHomography(src_points, dst_points)

    # Applica la trasformazione di omografia
    rectified_image = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))

    return rectified_image

# Esempio di utilizzo
# Leggi l'immagine e individua le linee verticali
vertical_lines = [[x1, y1], [x2, y2], ...]  # Lista dei punti delle linee verticali

# Rettifica le linee verticali
rectified_image = rectify_vertical_lines(imageForVanishingPoints, vertical_lines)
'''