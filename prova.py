import cv2
import numpy as np
'''
def isolate_pitch(image):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([30, 50, 50])
    upper_green = np.array([85, 255, 255])

    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask_green)

    # Convert the result to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to get only the pitch and lines
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours in the threshold image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour, which should be the pitch
    max_contour = max(contours, key=cv2.contourArea)

    # Create a black mask of the same size as the original image
    mask = np.zeros_like(image)

    # Draw the largest contour (the pitch) on the mask
    cv2.drawContours(mask, [max_contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    # Bitwise-AND the mask and the original image
    pitch = cv2.bitwise_and(image, mask)

    return pitch

image = cv2.imread("31.png")

imgPitch = isolate_pitch(image)

w = len(image[0])
h = len(image)
n = 60

for y in range(0, h - n, n):
    for x in range(0*16, w - n, n):
        window = np.array([imgPitch[y+m][x:x+n] for m in range(n)])
        imgGauss = cv2.GaussianBlur(window, (5, 5), 0)
        gray = cv2.cvtColor(imgGauss, cv2.COLOR_BGR2GRAY)
        imgBil = cv2.bilateralFilter(gray, 5, 5, 100)
        blurred = cv2.convertScaleAbs(imgBil)
        edges = cv2.Canny(blurred, 50, 150, L2gradient = True)
        linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 150, None, 40, 10)
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                cv2.line(window, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
            cv2.imshow("finestra", edges)
            cv2.waitKey(0)
        cv2.rectangle(imgPitch, (x, y), (x+n, y+n), (0, 0, 255), 1)
        #break
    #break


cv2.imshow('Image', imgPitch)
cv2.waitKey(0)
'''
from vanishingPoints import *

vanishing_point_viz_base_path = 'vp/'
goalDirection = 'left'
nomeFile = '34.png'

imageForVanishingPoints = cv2.imread(nomeFile)
#imageForVanishingPoints = cv2.flip(imageForVanishingPoints, 1)
print(imageForVanishingPoints.shape[:2])
vertical_vanishing_point = get_vertical_vanishing_point(imageForVanishingPoints, goalDirection)
horizontal_vanishing_point = get_horizontal_vanishing_point(imageForVanishingPoints)
cv2.line(imageForVanishingPoints, (int(vertical_vanishing_point[0]) , int(vertical_vanishing_point[1])) , (int(1450),int(710)), (0,255,0) , 2) 
print((int(vertical_vanishing_point[0]) , int(vertical_vanishing_point[1])))
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
