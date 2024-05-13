import cv2
from matplotlib import pyplot as plt
import numpy as np

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

image = cv2.imread("/home/simolb/Desktop/Universita/AiLab/progetto/1_4k.png")

imgPitch = isolate_pitch(image)

gray = cv2.cvtColor(imgPitch, cv2.COLOR_BGR2GRAY)

canny = cv2.Canny(gray, 50, 150, L2gradient=True)

# Rilevamento dei contorni o dei punti di interesse
corners = cv2.goodFeaturesToTrack(canny, 8, 0.01, 10) # Esempio: Rilevamento degli angoli di Shi-Tomasi

# Selezione dei punti di riferimento
corners = np.intp(corners)
 
for i in corners:
 x,y = i.ravel()
 cv2.circle(imgPitch,(x,y),3,255,-1)
 
plt.imshow(imgPitch)
plt.show()

