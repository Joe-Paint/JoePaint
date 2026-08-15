import json
from pathlib import Path

#===========================================================
class Calibration:
    def __init__(self):
        self.noiseRemovalSteps = 0
        self.fillHolesSteps    = 0
        self.minArea           = 0
# ===========================================================
def saveCalibration( calibration : Calibration ):
    data = {
        "noiseRemovalSteps": calibration.noiseRemovalSteps,
        "fillHolesSteps": calibration.fillHolesSteps,
        "minArea": calibration.minArea
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