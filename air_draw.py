"""
Air-Draw
Drawing in the air with Python and OpenCV!
"""

import cv2
import numpy as np

FRAME_WIDTH = 800 #640
FRAME_HEIGHT = 600 #480
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
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


def find_color(img, my_colors):
    """
    Function finds pixels with color from my_colors on image img.
    :param img: image to check for pixels.
    :param my_colors: list of colors for pixels to find.
    :return: list of found pixels.
    """
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    new_points = []
    for color_id, color in enumerate(my_colors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(img_hsv, lower, upper)

        x, y = get_contours(mask)
        if x != 0 and y != 0:
            print(color_id)
            new_points.append([x, y, color_id])
            # cv2.circle(imgResult, (x, y), 15, my_color_values[id], cv2.FILLED)
            cv2.circle(imgResult, (x, y), 15, [255, 255, 255], cv2.FILLED)
            # cv2.imshow(str(color[0]), mask)
    return new_points


def get_contours(img):
    """
    Function gets contours for pixels.
    :param img: Image to analyse.
    :return: None
    """
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


def draw_on_canvas(canvas, my_points, my_color_values):
    """
    Function draws circles on given canvas.
    :param canvas: Canvas to draw on.
    :param my_points: Points to draw.
    :param my_color_values: Colors for points to draw.
    :return: None
    """
    for point in my_points:
        cv2.circle(canvas, (point[0], point[1]), 10, my_color_values[point[2]], cv2.FILLED)


while True:
    success, image = cap.read()
    imgResult = image.copy()
    newPoints = find_color(image, myColors)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        draw_on_canvas(imgResult, myPoints, myColorValues)

    cv2.imshow("Result", cv2.flip(imgResult, flipCode=1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
