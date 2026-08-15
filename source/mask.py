
import cv2
import numpy as np

# ===========================================================
def drawMask( hueImage, statistics, calibration ):
    if statistics.hueStatistics.average == None:
        height, width, _ = hueImage.shape

        return np.zeros( ( height, width, 3 ), np.uint8 )

    darkColor = np.array( [ statistics.hueStatistics.minThreshold        ( 0 ),
                            statistics.saturationStatistics.minThreshold ( 1 ),
                            statistics.valueStatistics.minThreshold      ( 2 ) ] )

    lightColor = np.array([statistics.hueStatistics.maxThreshold (0),
                          statistics.saturationStatistics.maxThreshold(1),
                          statistics.valueStatistics.maxThreshold(2)])


    if darkColor[0] > lightColor[0]:
        darkColor1    = darkColor.copy()
        darkColor1[0] = 0
        lightColor1   = lightColor

        darkColor2     = darkColor
        lightColor2    = lightColor.copy()
        lightColor2[0] = 180

        maskGray1 = cv2.inRange(hueImage, darkColor1, lightColor1)
        maskGray2 = cv2.inRange(hueImage, darkColor2, lightColor2)
        maskGray  = maskGray1 + maskGray2
    else:
        maskGray = cv2.inRange(hueImage, darkColor, lightColor)

    # remove noise
    maskGray = cv2.erode( maskGray,  None, iterations = calibration.noiseRemovalSteps )
    maskGray = cv2.dilate( maskGray, None, iterations = calibration.noiseRemovalSteps )

    #Fill holes
    maskGray = cv2.dilate(maskGray, None, iterations = calibration.fillHolesSteps )
    maskGray = cv2.erode(maskGray, None, iterations = calibration.fillHolesSteps )

    maskColor = cv2.cvtColor( maskGray, cv2.COLOR_GRAY2BGR )

    return maskColor
# ===========================================================
def tintMask( mask, color ):
  percentages = color[ 0 ] / 255, color[ 1 ] / 255, color[ 2 ] / 255
  return cv2.multiply( mask, percentages )
# ===========================================================
def computeSampledPixels( mask, image ):
    return cv2.bitwise_and( image, mask )
# ===========================================================
