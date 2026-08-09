from enum import Enum

#===========================================================
class Color( Enum ):
   BLUE   = 1,
   RED    = 2,
   GREEN  = 3,
   PURPLE = 4,
   YELLOW = 5,
   ERASE  = 6,
# ===========================================================
def calculateBrushColor( color ):
    if color == Color.BLUE:
        return 255, 0, 0
    elif color == Color.RED:
        return 0, 0, 255
    elif color == Color.GREEN:
        return 0, 255, 0
    elif color == Color.PURPLE:
        return 99, 38, 103
    elif color == Color.YELLOW:
        return 0, 255, 255
    else:
        return 255, 255, 255
# ===========================================================
def colorName( color ):
    if color == Color.BLUE:
        return "Blue"
    elif color == Color.RED:
        return "Red"
    elif color == Color.GREEN:
        return "Green"
    elif color == Color.PURPLE:
        return "Purple"
    elif color == Color.YELLOW:
        return "Yellow"
    else:
        return "Erase"
# ===========================================================
