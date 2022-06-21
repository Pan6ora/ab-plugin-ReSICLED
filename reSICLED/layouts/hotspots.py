from calculations.gains import relativeWeight, gain1
from calculations.rates import computeShreddingPerPiece
from calculations.utils import arrondi

def displayFirstHotspotsTable(piecesList : list, arrond : int):
    notPolluantList = []
    polluantList = []
    for piece in piecesList:
        if piece.material.polluant:
            polluantList.append(piece)
        else:
            notPolluantList.append(piece)
    notPolluantList=sorted(notPolluantList, key=lambda x : gain1(x,arrond)*relativeWeight(x,piecesList,arrond),reverse=True)
    newOrder=notPolluantList+polluantList
    maxName=max([len(piece.name) for piece in newOrder])
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*17+"+"+"-"*24+"+")
    print(" {} | {} | {} | {} | {} | {} |".format(" Id ","Name"+" "*(maxName+5),"Polluant","Gain 1","Relative weight","Gain 1*Relative weight"))
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*17+"+"+"-"*24+"+")
    for piece in newOrder:
        id=piecesList.index(piece)+1
        print(" {} | {} | {} | {} | {} | {} |".format(" "*(4-len(str(id)))+str(id),\
                                                      piece.name+" "*(maxName+9-len(piece.name)),\
                                                      ("Yes"+" "*5)*piece.material.polluant+("No"+" "*6)*(not piece.material.polluant),\
                                                      " "*(6-len(str(gain1(piece,arrond))))+str(gain1(piece,arrond)),\
                                                      " "*(15-len(str(relativeWeight(piece,piecesList,arrond))))+str(relativeWeight(piece,piecesList,arrond)),\
                                                      " "*(22-len(str(arrondi(gain1(piece,arrond)*relativeWeight(piece,piecesList,arrond),arrond))))+str(arrondi(gain1(piece,arrond)*relativeWeight(piece,piecesList,arrond),arrond))))
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*8+"+"+"-"*17+"+"+"-"*24+"+")

def displaySecondHotspotsTable(piecesList : list, arrond : int):
    sortedPieces = sorted(piecesList, key = lambda x : computeShreddingPerPiece(x,arrond)[2],reverse=True)
    maxName=max([len(piece.name) for piece in sortedPieces])
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*14+"+"+"-"*8+"+")
    print(" {} | {} | {} | {} | {} |".format(" Id ", "Name"+" "*(maxName+5), "Polluant","Waste weight","Amount"))
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*14+"+"+"-"*8+"+")
    for piece in sortedPieces:
        id=piecesList.index(piece)+1
        print(" {} | {} | {} | {} | {} |".format(" "*(4-len(str(id)))+str(id),\
                                                      piece.name+" "*(maxName+9-len(piece.name)),\
                                                      ("Yes"+" "*5)*piece.material.polluant+("No"+" "*6)*(not piece.material.polluant),\
                                                      " "*(12-len(str(computeShreddingPerPiece(piece,arrond)[2])))+str(computeShreddingPerPiece(piece,arrond)[2]),\
                                                      " "*(6-len(str(piece.amount)))+str(piece.amount)))
                                                      
    print("------+"+"-"*(maxName+11)+"+"+'-'*10+"+"+"-"*14+"+"+"-"*8+"+")
    
