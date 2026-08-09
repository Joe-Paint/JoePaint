import glob
from tkinter import Image

import cv2

from brush import *
from contours import *
from coordiante import *
from histogram import *
from mask import *
from statistics import *
from knobs import *

#===========================================================
def getMask():
    if brushColor == Color.BLUE:
        return blueMasks[ currentImage ]
    elif brushColor == Color.RED:
        return redMasks[ currentImage ]
    elif brushColor == Color.GREEN:
        return greenMasks[ currentImage ]
    elif brushColor == Color.PURPLE:
        return purpleMasks[ currentImage ]
    else:
        return yellowMasks[ currentImage ]
# ===========================================================
def currentHistogram():
    if brushColor == Color.BLUE:
        return blueHistogram
    elif brushColor == Color.RED:
        return redHistogram
    elif brushColor == Color.GREEN:
        return greenHistogram
    elif brushColor == Color.PURPLE:
        return purpleHistogram
    else:
        return yellowHistogram
# ===========================================================
def currentStatistics():
    if brushColor == Color.BLUE:
        return blueStatistics
    elif brushColor == Color.RED:
        return redStatistics
    elif brushColor == Color.GREEN:
        return greenStatistics
    elif brushColor == Color.PURPLE:
        return purpleStatistics
    else:
        return yellowStatistics
# ===========================================================
def wipeMasks( masks ):
    for mask in masks:
        mask.fill(0)
# ===========================================================
def wipeAllMasks():
    wipeMasks( blueMasks   )
    wipeMasks( redMasks    )
    wipeMasks( greenMasks  )
    wipeMasks( purpleMasks )
    wipeMasks( yellowMasks )
# ===========================================================
def computeHistograms():
    global blueHistogram
    global redHistogram
    global greenHistogram
    global purpleHistogram
    global yellowHistogram
    blueHistogram   = computeSpecificColorHistograms( blueMasks, hsvImages   )
    redHistogram    = computeSpecificColorHistograms( redMasks, hsvImages    )
    greenHistogram  = computeSpecificColorHistograms( greenMasks, hsvImages   )
    purpleHistogram = computeSpecificColorHistograms( purpleMasks, hsvImages   )
    yellowHistogram = computeSpecificColorHistograms( yellowMasks, hsvImages )
# ===========================================================
def computeStatistics():
    global blueStatistics
    global redStatistics
    global greenStatistics
    global purpleStatistics
    global yellowStatistics
    blueStatistics.calculate   ( blueHistogram )
    redStatistics.calculate    ( redHistogram )
    greenStatistics.calculate  ( greenHistogram )
    purpleStatistics.calculate ( purpleHistogram )
    yellowStatistics.calculate ( yellowHistogram )
