
import cv2
from colors import *
from text import *

# ===========================================================
def drawContours( image, colorMask, minArea ):
    grayMask = cv2.cvtColor( colorMask, cv2.COLOR_BGR2GRAY )
    contours, _ = cv2.findContours( grayMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

    contoursImage = image.copy()

    # color = randomColor()
    color = ( 204, 74, 255 )

    number = 1
    for contour in contours:
        area = cv2.contourArea( contour )

        #ignore contours that are too small
        if area < minArea:
            continue

        cv2.drawContours( contoursImage, [ contour ], -1, color, 3)

        M = cv2.moments( contour )
        if M['m00'] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            drawTextAt( contoursImage, str( number ), cX, cY)

        number+=1

    return contoursImage
# ===========================================================
