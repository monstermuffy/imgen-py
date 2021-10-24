from pathlib import Path
import os
import json
import sys

metadataFiles = (os.listdir(Path('./metadata')))

ipfs = "ipfs://QmZWVLD6MdLX9GhYHAnsVY2dVv527nS1PAmjcnvA8pR5o9/"

def cleanMetadataFolder():
    for f in os.listdir(Path('./fixedMetadata')):
        if not f.endswith(""):
            continue
        os.remove(os.path.join(Path('./fixedMetadata'), f))


for i in range(len(metadataFiles)):
    tempString = ipfs + str(i+1) + ".png"
    a_file = open('./metadata/' + str(i+1) + '.json', "r")
    json_object = json.load(a_file)
    a_file.close()
    #print(json_object)

    json_object["image"] = tempString
    
    #print(json_object)
    with open('fixedMetadata/' + str(i+1) + '', 'w') as f:
        json.dump(json_object, f) 

for i in range(len(metadataFiles)):
    tempString = ipfs + str(i+1) + ".png"
    a_file = open('./metadata/' + str(i+1) + '.json', "r")
    json_object = json.load(a_file)
    a_file.close()
    #print(json_object)

    json_object["attributes"] = [{
        "trait_type": "Unrevealed"
    }]
    
    #print(json_object)
    with open('unrevealedMetadata/' + str(i+1) + '', 'w') as f:
        json.dump(json_object, f) 