# ===========================================================
def updateScreen():
    #make copy of captured image so that we can modify it
    image = images[ currentImage ].copy()
    hsvImage = hsvImages[ currentImage ].copy()

    #compute masks
    currentMask       = getMask()
    currentBlueMask   = blueMasks  [ currentImage ]
    currentRedMask    = redMasks   [ currentImage ]
    currentGreenMask  = greenMasks [ currentImage ]
    currentPurpleMask = purpleMasks[ currentImage ]
    currentYellowMask = yellowMasks[ currentImage ]

    #remove painted regions
    cv2.subtract( image, currentBlueMask,   image )
    cv2.subtract( image, currentRedMask,    image )
    cv2.subtract( image, currentGreenMask,  image )
    cv2.subtract( image, currentPurpleMask, image )
    cv2.subtract( image, currentYellowMask, image )

    #compute tinted masks
    currentColor        = calculateBrushColor( brushColor   )
    blueColor           = calculateBrushColor( Color.BLUE   )
    redColor            = calculateBrushColor( Color.RED    )
    greenColor          = calculateBrushColor( Color.GREEN  )
    purpleColor         = calculateBrushColor( Color.PURPLE )
    yellowColor         = calculateBrushColor( Color.YELLOW )

    sampledPixels = computeSampledPixels( currentMask, images[ currentImage ].copy() )

    tintedBlueMaskBGR   = tintMask( currentBlueMask,   blueColor    )
    tintedRedMaskBGR    = tintMask( currentRedMask,    redColor     )
    tintedGreenMaskBGR  = tintMask( currentGreenMask,  greenColor   )
    tintedPurpleMaskBGR = tintMask( currentPurpleMask, purpleColor  )
    tintedYellowMaskBGR = tintMask( currentYellowMask, yellowColor  )

    #draw painted regions on top of image
    cv2.add( image, tintedBlueMaskBGR,   image )
    cv2.add( image, tintedRedMaskBGR,    image )
    cv2.add( image, tintedGreenMaskBGR,  image )
    cv2.add( image, tintedPurpleMaskBGR, image )
    cv2.add( image, tintedYellowMaskBGR, image )

    drawText( image, "Capture with Painted Regions", Alignment.CENTER,0 )

    if brushColor != Color.ERASE:
        drawText( sampledPixels, "Sampled " + colorName( brushColor ) + " Pixels", Alignment.CENTER, 0 )

    desiredHeight, desiredWidth, _ = image.shape

    #draw brush
    if lastMousePosition != None:
        options           = BrushOptions()
        options.size      = brushSize
        options.shape     = brushShape
        options.thickness = calculateBrushThickness( mouseDown )

        if lastMousePosition.x < desiredWidth:
            options.center = lastMousePosition
            options.color = calculateBrushColor(brushColor)
            drawBrush(image, options)
        else:
            options.center = Coordinate(lastMousePosition.x - desiredWidth, lastMousePosition.y)
            options.color = calculateBrushColor( Color.ERASE )
            drawBrush(sampledPixels, options)

    histogramImage = drawHistogram( currentHistogram(), currentStatistics(), desiredHeight, brushColor )

    #show image side by side with mask for current color
    row1 = np.hstack( [ image, sampledPixels, histogramImage ] )

    computedMask       = drawMask( hsvImage, currentStatistics(), knobs )
    tintedComputedMask = tintMask( computedMask, currentColor )

    if brushColor != Color.ERASE:
        drawText( tintedComputedMask, "Computed " + colorName(brushColor) + " Mask", Alignment.CENTER, 0)
        drawText( tintedComputedMask, "Noise Removal: " + str( knobs.noiseRemovalSteps ), Alignment.LEFT, desiredHeight - 70 )
        drawText( tintedComputedMask, "N / M", Alignment.RIGHT, desiredHeight - 70)

        drawText( tintedComputedMask, "Fill Holes: " + str( knobs.fillHolesSteps ), Alignment.LEFT, desiredHeight - 40 )
        drawText( tintedComputedMask, "F / G", Alignment.RIGHT, desiredHeight - 40)

    _, row1Width, _ = row1.shape
    maskHeight, maskWidth, _ = tintedComputedMask.shape

    contoursImage = drawContours( images[ currentImage ].copy(), computedMask, knobs.minArea )
    drawText(contoursImage, "Computed Contours", Alignment.CENTER, 0)
    drawText(contoursImage, "Minimum Area: " + str(knobs.minArea), Alignment.LEFT, desiredHeight - 40)
    drawText(contoursImage, "A / S", Alignment.RIGHT, desiredHeight - 40)

    _, contoursWidth, _ = contoursImage.shape
    _, logoWidth, _ = logoImage.shape

    paddingWidth = row1Width - maskWidth - contoursWidth - logoWidth

    paddingWidth1 = np.int32( paddingWidth / 2 )
    paddingWidth2 = paddingWidth - paddingWidth1

    paddingImage1 = np.zeros(( maskHeight, paddingWidth1, 3), dtype="uint8")
    paddingImage2 = np.zeros(( maskHeight, paddingWidth2, 3), dtype="uint8")
    paddingImage1.fill( 255 )
    paddingImage2.fill(255)

    row2 = np.hstack([ tintedComputedMask, contoursImage, paddingImage1, logoImage, paddingImage2])

    painted = np.vstack( [ row1, row2 ] )

    cv2.imshow( windowName, painted )
