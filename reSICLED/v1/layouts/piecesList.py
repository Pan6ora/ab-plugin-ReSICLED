def displayPiecesList(piecesList):
    if len(piecesList)>0:
        maxName=max(max([len(piece.name) for piece in piecesList]),4)
        maxMatName =max(max([len(piece.material.name) for piece in piecesList]),8)
        #print("------+"+"-"*(maxName+11)+"+"+"-"*(maxMatName+6)+"+"+"-"*10+"+"+"-"*8+"+"+"-"*8+"+")
        #print("  {}  | {} | {} | {} | {} | {} |".format("Id",\
                                                        "Name"+" "*(maxName+5),\
                                                        "Material"+" "*(maxMatName-4),\
                                                        "Polluant",\
                                                        "Weight",\
                                                        "Amount"))
        #print("------+"+"-"*(maxName+11)+"+"+"-"*(maxMatName+6)+"+"+"-"*10+"+"+"-"*8+"+"+"-"*8+"+")
        for i in range(len(piecesList)):
            piece=piecesList[i]
            #print(" {} | {} | {} | {} | {} | {} |".format(" "*(4-len(str(i+1)))+str(i+1),\
                                                          piece.name+" "*(maxName+9-len(piece.name)),\
                                                          piece.material.name+" "*(maxMatName+4-len(piece.material.name)),\
                                                          ("Yes"+" "*5)*piece.material.polluant+("No"+" "*6)*(not piece.material.polluant),\
                                                          " "*(6-len(str(piece.weight)))+str(piece.weight),\
                                                          " "*(6-len(str(piece.amount)))+str(piece.amount)))

        #print("------+"+"-"*(maxName+11)+"+"+"-"*(maxMatName+6)+"+"+"-"*10+"+"+"-"*8+"+"+"-"*8+"+")