from PIL import Image
from pathlib import Path
import os
from random import randrange
import numpy
import datetime
import json

# cumquat was here

numEachFruit = 5   # number of each fruit test
numFruits = 6
dnarray = []
unrevealedIPFSlink = "ipfs://Qmefk8tH36QXoBNSGGAxoc8EtfPC122TH4Xa2zTVaoUbgr"

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

def cleanMetadataFolder():
    for f in os.listdir(Path('./metadata')):
        if not f.endswith(".json"):
            continue
        os.remove(os.path.join(Path('./metadata'), f))

def createMetadata(dna, edition):
    tempDic = []
    dic = {
        "name": ("Fruity Booty #" + str(edition)),
        "image": (unrevealedIPFSlink)
    }
    for i in range(1, len(dna)):
            chosen = ""
            pathTo = Path('./assets/' + (os.listdir(Path('./assets'))[dna[0]]))
            attributeCategory = os.listdir(pathTo)[i-1].split("_")[1]
            pathTo = os.path.join(pathTo, Path(os.listdir(pathTo)[i-1]))
            if i == 1:
                chosenAttribute = (os.listdir(pathTo)[dna[i]]).split("#")[0]
            else:
                chosenAttribute = (os.listdir(pathTo)[dna[i]].split("_")[1]).split("#")[0]
            tempDic2 = {
                "trait_type": attributeCategory,
                "value": chosenAttribute
            }
            tempDic.append(tempDic2)

    dic["attributes"] = tempDic
    with open('metadata/' + str(edition) + '.json', 'w') as f:
        json.dump(dic, f)            

def createFruit():
    cleanImageFolder()
    cleanMetadataFolder()
    edition = 1
    for dna in dnarray:
        createMetadata(dna, edition)
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
                base = Image.alpha_composite(base, tempImg)
            #base.show()                                 # cool thing showing creation in real time
        base.save(Path('./images/'+ str(edition) + '.png'), "PNG")
        edition += 1
        print("creating fruity booty #" + str(edition - 1))



timeStart = datetime.datetime.now()
createFruit()
timeEnd = datetime.datetime.now()

timeTaken = timeEnd-timeStart
a = 12000/(numFruits*numEachFruit)
print(timeTaken*a)