#===========================================================
def mouseCallback(event, x, y, flags, param):
    global lastMousePosition
    global mouseDown

    lastMousePosition = Coordinate(x, y)

    if event == cv2.EVENT_LBUTTONDOWN:
       mouseDown = True

    elif event == cv2.EVENT_LBUTTONUP:
        mouseDown = False

    if mouseDown:
        # compute masks
        currentBlueMask   = blueMasks   [ currentImage ]
        currentRedMask    = redMasks    [ currentImage ]
        currentGreenMask  = greenMasks  [ currentImage ]
        currentPurpleMask = purpleMasks [ currentImage ]
        currentYellowMask = yellowMasks [ currentImage ]

        white = 255, 255, 255
        black = 0, 0, 0

        options           = BrushOptions()
        options.size      = brushSize
        options.shape     = brushShape
        options.thickness = calculateBrushThickness( mouseDown )

        _, imageWidth, _ = images[ currentImage ].shape

        if lastMousePosition.x < imageWidth:
            options.center = lastMousePosition

            options.color = white if brushColor == Color.BLUE else black
            drawBrush(currentBlueMask, options)

            options.color = white if brushColor == Color.RED else black
            drawBrush(currentRedMask, options)

            options.color = white if brushColor == Color.GREEN else black
            drawBrush(currentGreenMask, options)

            options.color = white if brushColor == Color.PURPLE else black
            drawBrush(currentPurpleMask, options)

            options.color = white if brushColor == Color.YELLOW else black
            drawBrush(currentYellowMask, options)
        else:
            options.center = Coordinate(lastMousePosition.x - imageWidth, lastMousePosition.y)
            options.color = black

            if brushColor == Color.BLUE:
                drawBrush(currentBlueMask, options)
            if brushColor == Color.RED:
                drawBrush(currentRedMask, options)
            if brushColor == Color.GREEN:
                drawBrush(currentGreenMask, options)
            if brushColor == Color.PURPLE:
                drawBrush(currentPurpleMask, options)
            if brushColor == Color.YELLOW:
                drawBrush(currentYellowMask, options)

        computeHistograms()
        computeStatistics()

#    print("mouse position: " +str(x)+", " +str(y))
    updateScreen()

#===========================================================
def loadMasks():
    maskDirectory = directory + "/masks"

    path = Path(maskDirectory)
    if not path.is_dir():
        return

    for index, name in enumerate(imageNames):
        loadMask( redMasks, index, maskDirectory + "/" + name + "_red.png")
        loadMask( greenMasks, index, maskDirectory + "/" + name + "_green.png")
        loadMask( blueMasks, index, maskDirectory + "/" + name + "_blue.png")
        loadMask( purpleMasks, index, maskDirectory + "/" + name + "_purple.png")
        loadMask( yellowMasks, index, maskDirectory + "/" + name + "_yellow.png")
#===========================================================
def loadMask( masks, index, filename ):
    path = Path ( filename )
    if not path.is_file():
        return

    masks[ index ] = cv2.imread( filename )
#===========================================================
def saveMasks():
  maskDirectory = directory + "/masks"

  path = Path( maskDirectory )
  if not path.is_dir():
      path.mkdir()

  for index, name in enumerate( imageNames ):
    saveMask( redMasks[ index ], maskDirectory + "/" + name + "_red.png" )
    saveMask( greenMasks[ index ], maskDirectory + "/" + name + "_green.png" )
    saveMask( blueMasks[ index ], maskDirectory + "/" + name + "_blue.png" )
    saveMask( purpleMasks[ index ], maskDirectory + "/" + name + "_purple.png" )
    saveMask( yellowMasks[ index ], maskDirectory + "/" + name + "_yellow.png" )
# ===========================================================
def saveMask( mask, filename ):
    if np.sum( mask ) == 0:
        path = Path( filename )
        if path.is_file():
            path.unlink()
    else:
        cv2.imwrite( filename, mask )

# ===========================================================
windowName="Joe Paint"
directory   = "snapshots"
fileNames   =   glob.glob( directory + '/*.png')

if len( fileNames ) <= 0:
    print( "No snapshots found" )
    exit(1)

imageNames  =   []

images      =   []
hsvImages   =   []

blueMasks   =   []
redMasks    =   []
greenMasks  =   []
purpleMasks =   []
yellowMasks =   []

blueHistogram    = Histogram()
redHistogram     = Histogram()
greenHistogram   = Histogram()
purpleHistogram  = Histogram()
yellowHistogram  = Histogram()

