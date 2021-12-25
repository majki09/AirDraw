import cv2
import numpy as np

frameWidth = 800 #640
frameHeight = 600 #480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

# myColors = [[5, 107, 0, 19, 255, 255],
#             [133, 56, 0, 159, 156, 255],
#             [57, 76, 0, 100, 255, 255],
#             [90, 48, 0, 118, 255, 255]]

myColors = [[160, 155, 147, 179, 255, 255],
            [75, 109, 93, 103, 255, 255]]

# majkowe
# myColors = [[160, 155, 147, 179, 255, 255],
#             [75, 109, 93, 103, 255, 255]]

# myColorValues = [[51, 153, 255],  ## BGR
#                  [255, 0, 255],
#                  [0, 255, 0],
#                  [255, 0, 0]]

# majkowe
# myColorValues = [[0, 0, 255],
#                  [255, 0, 0]]

myColorValues = [[0, 0, 255],
                 [255, 0, 0],
                 [255, 255, 0],
                 [0, 255, 0]]

myPoints = []  ## []x , y , colorId ]


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for id, color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)

        x, y = getContours(mask)
        if x != 0 and y != 0:
            print(id)
            newPoints.append([x, y, id])
            # cv2.circle(imgResult, (x, y), 15, myColorValues[id], cv2.FILLED)
            cv2.circle(imgResult, (x, y), 15, [255, 255, 255], cv2.FILLED)
            # cv2.imshow(str(color[0]), mask)
    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    # img_raw = img.copy()
    # imgResult = cv2.flip(img_raw, flipCode=1)
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", cv2.flip(imgResult, flipCode=1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
