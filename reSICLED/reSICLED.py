import os
import json
from classes.material import Material
from classes.piece import Piece
from layouts.dismantling import displayDismantlingTable
from layouts.mixed import displayMixedTable, setStrategyDict
from layouts.shredding import displayShreddingTable
from layouts.hotspots import displayFirstHotspotsTable, displaySecondHotspotsTable
from layouts.piecesList import displayPiecesList
from calculations.rates import getMixedRates
from calculations.utils import arrondi

def getMaterialsNames(materialsList):
    """
    Returns the list of all materials' names in materialsList
    """
    return [material.name for material in materialsList]

def setMaterialsList(data):
    """
    data is the list of all materials stored in the json file
    """
    materialsList=[]
    for material in data:
        # type(material)=dict
        name=material['material name']
        type_material=material['material type']
        demrec=material['after dismantling']['recovery potential']
        demener=material['after dismantling']['energy recovery potential']
        demwaste = material['after dismantling']['residual waste potential']
        brorec=material['after shredding']['recovery potential']
        broener = material['after shredding']['energy recovery potential']
        browaste = material['after shredding']['residual waste potential']
        price=material['after shredding']['price']
        materialsList.append(Material(name,type_material,demrec,demener,demwaste,brorec,broener,browaste,price))
    return materialsList

def getMaterialByName(materialname,materialsList):
    """
    Gets the material with the name given in parameter in the materialsList
    """
    for material in materialsList:
        if material.name==materialname:
            return material
    return None

def mainMenu(pieceList,materialList):
    os.system("cls")
    print("Main Menu\n\n")
    select=input("Type 'add' to add a new piece, 'next' to step forward to Dismantling Part, or 'quit' to quit the application : ")
    if select=='quit':
        return "EXIT_SUCCESS"
    elif select=='add':
        AddPieceForm(pieceList,materialList)
    elif select=='next':
        print(computeDismantlingScores(pieceList))
    else:
        mainMenu(pieceList,materialList)

def AddPieceForm(pieceList,materialList):
    print("New Piece : \n")
    name = input("Piece Name : ")
    weight = float(input("Piece's weight (in grams) : "))
    material_type = input("Piece's Material Class (Polymer, Metal, Component, Other) : ")
    material = input("Piece's Material : ")
    amount = input("Number of pieces : ")
    pieceList.append(Piece(name,weight,material_type,getMaterialByName(material,materialList),amount))

def computeShreddingScores(piecesList):
    """
    Takes all pieces and computes the scores for Dismantling scenario
    """
    totalMass = sum([piece.weight for piece in piecesList])
    recovery_mass = 0
    energy_mass = 0
    waste_mass = 0
    for piece in piecesList:
        if piece.material.polluant:
            recovery_mass+=piece.weight*piece.material.demrec
            energy_mass+=piece.weight*piece.material.demener
            waste_mass+=piece.weight*piece.material.demwaste
        else:
            recovery_mass+=piece.weight*piece.material.brorec
            energy_mass+=piece.weight*piece.material.broener
            waste_mass+=piece.weight*piece.material.browaste
    return (recovery_mass/totalMass,energy_mass/totalMass,waste_mass/totalMass)

def computeDismantlingScores(piecesList):
    """
    Takes all pieces and computes the scores for Dismantling scenario
    """
    totalMass = sum([piece.weight for piece in piecesList])
    recovery_mass = 0
    energy_mass = 0
    waste_mass = 0
    for piece in piecesList:
        recovery_mass+=piece.weight*piece.material.demrec
        energy_mass+=piece.weight*piece.material.demener
        waste_mass+=piece.weight*piece.material.demwaste
    return (recovery_mass/totalMass,energy_mass/totalMass,waste_mass/totalMass)

def selectDirective(directiveFile):
    os.system("cls")
    print("List of all Directives to apply to the product : \n")
    print("1 - large household appliances")
    print("2 - Small household appliance")
    print("3 - IT/Telecom equipment")
    print("4 - Consumer equipment")
    print("5A - Lighting equipment : Gas discharge lamps")
    print("5B - Lighting Equipment - Other")
    print("6 - Electrical / Electronical tools")
    print("7 - Toys, leisure, sports equipment")
    print("8 - Medical devices")
    print("9 - Monitoring and control equipments")
    print("10 - Automatic dispensers")
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
        

