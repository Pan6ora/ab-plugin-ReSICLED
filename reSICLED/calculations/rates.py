from classes.piece import Piece
from .gains import weight
from .utils import arrondi

def computeDismantlingPerPiece(piece : Piece, arrond : int) -> tuple:
    """
    takes a piece and returns the recovery rate, energy recovery and residual waste for a single unit being dismantled
    (as example, a piece with 90% waste and a 100g weight will return a 90 for the residual waste)

    Since the piece is not mutable, we can use a tuple
    """
    return (arrondi(piece.weight*piece.material.demrec,arrond),arrondi(piece.weight*piece.material.demener,arrond),arrondi(piece.weight*piece.material.demwaste,arrond))
    
def computeShreddingPerPiece(piece : Piece, arrond : int) -> tuple:
    """
    takes a piece and returns the recovery rate, energy recovery and residual waste for a single unit being shredded
    (as example, a piece with 90% waste and a 100g weight will return a 90 for the residual waste)

    Since the piece is not mutable, we can use a tuple
    """
    if not piece.material.polluant:
        return (arrondi(piece.weight*piece.material.brorec,arrond),arrondi(piece.weight*piece.material.broener,arrond),arrondi(piece.weight*piece.material.browaste,arrond))
    else:
        return (arrondi(piece.weight*piece.material.demrec,arrond),arrondi(piece.weight*piece.material.demener,arrond),arrondi(piece.weight*piece.material.demwaste,arrond))
    
def getDismantlingRates(pieceList : list) -> tuple:
    recoveryRate=0
    energyRate=0
    wasteRate=0
    totalWeight=weight(pieceList)
    for piece in pieceList:
        recoveryRate+=computeDismantlingPerPiece(piece)[0]
        energyRate+=computeDismantlingPerPiece(piece)[1]
        wasteRate+=computeDismantlingPerPiece(piece)[2]
    return (recoveryRate/totalWeight,energyRate/totalWeight,wasteRate/totalWeight)

def getMixedRates(piecesList : list, strategyDict : dict, arrond) -> tuple:
    recoveryRate=0
    energyRate=0
    wasteRate=0
    totalWeight=weight(piecesList)
    for piece in piecesList:
        if strategyDict[piece][0]=="Dismantling":
            recoveryRate+=computeDismantlingPerPiece(piece,arrond)[0]
            energyRate+=computeDismantlingPerPiece(piece,arrond)[1]
            wasteRate+=computeDismantlingPerPiece(piece,arrond)[2]
        else:
            recoveryRate+=computeShreddingPerPiece(piece,arrond)[0]
            energyRate+=computeShreddingPerPiece(piece,arrond)[1]
            wasteRate+=computeShreddingPerPiece(piece,arrond)[2]
    return (recoveryRate/totalWeight,energyRate/totalWeight,wasteRate/totalWeight)