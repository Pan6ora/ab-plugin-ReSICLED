# main program v2

import brightway2 as bw
import os
import sys
from bw2io.package import BW2Package
from classes.productManager import addPiece
from layouts.piecesList import displayPiecesList
from calculations.piecesManager import getElementList
from layouts.dismantling import displayDismantlingTable
from layouts.shredding import displayShreddingTable
from layouts.mixed import displayMixedTable
from layouts.mixed import setStrategyDict

def getFileByName(directory):
    for file in os.listdir(directory):
        if file[:9]=="Materials" and os.path.splitext(file)[1]==".bw2package":
            return file
    return None

def selectDirective(directiveFile):
    os.system("clear")
    #print("List of all Directives to apply to the product : \n")
    #print("1 - large household appliances")
    #print("2 - Small household appliance")
    #print("3 - IT/Telecom equipment")
    #print("4 - Consumer equipment")
    #print("5A - Lighting equipment : Gas discharge lamps")
    #print("5B - Lighting Equipment - Other")
    #print("6 - Electrical / Electronical tools")
    #print("7 - Toys, leisure, sports equipment")
    #print("8 - Medical devices")
    #print("9 - Monitoring and control equipments")
    #print("10 - Automatic dispensers")
    selected = input("Which directive do you choose ?")
    if selected == '5A':
        selected=5
    elif selected=="5B":
        selected=6
    elif int(selected)>=6:
        selected=int(selected)+1
    else:
        selected=int(selected)
    with open(directiveFile,"r") as f:
        return [float(nb) for nb in f.readlines()[selected].split(",")]

def main():
    directive = None
    os.system("clear")
    #print(os.getcwd())
    #print("Welcome to ReSICLED")
    #print("Current version : 1.2\n")
    a = input("Type 'begin' to start a new product, or 'quit' to quit the app : ")
    bw.projects.set_current("reSICLED")
    if "Materials" not in bw.databases:
        #We have to add it to the databases linxœked to the project
        if getFileByName(os.getcwd()) is not None:
            BW2Package().import_file(os.path.join(os.getcwd(),getFileByName(os.getcwd())))
        else:
            #print("There is no Materials data inserted in the parent directoty")
            sys.exit(1)
    materials=bw.Database("Materials")
    while a != "quit":
        if a == "begin":
            # begin part, we init the project : 
            os.system("clear")
            productName = input("What's your product's name ? ")
            while productName in list(bw.databases):
                os.system("clear")
                #print("This name is already used !")
                productName = input("What's your product's name ? ")
            productDatabase = bw.Database(productName)

            a = input("Type 'input' to reach the pieces input part, or 'quit' to exit : ")

        elif a == "input":
            # Inputing pieces
            piecesList = getElementList(productDatabase,"Piece")
            materialsList = getElementList(productDatabase, "Material")
            b = input("Type 'add' to add a new piece, 'next' to step forward or 'quit' to quit : ")
            if b=='quit':
                sys.exit(0)
            elif b=='next':
                a="dismantling"
            elif b=='add':
                os.system("clear")
                displayPiecesList(piecesList, materialsList)
                name = input("What's the piece's name ? ")
                weight = float(input("What's the piece's weight ? "))
                materialName = input("What is the piece's material ? ")
                amount = int(input("How many of this piece are in the product ? "))
                addPiece(name,weight,amount,materialName,productName,productDatabase,materials)
                a="input" # security matter

        elif a == "dismantling":
            os.system("clear")
            displayDismantlingTable(piecesList,materialsList)
            if directive is None:
                zeb=input("No directive selected yet : Press enter to select a directive ")
                directive = selectDirective("directives.txt")
            else:
                #print("the current directive selected is  : ",directive)
                a = input("Type 'shred' to go to shredding part, or 'quit' to quit the app : ")

        elif a == "shred":
            os.system("clear")
            displayShreddingTable(piecesList,materialsList)
            #print("the current directive selected is  : ",directive)
            a = input("Type 'mixed' to get  to the next step, or 'quit' to quit the app : ")
        
        elif a == "mixed":
            stratDcit = setStrategyDict(piecesList, materialsList)
            displayMixedTable(piecesList,stratDcit,materialsList)
            os.system("pause")


        elif a== 'quit':
            sys.exit(0)


if __name__=="__main__":
    main()