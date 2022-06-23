from calculations.rates import computeDismPerPiece

def displayDismantlingTable(piecesList,materialsList):
    # formatting variables 
    maxName=max([len(piece["Name"]) for piece in piecesList])
    print("-"*(maxName+11)+"+"+'-'*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    print(" Name"+" "*(maxName+6)+"|"+" Recycle weight | Energy weight | Waste weight | Amount |")
    print("-"*(maxName+11)+"+"+'-'*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")
    for piece in piecesList:
        a=computeDismPerPiece(piece,materialsList)
        print(" "+piece["Name"]+" "*(maxName+10-len(piece["Name"]))+"| {} | {} | {} | {} |".format(" "*(14-len(str(a[0])))+str(a[0])," "*(13-len(str(a[1])))+str(a[1])," "*(12-len(str(a[2])))+str(a[2])," "*(6-len(str(piece["Amount"])))+str(piece["Amount"])))
    print("-"*(maxName+11)+"+"+'-'*16+"+"+"-"*15+"+"+"-"*14+"+"+"-"*8+"+")

