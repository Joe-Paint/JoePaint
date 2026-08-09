
import cv2
import numpy as np
from colors import *

#===========================================================
class BrushShape( Enum ):
    CIRCLE    = 1,
    RECTANGLE = 2,
    TRIANGLE  = 3,
#===========================================================
class BrushOptions:
    def __init__( self ):
        self.center    = None
        self.size      = 32
        self.shape     = BrushShape.CIRCLE
        self.color     = Color.BLUE
        self.thickness = 2
#===========================================================
def drawBrush( image, options ):
    if options.shape == BrushShape.RECTANGLE:
        drawRect( image, options )
    elif options.shape == BrushShape.CIRCLE:
        drawCircle( image, options )
    elif options.shape == BrushShape.TRIANGLE:
        drawTriangle( image, options )
#===========================================================
def calculateBrushThickness( mouseDown ):
    if mouseDown:
        return cv2.FILLED
    else:
        return 2
#===========================================================
def drawTriangle( image, options ):
    cursorRatio  =   options.size / 32
    halfHeight   =   np.int32( 15 * cursorRatio )
    halfWidth    =   np.int32( 20 * cursorRatio )

    top   = ( options.center.x ,            options.center.y - halfHeight )
    right = ( options.center.x + halfWidth, options.center.y + halfHeight )
    left  = ( options.center.x - halfWidth, options.center.y + halfHeight )
    cv2.drawContours( image, [np.array([top,right,left])], 0, options.color, options.thickness )
#===========================================================
def drawCircle( image, options ):
    center    = ( options.center.x, options.center.y )
    radius    = np.int32( options.size / 2 )
    cv2.circle( image, center, radius, options.color, options.thickness )
# ===========================================================
def drawRect( image, options ):
    halfSize    = np.int32( options.size / 2 )
    topLeft     = ( options.center.x - halfSize, options.center.y - halfSize )
    bottomRight = ( options.center.x + halfSize, options.center.y + halfSize )
    cv2.rectangle( image, topLeft, bottomRight, options.color, options.thickness )
# ===========================================================