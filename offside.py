import cv2
#coordinate = x, y
side  = "left"
#side = "right"
image = cv2.imread("34.png")
#image = cv2.imread("30.jpg")

#fuoco = [-1371, 27]
fuoco = [2375, -387]

#defender = [[1214, 617], [1202, 748], [741, 588]]
defender = [[334, 560], [556, 426], [750, 350]]
#attacker = [[1297, 627], [808, 618], [803, 580]]
attacker = [[229, 564], [811, 343], [832, 423]]

d = [] 
a_inside = []
a_offside = []

if side == "right":
    for p in defender:
        m = -((p[1] - fuoco[1])/(p[0] - fuoco[0]))
        d.append(m) 
    m_offside = max(d)
    i = d.index(m_offside)
    line = cv2.line(image, defender[i], fuoco, (255,0,0), 1)
    for p in attacker:
        m = -((p[1] - fuoco[1])/(p[0] - fuoco[0]))
        if m > m_offside:
            a_offside.append(tuple(p))
            line = cv2.line(image, p, fuoco, (0,0,255), 1)
        else:
            a_inside.append(tuple(p))
            line = cv2.line(image, p, fuoco, (0,255,0), 1)
else:
    for p in defender:
        m = -((p[1] - fuoco[1])/(p[0] - fuoco[0]))
        d.append(m)
    m_offside = min(d)
    i = d.index(m_offside)
    line = cv2.line(image, defender[i], fuoco, (255,0,0), 1)
    for p in attacker:
        m = -((p[1] - fuoco[1])/(p[0] - fuoco[0]))
        if m < m_offside:
            a_offside.append(tuple(p))
            line = cv2.line(image, p, fuoco, (0,0,255), 1)
        else:
            a_inside.append(tuple(p))
            line = cv2.line(image, p, fuoco, (0,255,0), 1)

print(m_offside)
print(a_offside)
print(a_inside)
cv2.imshow("prova", line)
cv2.waitKey(0)