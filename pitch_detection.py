import cv2
import numpy as np

# Use the function

def line_intersection(line1, line2):
    # Linee nel formato [x1, y1, x2, y2]
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # Calcola i denominatori per l'equazione dell'intersezione
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denom == 0:
        # Le linee sono parallele o coincidenti, nessuna intersezione
        return None

    # Calcola le coordinate dell'intersezione
    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

    return x, y

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
image = cv2.imread("31.png")

imgPitch = isolate_pitch(image)
#cv2.imshow("image", imgPitch)
#cv2.waitKey(0)
resized = cv2.resize(imgPitch, (0,0), fx=0.5, fy=0.5)

# Apply Gaussian blur
imgGauss = cv2.GaussianBlur(imgPitch, (3, 3), 0)
cv2.imshow('Image Gauss', imgGauss)
cv2.waitKey(0)

# Convert the image to grayscale
gray = cv2.cvtColor(imgGauss, cv2.COLOR_BGR2GRAY)
cv2.imshow('Image gray', gray)
cv2.waitKey(0)

imgBil = cv2.bilateralFilter(gray, 5, 5, 100)
#imgLapl = cv2.Laplacian(gray, cv2.CV_16S, ksize = 3)
blurred = cv2.convertScaleAbs(imgBil)
#blurred = cv2.bitwise_not(imgLapl)
cv2.imshow('Image blurred', blurred)
cv2.waitKey(0)

#
#blurred = cv2.fastNlMeansDenoising(gray, None, 10, 10, 7, 21)
#ddepth = cv2.CV_8U
#kernel_size = 3
#blurred2 = cv2.Laplacian(blurred, ddepth, ksize = kernel_size)

# Use Canny edge detection
edges = cv2.Canny(blurred, 50, 150, L2gradient = True)
cv2.imshow('Image edges', edges)
cv2.waitKey(0)

pitch2D = cv2.imread("pitch2D.png")
resizedPitch = cv2.resize(pitch2D, (0,0), fx=0.5, fy=0.5)

linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 150, None, 40, 10)

list = [linesP[i][0].tolist() for i in range(0, len(linesP))]
print(list)
l = set()

if linesP is not None:
    for i in range(0, len(list)-1):
        l1 = list[i]
        for j in range(i+1, len(list)):
            l2 = list[j]
            if abs((l2[3]-l2[1])/(l2[2]-l2[1])) == abs((l1[3]-l1[1])/(l1[2]-l1[1])):
                l.add(tuple(l2))
        #cv2.line(image, (l1[0], l1[1]), (l1[2], l1[3]), (0,0,255), 3, cv2.LINE_AA)

for line in l:
    l3 = [t for t in line]
    list.remove(l3)

for i in range(0, len(list)):
    l1 = list[i]
    cv2.line(image, (l1[0], l1[1]), (l1[2], l1[3]), (0,0,255), 3, cv2.LINE_AA)
#l = linesP[0][0]
#cv2.circle(image, (l[0], l[1]), 10, (255, 255, 0), -1)

src_points = [[375,195], [587,262], [952,332], [150,248], [315,290], [568,353], [895,435]]
dst_points = [[962,9], [916,227], [916,383], [820,134], [820,242],[820,374],[820,482]]
pts_src = np.array(src_points)
pts_dst = np.array(dst_points)
h, status = cv2.findHomography(pts_src, pts_dst) 
print(h)

p = [375, 195, 1]

for x in src_points:
    x.append(1)
    matZ = np.matmul(h,x)
    print(round(matZ[0]/matZ[2]), round(matZ[1]/matZ[2]))

# Display the image
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()