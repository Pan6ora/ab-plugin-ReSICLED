from .piecesManager import getMaterialByName

def computeDismPerPiece(piece, materialsList):
    mat=getMaterialByName(piece["Material"][1],materialsList)
    rec = mat["Dismantling recovery"]*piece["Weight"]
    ene = mat["Dismantling energy"]*piece["Weight"]
    was = mat["Dismantling waste"]*piece["Weight"]
    return (rec,ene,was)

def computeShredPerPiece(piece, materialsList):
    mat=getMaterialByName(piece["Material"][1],materialsList)
    if not mat["Pollutant"]:
        rec = mat["Shredding recovery"]*piece["Weight"]
        ene = mat["Shredding energy"]*piece["Weight"]
        was = mat["Shredding waste"]*piece["Weight"]
    else:
        rec = mat["Dismantling recovery"]*piece["Weight"]
        ene = mat["Dismantling energy"]*piece["Weight"]
        was = mat["Dismantling waste"]*piece["Weight"]
    return (rec,ene,was)