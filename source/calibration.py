import json
import numpy as np
from pathlib import Path

#===========================================================
class Calibration:
    def __init__(self):
        self.noiseRemovalSteps = 0
        self.fillHolesSteps    = 0
        self.minArea           = 0
        self.minBlue   = np.array( [ 0, 0, 0 ] )
        self.maxBlue   = np.array( [ 0, 0, 0 ] )
        self.minRed    = np.array( [ 0, 0, 0 ] )
        self.maxRed    = np.array( [ 0, 0, 0 ] )
        self.minGreen  = np.array( [ 0, 0, 0 ] )
        self.maxGreen  = np.array( [ 0, 0, 0 ] )
        self.minPurple = np.array( [ 0, 0, 0 ] )
        self.maxPurple = np.array( [ 0, 0, 0 ] )
        self.minYellow = np.array( [ 0, 0, 0 ] )
        self.maxYellow = np.array( [ 0, 0, 0 ] )

# ===========================================================
def saveCalibration( calibration : Calibration ):
    data = {
        "noiseRemovalSteps": calibration.noiseRemovalSteps,
        "fillHolesSteps": calibration.fillHolesSteps,
        "minArea": calibration.minArea,
        "minBlue": calibration.minBlue.tolist(),
        "maxBlue": calibration.maxBlue.tolist(),
        "minRed": calibration.minRed.tolist(),
        "maxRed": calibration.maxRed.tolist(),
        "minGreen": calibration.minGreen.tolist(),
        "maxGreen": calibration.maxGreen.tolist(),
        "minPurple": calibration.minPurple.tolist(),
        "maxPurple": calibration.maxPurple.tolist(),
        "minYellow": calibration.minYellow.tolist(),
        "maxYellow": calibration.maxYellow.tolist()
    }

    with open("calibration.json", "w") as file:
        json.dump( data, file, indent = 4 )

# ===========================================================
def loadCalibration() -> Calibration:
    calibration = Calibration()
    filename = "calibration.json"
    path = Path( filename )
    if not path.is_file():
        return calibration

    with open(filename, "r") as file:
        data = json.load( file )

        if "noiseRemovalSteps" in data:
            calibration.noiseRemovalSteps = data[ "noiseRemovalSteps"]

        if "fillHolesSteps" in data:
            calibration.fillHolesSteps = data[ "fillHolesSteps"]

        if "minArea" in data:
            calibration.minArea = data[ "minArea"]

    return calibration
# ===========================================================