from .piecesManager import getMaterialByName

def gain1(piece, materialsList):
    if not getMaterialByName(piece["Material"][1],materialsList)["Pollutant"]:
        return getMaterialByName(piece["Material"][1],materialsList)["Dismantling recovery"]-getMaterialByName(piece["Material"][1],materialsList)["Shredding recovery"]
    else:
        return 0.

def gain2(piece, materialsList) -> float:
    if getMaterialByName(piece["Material"][1],materialsList)["Pollutant"]:
        return 0.
    else:
        return getMaterialByName(piece["Material"][1],materialsList)["Dismantling recovery"]+getMaterialByName(piece["Material"][1],materialsList)["Dismantling energy"]-getMaterialByName(piece["Material"][1],materialsList)["Shredding recovery"]-getMaterialByName(piece["Material"][1],materialsList)["Shredding energy"]

def relativeWeight(piece, piecesList) -> float:
    """
    Returns the relative weight of the piece among the whole unit
    """
    return (piece["Weight"]/weight(piecesList))

def weight(piecesList : list) -> float:
    return sum([piece["Weight"] for piece in piecesList])