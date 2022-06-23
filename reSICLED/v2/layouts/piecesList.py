from calculations.piecesManager import getMaterialByName

def displayPiecesList(piecesList,materialsList):
    if len(piecesList)>0:
        maxName=max(max([len(piece["Name"]) for piece in piecesList]),4)
        maxMatName =max(max([len(piece["Material"][1]) for piece in piecesList]),8)
        print("------+"+"-"*(maxName+11)+"+"+"-"*(maxMatName+6)+"+"+"-"*10+"+"+"-"*8+"+"+"-"*8+"+")
        print("  {}  | {} | {} | {} | {} | {} |".format("Id",\
                                                        "Name"+" "*(maxName+5),\
                                                        "Material"+" "*(maxMatName-4),\
                                                        "Polluant",\
                                                        "Weight",\
                                                        "Amount"))
        print("------+"+"-"*(maxName+11)+"+"+"-"*(maxMatName+6)+"+"+"-"*10+"+"+"-"*8+"+"+"-"*8+"+")
        for i in range(len(piecesList)):
            piece=piecesList[i]
            print(" {} | {} | {} | {} | {} | {} |".format(" "*(4-len(str(i+1)))+str(i+1),\
                                                          piece["Name"]+" "*(maxName+9-len(piece["Name"])),\
                                                          piece["Material"][1]+" "*(maxMatName+4-len(piece["Material"][1])),\
                                                          ("Yes"+" "*5)*getMaterialByName(piece["Material"][1],materialsList)["Pollutant"]+("No"+" "*6)*(not getMaterialByName(piece["Material"][1],materialsList)["Pollutant"]),\
                                                          " "*(6-len(str(piece["Weight"])))+str(piece["Weight"]),\
                                                          " "*(6-len(str(piece["Amount"])))+str(piece["Amount"])))

        print("------+"+"-"*(maxName+11)+"+"+"-"*(maxMatName+6)+"+"+"-"*10+"+"+"-"*8+"+"+"-"*8+"+")