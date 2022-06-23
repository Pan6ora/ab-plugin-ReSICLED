# Dismantling layout 
from calculations.rates import computeDismantlingPerPiece

def displayDismantlingTable(piecesList,arrond):
    # formatting variables 
    maxName=max([len(piece.name) for piece in piecesList])
    print("-"*(maxName+11)+"+"+'-'*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    print(" Name"+" "*(maxName+6)+"|"+" Recycle weight | Energy weight | Waste weight | Amount |")
    print("-"*(maxName+11)+"+"+'-'*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    for piece in piecesList:
        a=computeDismantlingPerPiece(piece,arrond)
        print(" "+piece.name+" "*(maxName+10-len(piece.name))+"| {} | {} | {} | {} |".format(" "*(14-len(str(a[0])))+str(a[0])," "*(13-len(str(a[1])))+str(a[1])," "*(12-len(str(a[2])))+str(a[2])," "*(6-len(str(piece.amount)))+str(piece.amount)))
    print("-"*(maxName+11)+"+"+'-'*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")

