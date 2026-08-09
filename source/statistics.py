import math

import numpy as np
from astropy.stats import circmean
from astropy.stats import circstd

#===========================================================
class Statistics:
    def __init__( self ):
        self.average           = None
        self.standardDeviation = None

    def minThreshold( self, channel ):
        value = self.average - 2 * self.standardDeviation
        if value >= 0:
            return value
        elif channel == 0:
            return value + 180
        else:
            return 0

    def maxThreshold(self, channel):
        value = self.average + 2 * self.standardDeviation

        size = 180 if channel == 0 else 256

        if value < size:
            return value
        elif channel == 0:
            return value - 180
        else:
            return size - 1

    def withinRange( self, value, min, max ):
        if min > max:
            return value >= min or value <= max
        else:
            return min <= value <= max

    def resetVariables( self ):
        self.average = None
        self.standardDeviation = None

    def calculateCircularMean( self, counts ):
        if sum( counts ) == 0:
            self.resetVariables()
            return

        valuesInDegrees = []
        for hue, count in enumerate( counts ):
            degrees = 2 * hue
            valuesInDegrees = valuesInDegrees + [ degrees ] * np.int32( np.round( count ) )

        valueInRadians = np.deg2rad( valuesInDegrees )

        meanRadians = circmean( valueInRadians )
        stdRadians  = circstd ( valueInRadians )

        # check if mean is less than 0 and if so
        # add 2 pi to make it fall in the range [ 0, 2 pi ]
        twoPi = 2 * math.pi
        while meanRadians < 0:
            meanRadians += twoPi

        if meanRadians >= twoPi:
            meanRadians = meanRadians % twoPi

        meanInDegrees = np.rad2deg( meanRadians )
        stdDegrees = np.rad2deg( stdRadians )

        self.average           = meanInDegrees / 2
        self.standardDeviation = stdDegrees / 2

    def calculateArthimeticMean( self, counts ):
        if sum( counts ) == 0:
            self.resetVariables()
            return

        size = len(counts)

        values                 = np.arange( 0, size, 1 )
        self.average           = np.average( values, weights = counts )
        pixelVariance          = np.average( ( values - self.average ) ** 2, weights=counts )
        self.standardDeviation = np.sqrt( pixelVariance )
#===========================================================
class ColorChannelsStatistics:
    def __init__(self ):
        self.hueStatistics        = Statistics()
        self.saturationStatistics = Statistics()
        self.valueStatistics      = Statistics()

    def calculate( self, histogram ):
        self.hueStatistics.calculateCircularMean( histogram.hueCounts )
        self.saturationStatistics.calculateArthimeticMean( histogram.saturationCounts )
        self.valueStatistics.calculateArthimeticMean( histogram.valueCounts )
#===========================================================
