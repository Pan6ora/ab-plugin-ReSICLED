import os
from calculations.gains import gain1, gain2, relativeWeight
from calculations.rates import computeDismPerPiece
from calculations.rates import computeShredPerPiece
from calculations.piecesManager import getMaterialByName

def setStrategyDict(piecesList, materialsList):
    """
    sets the dict containing the infos about the recycling strategy used, and if we can change the strategy (to keep user from changing the strategy for polluants)
    key : piece, value : tuple ("Shredding"/"Dismantling", false)
    """
    strategyDict= {}
    for piece in piecesList:
        if getMaterialByName(piece["Material"][1],materialsList)["Pollutant"]:
            strategyDict[piece["Name"]]=("Dismantling",False)
        else:
            strategyDict[piece["Name"]]=("Shredding",True)
    return strategyDict


def displayMixedTable(piecesList : list, strategyDict : dict, materialsList) -> None:
    maxName = max([len(piece["Name"]) for piece in piecesList])
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*8+"+"+"-"*17+"+"+"-"*13+"+"+"-"*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    print("  Id  | Name"+" "*(maxName+6)+"|"+" Polluant | Gain 1 | Gain 2 | Relative weight | Strategy    | Recycle weight | Energy weight | Waste weight | Amount |")
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*8+"+"+"-"*17+"+"+"-"*13+"+"+"-"*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    counter=0
    for piece in piecesList:
        if getMaterialByName(piece["Material"][1],materialsList)["Pollutant"]:
            #polluant piece
            a=computeDismPerPiece(piece, materialsList)
            print(" {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(" "*(4-len(str(counter)))+str(counter+1), \
                                                                                    piece["Name"]+" "*(maxName+9-len(piece["Name"])), \
                                                                                    "Yes"+" "*5," "*(6-len(str(gain1(piece,materialsList))))+str(gain1(piece,materialsList)), \
                                                                                    " "*(6-len(str(gain2(piece,materialsList))))+str(gain2(piece,materialsList)), \
                                                                                    " "*(15-len(str(relativeWeight(piece,piecesList))))+str(relativeWeight(piece,piecesList)), \
                                                                                    " "*(11-len(strategyDict[piece["Name"]][0]))+strategyDict[piece["Name"]][0],\
                                                                                    " "*(14-len(str(a[0])))+str(a[0])," "*(13-len(str(a[1])))+str(a[1])," "*(12-len(str(a[2])))+str(a[2])," "*(6-len(str(piece["Amount"])))+str(piece["Amount"])))
        else:
            a=computeShredPerPiece(piece,materialsList)
            print(" {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(" "*(4-len(str(counter)))+str(counter+1), \
                                                                                    piece["Name"]+" "*(maxName+9-len(piece["Name"])), \
                                                                                    "No"+" "*6," "*(6-len(str(gain1(piece,materialsList))))+str(gain1(piece,materialsList)), \
                                                                                    " "*(6-len(str(gain2(piece,materialsList))))+str(gain2(piece,materialsList)), \
                                                                                    " "*(15-len(str(relativeWeight(piece,piecesList))))+str(relativeWeight(piece,piecesList)), \
                                                                                    " "*(11-len(strategyDict[piece["Name"]][0]))+strategyDict[piece["Name"]][0],\
                                                                                    " "*(14-len(str(a[0])))+str(a[0])," "*(13-len(str(a[1])))+str(a[1])," "*(12-len(str(a[2])))+str(a[2])," "*(6-len(str(piece["Amount"])))+str(piece["Amount"])))
        counter+=1       


    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*8+"+"+"-"*17+"+"+"-"*13+"+"+"-"*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")

