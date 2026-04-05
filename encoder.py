from drawing import generateStrip
from random import choice, randint

tileCodes = {
    "?"     : 63,
    "-"     : 35,
    "#"     : 45,
    "UP"    : 94,
    "DOWN"  : 118,
    "RIGHT" : 62,
    "LEFT"  : 60,
}

allowedChars = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","?","#","-"]

# letter codes are their ASCII codes
# number codes = number % 10 + 48


#---------# get data to turn into puzzle
tileData = ""
modifiers = ""

mode = input("Enter the mode of data generation: (r = random, t = text, a = ASCII code)\n> ").lower()

rows = 10
cols = 10

if mode == "t":
#---------# collect user inputs
    modifiers = input("Enter the modifiers for the puzzle. Modifiers should be separated by spaces.\
                     \nIf the level uses clouds, type c.\
                     \nIf the level uses arrows, type a.\
                     \n> ").lower()
    tileData = input("Enter the tile data as letters for the puzzle. Tiles should be separated by spaces.\
                     \nIf a block has ice, write it in this form <iced{number of ice}{letter}>.\
                     \nArrow tiles are represented by typing up, down, left, or right.\
                     \nIf a tile is blank, type -, if a tile is empty, type #.\
                     \n> ").upper()

elif mode == "a":
    modifiers = input("Enter the modifiers for the puzzle. Modifiers should be separated by spaces.\
                     \nIf the level uses clouds, type c.\
                     \nIf the level uses arrows, type a.\
                     \n> ").lower()
    tileData = input("Enter the tile data as ASCII codes for the puzzle. Tiles should be separated by spaces.\
                     \nIf a block has ice, write it in this form <iced{number of ice}{ASCII code}>.\
                     \nArrow tiles are represented by typing up, down, left, or right.\
                     \nIf a tile is blank, type -, if a tile is empty, type #.\
                     \n> ").upper()
    rows = int(input("Enter the number of rows you want in the puzzle.\
                     \n> "))
    if rows < 10:
        rows = 10
    cols = int(input("Enter the number of columns you want in the puzzle.\
                     \n> "))
    if cols < 10:
        cols = 10

elif mode == "r":
#---------# choose a modifier combination
    print("Randomising modifiers...")
    modifiers = choice(["", "c", "a", "c a"])
    print(f"Chosen modifiers: <{modifiers}>")

#---------# choose a character from allowed characters to fill entire grid
    print("Randomising tile data...")
    if "a" in modifiers:
        allowedChars.extend(["UP","DOWN","RIGHT","LEFT"])
    for _ in range(100):
        # check if tile is iced (isIced = 0)
        isIced = randint(0, len(allowedChars)+1)
        icedLevel = randint(0,9)

        # if is iced, add ice tile prefix
        if isIced == 0:
            tileData += f"ICED{icedLevel}"

        tileData += f"{choice(allowedChars)} "
    
    tileData = tileData[:len(tileData) - 1]
    print(f"Randomised tile data: <{tileData}>")

else:
    print("Invalid input. Exiting program...")
    exit()

#---------# convert data to LOK data
puzzleData = []
tiles = []
if tileData != "":
    tiles = tileData.split(" ")

print(tiles)

#---# split data into length <cols> chunks
chunks = []

for i in range(rows):
    chunk = []

#---------# if all data has run out, fill the rest of the chunks with emtpies
    if len(tiles) == 0:
        chunk = ["-" for _ in range(cols)]
        chunks.append(chunk)
        continue

#---------# loop through the given data until it runs out, splitting into <cols> item long chunks for each row of tiles and delete used data
    for item in tiles:
        print(item)
        chunk.append(item)

        if len(chunk) == cols:
            del tiles[:cols]
            break

#---------# if there were not enough items for the current chunk to be 10 items long, pad with empties and delete remaining data
    if len(chunk) < cols:
        chunk.extend(["#" for _ in range(cols - len(tiles))])
        del tiles[:len(tiles)]

    print(tiles)

    chunks.append(chunk)

print(chunks)

for chunk in chunks:
    to_add = [10]

    for tile in chunk:
        iced = False
        special = False
        
        print(f"<{tile}>")

#---------# check if the current tile has ice
        print(f"Checking if tile <{tile}> is an iced tile.")
        if "ICED" in tile:
            iced = True
            print(f"The tile <{tile}> is an iced tile.")
        else: 
            print(f"The tile <{tile}> is not an iced tile.")

        iceNum = []
        if iced:
            iceNum = [ord(tile[4])]
            tile = tile[5:]
        
#---------# convert to bytes if ascii code was given
        if mode == "a" and tile not in allowedChars:
            to_add.extend([tile.encode("utf-8")])
            to_add.extend(iceNum)
            print(to_add)
            continue

#---------# check if the current tile is not a letter
        print(f"Checking if tile <{tile}> is a special character.")
        try:
            to_add.extend([tileCodes[tile]])
            print(f"The tile <{tile}> is a special character.")
            
        except KeyError:
            to_add.extend([ord(tile)])
            print(f"The tile <{tile}> is not a special character.") 
        
        to_add.extend(iceNum)

        print(to_add)

    puzzleData.extend(to_add)

print(puzzleData)

#---------# append modifiers to puzzle data as suffix
suffix = ["10", "36", "48", "48", "49"]

for toggle in modifiers.split(" "):
    if toggle == "a":
        suffix[2] = "49"
    elif toggle == "c":
        suffix[3] = "49"

puzzleData.extend(suffix)

#---------# append header data containing dimensions and length to puzzle data as prefix
rowsDigits = str(rows)
colsDigits = str(cols)
prefix = [0, 0, 0, 0, ord(rowsDigits[0]), ord(rowsDigits[1]), 10, ord(colsDigits[0]), ord(colsDigits[1])]

prefix.extend(puzzleData)
print(len(prefix))
prefix[3] = len(prefix)
puzzleData = prefix

#---# calculate height required to fit data in one puzzle strip
#---# using ceiling division
height = (len(puzzleData) + 64 - 1) // 64
print(height)

#---------# use drawing lib to convert to a LOK data strip
generateStrip(puzzleData, height)
print("The input has been converted to a LOK Digital Puzzle Strip successfully.")