if __name__=='__main__':
    arrond_const=4
    with open("data.json","r") as f:
        jdata = json.load(f)
    materialList=setMaterialsList(jdata)
    #pieceList=[Piece("capot",20,"Polymer",getMaterialByName("ABS",materialList),1),Piece("carte sim",1,"Polymer",getMaterialByName("Other Polymer",materialList),1),Piece("Vis",0.25,"Metal",getMaterialByName("Other metal",materialList),4)]
    StrategyDict_setup_status=False
    pieceList=[]
    directive_objectives=None
    lrighozeg = input("Welcome to reSICLED Python Shell version. Press Enter to start")
    os.system("cls")
    main_selector=input("Type 'add' to add a new piece, 'dism' to step forward to Dismantling Part, or 'quit' to quit the application : ")
    mixed_selector="main"
    while not main_selector=="quit":
        if main_selector=="add":
            os.system("cls")
            print("Current list of all added pieces")
            displayPiecesList(pieceList)
            #adding a new piece to the full list :
            AddPieceForm(pieceList, materialList)
            main_selector=input("Type 'add' to add a new piece, 'dism' to step forward to Dismantling Part, or 'quit' to quit the application : ")
    
        elif main_selector=="dism":
            #stepping forward to Dismantling scenario
            os.system("cls")
            print("Recyclability rates in case we follow the full demantling scenario (best scenario possible yet impossible because of money reasons)")
            displayDismantlingTable(pieceList, arrond_const)
            print("Current Recycling Rates for the whole product are : ")
            a=computeDismantlingScores(pieceList)
            print("Recovery Rate : {} %\n Energy Recovery Rate : {} %\n Residual Waste Rate : {} %".format(100*arrondi(a[0],arrond_const),100*arrondi(a[1],arrond_const),100*arrondi(a[2],arrond_const)))
            if directive_objectives is None:
                main_selector=input("No Recovery objective has been selected, please type 'select' to select one among the list available : ")
            else:
                print("The current objectives to be reached are : ")
                print("Recovery Rate : {} %\n Energy Recovery Rate : {} %\n Residual Waste Rate : {} %".format(100*directive_objectives[0],100*directive_objectives[1],100*directive_objectives[2]))
                print("Since the full demantling scenario is the one with the best results, we need to seek on scenarios that are possible but less efficient")
                main_selector = input("Type 'shred' to take a look at the worst possible scenario, or 'quit' to quit reSICLED.")

        elif main_selector=="select":
            # Directive selection mode
            directive_objectives =  selectDirective("directives.txt")
            main_selector = "dism"

        elif main_selector == "shred":
            # Shredding scenario
            os.system("cls")
            print("Recyclability rates, in case we follow the full Shredding scenario : ")
            displayShreddingTable(pieceList, arrond_const)
            print("Current Recycling Rates for the whole product are : ")
            b = computeShreddingScores(pieceList)
            print("Recovery Rate : {} %\n Energy Recovery Rate : {} %\n Residual Waste Rate : {} %".format(arrondi(100*b[0],arrond_const),arrondi(100*b[1],arrond_const),arrondi(100*b[2],arrond_const)))
            print("The Recovery objectives to reach are the following :")
            print("Recovery Rate : {} %\n Energy Recovery Rate : {} %\n Residual Waste Rate : {} %".format(100*directive_objectives[0],100*directive_objectives[1],100*directive_objectives[2]))
            if b[0]>=directive_objectives[0] and b[1]>=directive_objectives[1]:
                #All objectives are reached with htis scenario
                print("All the recovery objectives defined by the directives are reached, hence the design of the product is sufficient to respect these rules.")
                zeli=input("Press enter to quit the software")
                main_selector="quit"
            else:
                print("One of the objectives is not reached so far, since Full Shredding is the worst scenario possible, we'll have to change some strategies in a mixed Scenario")
                zefn = input("Press Enter to get to Mixed Scenario ")
                main_selector = "mixed"


        elif main_selector=="mixed":
            # mixed scenario
            strategyDict=setStrategyDict(pieceList)
            while not mixed_selector=="quit_mixed":
                if mixed_selector=="main":
                    #main entrance, displaying the mixed table, which is updated everytime we go back to this "tab"
                    print("Mixed scenario : you can change the outcome of each piece (as long as it's not pollutant)")
                    displayMixedTable(pieceList,arrond_const,strategyDict)
                    print("The current recycling objectives are :")
                    c = getMixedRates(pieceList,strategyDict,arrond_const)
                    print("Recovery Rate : {} %\n Energy Recovery Rate : {} %\n Residual Waste Rate : {} %".format(arrondi(100*c[0],arrond_const),arrondi(100*c[1],arrond_const),arrondi(100*c[2],arrond_const)))
                    if c[0]>=directive_objectives[0] and c[1]>=directive_objectives[1]:
                        print("The recovery objectives are reached, you can now quit the app")
                    else:
                        print("Recovery objectives are not reached so far, you shall change some pieces's recovery status")
                    mixed_selector=input("Type 'hotspots' to see the hotspots, 'change' to change some piece's strategy or 'quit_mixed' to quit the app")
                
                elif mixed_selector=="hotspots":
                    os.system("cls")
                    print("These are the hotspots tables, presenting the most relevant pieces to change strategy and reach the objective")
                    displayFirstHotspotsTable(pieceList,arrond_const)
                    displaySecondHotspotsTable(pieceList,arrond_const)
                    ekjrge=input("Type Enter to go back to the mixed scenario tab and change some pieces outcomes")
                    mixed_selector="main"

                elif mixed_selector=="change":
                    os.system("cls")
                    displayMixedTable(pieceList,arrond_const,strategyDict)
                    choice=int(input("Which piece do you want to change the recovery strategy : "))
                    if strategyDict[pieceList[choice-1]][1]==False:
                        print("Sorry, but due to its polluting status, this piece has to be dismantled")
                        rechoice = input("Do you still want to change a piece's strategy [Y/N] ?")
                        if rechoice=="N":
                            mixed_selector=="quit_mixed"
                    else:
                        print("This piece's can be changed.")
                        if strategyDict[pieceList[choice-1]][0]=="Dismantling":
                            strategyDict[pieceList[choice-1]]=("Shredding",True)
                        else:
                            strategyDict[pieceList[choice-1]]=("Dismantling",True)
                        print("The piece's status has been updated, you'll be redirected to the Mixed table tab.")
                        mixed_selector="main"


                    #changing a piece outcome

            main_selector="quit"