import cv2
#coordinate = x, y
side  = "left"
image = cv2.imread("34.png")

#fuoco = [-1371, 27]
fuoco = [2375, -387]

#defender = [[1214, 617], [1202, 748], [741, 588]]
defender = [[334, 560], [556, 426], [750, 350]]

if side == "right":
    l = [] 
    for p in defender:
        m = -((p[1] - fuoco[1])/(p[0] - fuoco[0]))
        l.append(m)
        line = cv2.line(image, p, fuoco, (255,0,0), 3)
    m_offside = max(l)
else:
    l = []
    for p in defender:
        m = -((p[1] - fuoco[1])/(p[0] - fuoco[0]))
        l.append(m)
        line = cv2.line(image, p, fuoco, (255,0,0), 3)
    m_offside = min(l)

print(m_offside)
cv2.imshow("prova", line)
cv2.waitKey(0)