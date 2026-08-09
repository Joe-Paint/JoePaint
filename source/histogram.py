import colorsys
import math

from colors import *
from text import *

#===========================================================
class Histogram:
    def __init__( self ):
        self.hueCounts        = []
        self.saturationCounts = []
        self.valueCounts      = []
#===========================================================
def channelSize( channel ):
    # hue
    if channel == 0:
        return 180
    # saturation and value
    else:
        return 255
# ===========================================================
def getCountsForChannel( histogram, channel ):
  if channel == 0:
      return histogram.hueCounts
  elif channel == 1:
      return histogram.saturationCounts
  else:
      return histogram.valueCounts
# ===========================================================
def computeSpecificColorHistograms( masks, hsvImages ):
    histogram = Histogram()
    histogram.hueCounts        = computeSpecificChannelHistograms(0, masks, hsvImages )
    histogram.saturationCounts = computeSpecificChannelHistograms(1, masks, hsvImages )
    histogram.valueCounts      = computeSpecificChannelHistograms(2, masks, hsvImages )
    return histogram
# ===========================================================
def computeSpecificChannelHistograms( channel, masks, hsvImages ):
    size   = channelSize( channel )
    counts = np.zeros( ( size, 1, 1 ) )

    for index, hsvImage in enumerate( hsvImages ):
        colorMask = masks[ index ]
        grayMask  = cv2.cvtColor( colorMask, cv2.COLOR_BGR2GRAY )
        counts    = cv2.calcHist([hsvImage],[channel], grayMask,[size],[0, size], counts,True )

    return counts.flatten()
# ===========================================================
def drawHistogram( histogram, statistics, desiredHeight, brushColor ):
    if brushColor == Color.ERASE:
        return np.zeros( ( desiredHeight, 360, 3 ), dtype="uint8")

    hueImage        = drawHistogramChannel( histogram, statistics.hueStatistics,        0, brushColor )
    saturationImage = drawHistogramChannel( histogram, statistics.saturationStatistics, 1, brushColor )
    valueImage      = drawHistogramChannel( histogram, statistics.valueStatistics,      2, brushColor )

    channelHeight, channelWidth, _ = hueImage.shape
    channelsHeight = channelHeight * 3

    unusedHeight = desiredHeight - channelsHeight
    lowerMargin =  np.int32( np.floor( unusedHeight / 3 ) )

    deadSpace  = np.zeros( ( lowerMargin, channelWidth, 3 ), dtype="uint8" )

    stackedImage    = np.vstack( [ hueImage, deadSpace, saturationImage, deadSpace, valueImage, deadSpace ] )
    stackedHeight, stackedWidth, _ = stackedImage.shape

    y1 = channelHeight
    y2 = channelHeight*2 + lowerMargin
    y3 = channelHeight*3 + lowerMargin*2

    drawText( stackedImage, "Hue",         Alignment.LEFT,     y1 )
    drawText( stackedImage, "Saturation" , Alignment.LEFT,     y2 )
    drawText( stackedImage, "Value",       Alignment.LEFT,     y3 )

    if statistics.hueStatistics.average is not None:
      drawThresholds( stackedImage, statistics.hueStatistics,        0, y1 )
      drawThresholds( stackedImage, statistics.saturationStatistics, 1, y2 )
      drawThresholds( stackedImage, statistics.valueStatistics,      2, y3 )

    drawText( stackedImage, colorName( brushColor) + " Histogram", Alignment.CENTER,0 )

    lostHeight = desiredHeight - stackedHeight
    lostImage  = np.zeros( ( lostHeight, stackedWidth, 3 ), dtype="uint8" )

    return np.vstack( [ stackedImage, lostImage ] )
#===========================================================
def drawThresholds( image, statistics, channel, y ):
    minThreshold = str( round( statistics.minThreshold( channel ) ) )
    maxThreshold = str( round( statistics.maxThreshold( channel ) ) )
    drawText( image, minThreshold + " - " + maxThreshold, Alignment.RIGHT, y)
#===========================================================
def drawHistogramChannel( histogram, statistics, channel, brushColor ):
    histogramHeight = 100
    colorBarHeight  = 9
    width           = 360
    height          = histogramHeight + colorBarHeight
    histogramImage  = np.zeros( ( height, width, 3 ), dtype="uint8" )

    counts    = getCountsForChannel( histogram, channel )

    if sum( counts ) == 0:
        return histogramImage

    normalizedCounts = cv2.normalize( counts, None, 0, histogramHeight, cv2.NORM_MINMAX ).flatten()

    white          = ( 255, 255, 255 )
    meanColor      = (  74,  74, 255 )
    withRangeColor = (   0, 228, 254 )
    y1 = colorBarHeight

    brushBGR =  calculateBrushColor( brushColor )
    brushHSL =  colorsys.rgb_to_hsv( brushBGR[2], brushBGR[1], brushBGR[0] )

    maxValue = channelSize( channel )

    minThreshold = statistics.minThreshold( channel )
    maxThreshold = statistics.maxThreshold( channel )

    for x in range( width ):
        percent = x / ( width - 1 )
        valueF = percent * ( maxValue - 1)

        valueL = np.int32 ( math.floor ( valueF ) )
        valueR = np.int32 ( math.ceil  ( valueF ) )
        countL = normalizedCounts [ valueL ]
        countR = normalizedCounts [ valueR ]

        valuePercent = valueF - valueL
        countF       = countL + valuePercent * ( countR - countL )
        count        = np.int32( np.round ( countF ) )

        distanceFromMean = abs( valueF - statistics.average )
        if distanceFromMean <= 2:
            color = meanColor
        elif statistics.withinRange( valueF, minThreshold, maxThreshold ):
            color = withRangeColor
        else:
            color = white

        y2 = y1 + np.int32( count )
        cv2.line( histogramImage, ( x, y1 ), ( x, y2 ), color )

        #paint color bar
        h = brushHSL[ 0 ]
        s = 1
        v = 1

        if channel == 0:
            h = percent
        elif channel == 1:
            s = percent
        elif channel == 2:
            v = percent

        rgb = colorsys.hsv_to_rgb( h, s, v )
        bgr = ( 255 * rgb[2], 255 * rgb[1], 255 * rgb[0] )
        cv2.line ( histogramImage, ( x, 0 ), ( x, y1-1 ), bgr )

    return np.flipud( histogramImage )
# ===========================================================
