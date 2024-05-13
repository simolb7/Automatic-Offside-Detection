import cv2
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

# Load the image
image = cv2.imread("/home/simolb/Documents/GitHub/Automatic-Offside-Detection/30.jpg")

imgPitch = isolate_pitch(image)
#cv2.imshow('Pitch', imgPitch)
#resized = cv2.resize(imgPitch, (0,0), fx=0.5, fy=0.5)

# Convert the image to grayscale
gray = cv2.cvtColor(imgPitch, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(blurred, 50, 150)
cv2.imshow('Image edges', edges)
cv2.waitKey(0)

pitch2D = cv2.imread("/home/simolb/Desktop/Universita/AiLab/progetto/world_cup_template.png")
cv2.imshow(pitch2D)
cv2.waitKey(0)
resizedPitch = cv2.resize(pitch2D, (0,0), fx=0.5, fy=0.5)


src_points = [[375,195], [587,262], [952,332], [150,248], [315,290], [568,353], [895,435]]
dst_points = [[962,9], [916,227], [916,383], [820,134], [820,242],[820,374],[820,482]]
pts_src = np.array(src_points)
pts_dst = np.array(dst_points)
h, status = cv2.findHomography(pts_src, pts_dst) 
print(h)

p = [375, 195, 1]

h = [[ 0.3409,  0.0644,  0.4066],
         [ 0.2507,  1.7835, -0.1349],
         [ 0.1683,  1.9608,  1.0000]]

for x in src_points:
    x.append(1)
    matZ = np.matmul(h,x)
    print(round(matZ[0]/matZ[2]), round(matZ[1]/matZ[2]))

# Display the image
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()