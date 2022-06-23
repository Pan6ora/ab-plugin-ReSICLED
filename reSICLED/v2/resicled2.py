# main program v2

import brightway2 as bw
import os
import sys
from bw2io.package import BW2Package
from classes.productManager import addPiece

def getFileByName(directory):
    for file in os.listdir(directory):
        if file[:9]=="Materials" and os.path.splitext(file)==".bw2package":
            return file
    return None

def main():
    os.system("clear")
    print("Welcome to ReSICLED")
    print("Current version : 1.2\n")
    a = input("Type 'begin' to start a new product, or 'quit' to quit the app : ")
    bw.projects.set_current("reSICLED")
    if "Materials" not in bw.databases:
        #We have to add it to the databases linked to the project
        if getFileByName(os.getcwd()) is not None:
            BW2Package().import_file(os.path.join(os.getcwd(),getFileByName(os.getcwd())))
        else:
            print("There is no Materials data inserted in the parent directoty")
            sys.exit(1)
    materials=bw.Database("Materials")
    while a != "quit":
        if a == "begin":
            # begin part, we init the project : 
            os.system("clear")
            productName = input("What's your product's name ? ")
            while productName in list(bw.databases):
                os.system("clear")
                print("This name is already used !")
                productName = input("What's your product's name ? ")
            productDatabase = bw.Database(productName)

            a = input("Type 'input' to reach the pieces input part, or 'quit' to exit : ")

        elif a == "input":
            # Inputing pieces
            b = input("Type 'add' to add a new piece, 'next' to step forward or 'quit' to quit : ")
            if b=='quit':
                sys.exit(0)
            elif b=='next':
                a="dismantling"
            elif b=='add':
                os.system("clear")
                name = input("What's the piece's name ? ")
                weight = float(input("What's the piece's weight ? "))
                materialName = input("What is the piece's material ? ")
                amount = int(input("How many of this piece are in the product ? "))
                addPiece(name,weight,amount,materialName,productName,productDatabase,materials)
                a="input" # security matter

        elif a == "dismantling":
            sys.exit(0)
    

if __name__=="__main__":
    main()