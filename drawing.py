from PIL import Image
import numpy as np

# assigning constants for the strip
def generateStrip(data, height = 1):
    """This function generates a data strip image for the given LOK puzzle data.

    Args:
        data (array): The LOK puzzle data to be converted to a data strip
        height (int, optional): The height required to fit the LOK puzzle data into a 64 by n data strip. Defaults to 1.
    """
    #---------# append the given data to the puzzle data list
    puzzleData = data

    #---------# pad the list until the length is a multiple of 64
    requiredPadding = 64 - (len(puzzleData) % 64)

    print(requiredPadding)

    #---# check if padding is required
    if requiredPadding != 0:
        puzzleData.extend([0 for _ in range(requiredPadding)])

    print(puzzleData)

    #---------# create numpy array from data with shape 64 by `height`
    dataArray = np.zeros((height, 64, 3), dtype=np.uint8)
    print(dataArray.shape)

    #---# mapping puzzle data onto array in correct format
    #---# PIL formats image from top left to bottom right
    #---# but data formatted from bottom left to top right
    #---# so data must be chunked and indexed at the correct location
    #---# chunk 0 = last 64 indexes

    idx = 0
    chunk = 0

    for item in puzzleData:
        if chunk == height:
            break
        print(f"item <{item}> at chunk <{chunk}>")

        # sets the pixel at position x,y = (idx, height - 1 - chunk) to item
        dataArray[(height - 1 - chunk), idx] = [item, item, item]

        idx += 1
        # loop index when reaching end of strip length
        if idx % 64 == 0:
            chunk += 1
            idx = 0

    # dataArray = np.reshape(dataArray, (height, 64) )
    print(dataArray.shape)
    print(dataArray)

    #---------# create data strip for the puzzle data
    dataStrip = Image.fromarray(dataArray, "RGB")
    dataStrip = dataStrip.resize((dataStrip.width * 3, dataStrip.height * 3), Image.NEAREST)

    #---------# overlay data strip on another image to create a custom level
    #---# create background and white border of strip
    background = Image.new("RGB", (512,512), (50, 50, 50))
    border = Image.new("RGB", (3 * 64 + 2 , 3 * height + 2), (255, 255, 255))

    #---# overlay images on background
    background.paste(border, (4, 498))
    background.paste(dataStrip, (5, 499))

    #---# save image
    background.save("./LOK puzzle maker/puzzle.png")


if __name__ == "__main__":
    print("This is the <drawing.py> file!")