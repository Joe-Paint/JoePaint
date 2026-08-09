import json
from pathlib import Path

#===========================================================
class Knobs:
    def __init__(self):
        self.noiseRemovalSteps = 0
        self.fillHolesSteps    = 0
        self.minArea           = 0
# ===========================================================
def saveKnobs( knobs : Knobs ):
    data = {
        "noiseRemovalSteps": knobs.noiseRemovalSteps,
        "fillHolesSteps": knobs.fillHolesSteps,
        "minArea": knobs.minArea
    }

    with open("joePaintKnobs.json", "w") as file:
        json.dump( data, file, indent = 4 )

# ===========================================================
def loadKnobs() -> Knobs:
    knobs = Knobs()

    filename = "joePaintKnobs.json"
    path = Path( filename )
    if not path.is_file():
        return knobs

    with open(filename, "r") as file:
        data = json.load( file )

        if "noiseRemovalSteps" in data:
            knobs.noiseRemovalSteps = data[ "noiseRemovalSteps"]

        if "fillHolesSteps" in data:
            knobs.fillHolesSteps = data[ "fillHolesSteps"]

        if "minArea" in data:
            knobs.minArea = data[ "minArea"]

    return knobs
# ===========================================================