blueStatistics   = ColorChannelsStatistics()
redStatistics    = ColorChannelsStatistics()
greenStatistics  = ColorChannelsStatistics()
purpleStatistics = ColorChannelsStatistics()
yellowStatistics = ColorChannelsStatistics()

logoFilename = "logo.png"
logoImage    = cv2.imread( logoFilename )

for fileName in fileNames:
    imageName = Path( fileName ).stem
    imageNames.append( imageName )

    loadedImage = cv2.imread( fileName )
    hsvImage = cv2.cvtColor(loadedImage, cv2.COLOR_BGR2HSV)
    images.append( loadedImage )
    hsvImages.append( hsvImage )

    height, width, _ = loadedImage.shape
    mask = np.zeros( ( height, width, 3 ), dtype="uint8" )
    blueMasks.append(mask.copy())
    redMasks.append(mask.copy())
    greenMasks.append(mask.copy())
    purpleMasks.append(mask.copy())
    yellowMasks.append(mask.copy())

currentImage      = 0
lastKeyPressed    = None
lastMousePosition = None

brushShape        = BrushShape.CIRCLE
brushColor        = Color.GREEN
brushSize         = 32
mouseDown         = False

knobs = loadKnobs()
loadMasks()
computeHistograms()
computeStatistics()
updateScreen()

updateScreen()
cv2.setMouseCallback(windowName, mouseCallback)

while True:
    keyPressed = cv2.waitKey(1)

    #spacebar change brush shape
    if keyPressed == 32:
        if brushShape == BrushShape.TRIANGLE:
            brushShape = BrushShape.CIRCLE
        else:
            brushShape = BrushShape( np.int32( brushShape.value ) + 1 )
        updateScreen()

    if keyPressed == ord( '=' ):
        brushSize+= 1
        updateScreen()

    if keyPressed == ord( '-' ) and brushSize > 1:
        brushSize-= 1
        updateScreen()

    if keyPressed == ord( 'n' ):
        knobs.noiseRemovalSteps+= 1
        updateScreen()

    if keyPressed == ord('m') and knobs.noiseRemovalSteps > 0:
        knobs.noiseRemovalSteps-= 1
        updateScreen()

    if keyPressed == ord( 'f' ):
        knobs.fillHolesSteps+= 1
        updateScreen()

    if keyPressed == ord('g') and knobs.fillHolesSteps > 0:
        knobs.fillHolesSteps-= 1
        updateScreen()

    if keyPressed == ord( 'a' ):
        knobs.minArea+= 10
        updateScreen()

    if keyPressed == ord('s') and knobs.minArea > 0:
        knobs.minArea-= 10
        updateScreen()

    if keyPressed == ord('r') or keyPressed == 127:
        wipeAllMasks()
        knobs.noiseRemovalSteps = 0
        knobs.fillHolesSteps    = 0
        knobs.minArea           = 0
        computeHistograms()
        computeStatistics()
        updateScreen()

    #change brush color
    if keyPressed == ord( '1' ):
        brushColor = Color.GREEN
        updateScreen()

    elif keyPressed == ord( '2' ):
        brushColor = Color.PURPLE
        updateScreen()

    elif keyPressed == ord( '3' ):
        brushColor = Color.RED
        updateScreen()

    elif keyPressed == ord( '4' ):
        brushColor = Color.BLUE
        updateScreen()

    elif keyPressed == ord( '5' ):
        brushColor = Color.YELLOW
        updateScreen()

    elif keyPressed == ord( '6' ):
        brushColor = Color.ERASE
        updateScreen()

    # Left Arrow or [
    elif keyPressed== 2 or keyPressed == ord( '[' ):
        currentImage -= 1
        if currentImage < 0:
            currentImage = len( images ) - 1
        updateScreen()

    # Right Arrow or ]
    if keyPressed == 3 or keyPressed == ord( ']' ):
        currentImage += 1
        if currentImage == len( images ):
            currentImage = 0
        updateScreen()

    #Escape or Q exits Joe Paint!!!
    if keyPressed == 27 or keyPressed == ord( 'q' ):
        saveKnobs( knobs )
        saveMasks()
        break

    # if keyPressed != lastKeyPressed:
    #     lastKeyPressed = keyPressed
    #     if keyPressed!= 255:
    #         print( keyPressed )
