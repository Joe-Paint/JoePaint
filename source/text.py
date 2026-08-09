
import cv2
import numpy as np
from enum import Enum

#===========================================================
class Alignment( Enum ):
    CENTER = 1,
    LEFT   = 2,
    RIGHT  = 3,
# ===========================================================
def drawText( image, text, alignment, y ):
    fontFace  = cv2.FONT_HERSHEY_DUPLEX
    scale     = .8
    thickness = 1

    ( textWidth, textHeight ), _ = cv2.getTextSize( text, fontFace, scale, thickness )

    _, imageWidth, _ = image.shape
    margin = 12

    if alignment == Alignment.CENTER:
        textX = np.int32( np.round( imageWidth / 2 - textWidth / 2  ) )
    elif alignment == Alignment.LEFT:
        textX = 0
    else:
        textX = imageWidth - textWidth

    textY = textHeight + margin + y
    color = ( 255, 255, 255 )

    margin = 4
    topLeft     = ( textX - margin,             textY - textHeight - margin )
    bottomRight = ( textX + textWidth + margin, textY + margin )
    black = ( 0, 0, 0 )
    cv2.rectangle(image, topLeft, bottomRight, black, -1)

    cv2.putText( image,
                 text,
                 ( textX, textY ),
                 fontFace,
                 scale,
                 color,
                 thickness,
                 cv2.LINE_AA )
# ===========================================================
def drawTextAt( image, text, x, y ):
    fontFace  = cv2.FONT_HERSHEY_DUPLEX
    scale     = .8
    thickness = 2

    ( textWidth, textHeight ), _ = cv2.getTextSize( text, fontFace, scale, thickness )

    _, imageWidth, _ = image.shape

    textX = x - np.int32( np.round( textWidth  / 2 ) )
    textY = y + np.int32( np.round( textHeight / 2 ) )
    color = ( 255, 255, 255 )

    cv2.putText( image,
                 text,
                 ( textX, textY ),
                 fontFace,
                 scale,
                 color,
                 thickness,
                 cv2.LINE_AA )
# ===========================================================