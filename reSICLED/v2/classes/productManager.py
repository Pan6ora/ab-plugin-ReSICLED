import brightway2 as bw

def addMaterialToProd(materialName,materialBase,prodBase,prodName):
    prodDict=prodBase.load()
    materialactivity=materialBase.load()[("Materials",materialName)]
    materialactivity["Class"]="Material"
    prodDict[(prodName,materialName)]=materialactivity
    prodBase.write(prodDict)

def addPiece(name,weight,amount,materialName,prodName,prodDatabase,materialBase):
    if not (prodName,materialName) in list(prodDatabase.load().keys()):
        addMaterialToProd(materialName,materialBase,prodDatabase,prodName)
    if not ((prodName,name) in list(prodDatabase.load().keys()) and prodDatabase.load()[(prodName,name)]["Class"]=="Piece"):
        dico=prodDatabase.load()
        newpiece={}
        newpiece["Class"]="Piece"
        newpiece["Name"]=name
        newpiece["Weight"]=weight
        newpiece["Amount"]=amount
        newpiece["Material"]=(prodName,materialName)
        dico[(prodName,name)]=newpiece
        prodDatabase.write(dico)
