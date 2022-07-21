import os
from calculations.gains import gain1, gain2, relativeWeight
from calculations.rates import computeDismantlingPerPiece
from calculations.rates import computeShreddingPerPiece
from classes.piece import Piece

def setStrategyDict(piecesList):
    """
    sets the dict containing the infos about the recycling strategy used, and if we can change the strategy (to keep user from changing the strategy for polluants)
    key : piece, value : tuple ("Shredding"/"Dismantling", false)
    """
    strategyDict= {}
    for piece in piecesList:
        if piece.material.polluant:
            strategyDict[piece]=("Dismantling",False)
        else:
            strategyDict[piece]=("Shredding",True)
    return strategyDict


def displayMixedTable(piecesList : list ,arrond : int, strategyDict : dict) -> None:
    maxName = max([len(piece.name) for piece in piecesList])
    #print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*8+"+"+"-"*17+"+"+"-"*13+"+"+"-"*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    #print("  Id  | Name"+" "*(maxName+6)+"|"+" Polluant | Gain 1 | Gain 2 | Relative weight | Strategy    | Recycle weight | Energy weight | Waste weight | Amount |")
    #print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*8+"+"+"-"*17+"+"+"-"*13+"+"+"-"*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    counter=0
    for piece in piecesList:
        if piece.material.polluant:
            #polluant piece
            a=computeDismantlingPerPiece(piece,arrond)
            #print(" {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(" "*(4-len(str(counter)))+str(counter+1), \
                                                                                    piece.name+" "*(maxName+9-len(piece.name)), \
                                                                                    "Yes"+" "*5," "*(6-len(str(gain1(piece,arrond))))+str(gain1(piece,arrond)), \
                                                                                    " "*(6-len(str(gain2(piece,arrond))))+str(gain2(piece,arrond)), \
                                                                                    " "*(15-len(str(relativeWeight(piece,piecesList,arrond))))+str(relativeWeight(piece,piecesList,arrond)), \
                                                                                    " "*(11-len(strategyDict[piece][0]))+strategyDict[piece][0],\
                                                                                    " "*(14-len(str(a[0])))+str(a[0])," "*(13-len(str(a[1])))+str(a[1])," "*(12-len(str(a[2])))+str(a[2])," "*(6-len(str(piece.amount)))+str(piece.amount)))
        else:
            a=computeShreddingPerPiece(piece,arrond)
            #print(" {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(" "*(4-len(str(counter)))+str(counter+1), \
                                                                                    piece.name+" "*(maxName+9-len(piece.name)), \
                                                                                    "No"+" "*6," "*(6-len(str(gain1(piece,arrond))))+str(gain1(piece,arrond)), \
                                                                                    " "*(6-len(str(gain2(piece,arrond))))+str(gain2(piece,arrond)), \
                                                                                    " "*(15-len(str(relativeWeight(piece,piecesList,arrond))))+str(relativeWeight(piece,piecesList,arrond)), \
                                                                                    " "*(11-len(strategyDict[piece][0]))+strategyDict[piece][0],\
                                                                                    " "*(14-len(str(a[0])))+str(a[0])," "*(13-len(str(a[1])))+str(a[1])," "*(12-len(str(a[2])))+str(a[2])," "*(6-len(str(piece.amount)))+str(piece.amount)))
        counter+=1       


    #print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*8+"+"+"-"*17+"+"+"-"*13+"+"+"-"*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")

