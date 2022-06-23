


def getElementList(prodDatabase,criteria):
    elementList=[]
    for key in list(prodDatabase.load().keys()):
        if prodDatabase.load()[key]["Class"]==criteria:
            elementList.append(prodDatabase.load()[key])
    return elementList

def getMaterialByName(materialName,materialList):
    for material in materialList:
        if material["Name"]==materialName:
            return material
    return None
