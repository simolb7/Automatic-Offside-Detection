import offside
import torch
import cv2
import numpy as np

def isolate_pitch(image, point1, point2):
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

    if point2[0] - point1[0] != 0:
        m = (point2[1] - point1[1]) / (point2[0] - point1[0])
    else:
        m = float('inf')  # Linea verticale

    h, w = image.shape[:2]
    # Calcola le intersezioni della linea con i bordi dell'immagine
    x1 = 0
    y1 = int(point1[1] - m * (point1[0] - x1))
    x2 = w - 1
    y2 = int(point1[1] + m * (x2 - point1[0]))
    y3 = 0
    x3 = int(point1[0] - (point1[1] - y3) / m)
    y4 = h - 1
    x4 = int(point1[0] + (y4 - point1[1]) / m)

    cv2.line(mask, (x1, y1), (x2, y2), color=(0,0,0), thickness=2)
    cv2.line(mask, (x3, y3), (x4, y4), color=(0,0,0), thickness=2)

    cv2.imshow("mask", maskOffside)
    cv2.waitKey(0)

    if len(mask.shape) == 3:
     print('porcodio')
     mask = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    
    # Threshold the grayscale image to get only the pitch and lines
    _, threshold = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    # Find contours in the threshold image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour, which should be the pitch
    max_contour = max(contours, key=cv2.contourArea)

    maskOffside = np.zeros_like(image)

    cv2.drawContours(maskOffside, [max_contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    # Create a black mask of the same size as the original image
    
    print(mask.shape)
    print(maskOffside.shape)
    #mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #offside = cv2.bitwise_and(mask, maskOffside)



        #cv2.line(mask, (int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])), (255,255,255), thickness=2)
    cv2.imshow("mask", maskOffside)
    cv2.waitKey(0)
    # Bitwise-AND the mask and the original image
    #pitch = cv2.bitwise_and(image, mask)
    #cv2.imshow("maskd", pitch)
    #cv2.waitKey(0)
    return pitch


homography = torch.tensor([[[ 0.2940,  0.0238, -0.3597],
            [-0.2042,  1.1472,  0.1179],
            [ 0.0560,  0.9439,  1.0000]]])

pitch2D = cv2.imread("model/sportsfield_release/data/world_cup_template.png")
image = cv2.imread("samples/363.jpg")
p1_3D = [2200.4927825927734, 231.54536247253418] 
p2_3D = [-59.255828857421875, 1275.4373359680176]
image = cv2.line(image, (int(p1_3D[0]), int(p1_3D[1])), (int(p2_3D[0]), int(p2_3D[1])), (0, 255, 255), 3)
pitch = isolate_pitch(image, p1_3D, p2_3D)


cv2.waitKey(0)
#offside.drawShadowPitch(image, pitch2D, homography)