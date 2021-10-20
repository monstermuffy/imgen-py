from PIL import Image
from pathlib import Path
import os
from random import randrange
import numpy
import datetime


numEachFruit = 10   # number of each fruit
numFruits = 4
dnarray = []

def getProperties(fruit): # return an array of the properties for each fruit, len(getProperties) for number of properties
    tempProp = []
    for filename in os.listdir(Path(fruit)):
        f = os.path.join(Path(fruit), filename)
        if os.path.isdir(f):
            tempProp.append(f.split("_")[1])
    return tempProp


def pickRandomAsset(rarityArray):                   # iterate over the rarity array to choose a random asset
    totalArray = 0                                  # totalArray holds the value of all the numbers in the array together
    for i in rarityArray:
        totalArray = totalArray + int(i)
    randNum = randrange(totalArray)
    x = 0
    while(randNum > 0):
        randNum = randNum - int(rarityArray[x])
        if randNum > 0:
            x += 1
    return x


def createDna(fruit, fruitNum):
    tempDNA = [fruitNum]
    properties = getProperties(fruit)
    for i in range(len(properties)):                                # iterate over each property to pick a random one for each
        rarityArray = getRarityArray(properties[i], fruit)
        randAss = pickRandomAsset(rarityArray)
        tempDNA.append(randAss)
    if(tempDNA in dnarray):
        createDna(fruit, fruitNum)                                    # dna was already in array, to stop duplicate just try again, causes infinite loop if not enough assets
    else:
        dnarray.append(tempDNA)


def getRarityArray(prop, fruit):                                    # return an array of the rarity values given a an asset
    tempRarityArray = list()
    for filename in os.listdir(Path(fruit + "\\" + fruit.split('\\')[1] + "_" + prop)):
        temp = filename.split("#")[1].split(".")[0]
        tempRarityArray.append(temp)
    return tempRarityArray

def startCreating():
    counter = 0
    fruitCounter = []
    fruitStopper = []
    for i in range(numFruits):
        fruitCounter.append(0)
        fruitStopper.append(numEachFruit)
    while numpy.array_equal(fruitCounter, fruitStopper) == False:
        randNum = randrange(numFruits)
        if(fruitCounter[randNum] != numEachFruit):
            fruitCounter[randNum] += 1
            counter += 1
            createDna('assets\\' + os.listdir(Path('./assets'))[randNum], randNum)    

startCreating()

def cleanImageFolder():
    for f in os.listdir(Path('./images')):
        if not f.endswith(".png"):
            continue
        os.remove(os.path.join(Path('./images'), f))

def createFruit():
    cleanImageFolder()
    edition = 1
    for dna in dnarray:
        tempDNA = dna
        base = Image
        tempImg = Image
        for i in range(1, len(tempDNA)):
            pathTo = Path('./assets/' + (os.listdir(Path('./assets'))[tempDNA[0]]))
            pathTo = os.path.join(pathTo, Path(os.listdir(pathTo)[i-1]))
            pathTo = os.path.join(pathTo, os.listdir(pathTo)[tempDNA[i]])
            if i == 1:
                base = Image.open(Path(pathTo)).convert("RGBA")
                base = base.resize((2000, 2000), resample=Image.NEAREST)

            else:
                tempImg = Image.open(Path(pathTo)).convert("RGBA")
                x, y = tempImg.size
                base.paste(tempImg, (0, 0, x, y), tempImg)
        base.save(Path('./images/Fruity Booty #'+ str(edition) + '.png'), "PNG")
        edition += 1
        print("creating fruity booty #" + str(edition - 1))

timeStart = datetime.datetime.now()
createFruit()
timeEnd = datetime.datetime.now()

timeTaken = timeEnd-timeStart
print(timeTaken*300)