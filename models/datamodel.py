import sys
from PySide2.QtCore import QAbstractTableModel

import operator
from PySide2.QtCore import *
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QGridLayout, QComboBox,
    QWidget, QTableView, QWidget
)
from ..databases.database import DatabaseManager

databasemanager = DatabaseManager()

class Datamodel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        #sum calculation
        self.parent = parent
        self.sum_weight = 0
        self.sum_Recycle_weight = 0
        self.sum_Energy_recovery_weight = 0
        self.sum_Residual_waste_weight = 0
        self.recycling_rate = 0
        self.recovery_rate = 0
        self.residual_rate = 0
        
        # the solvent data ...
        self.header_component_test = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
        self.header_database_product = ['Name product', 'Name author product', 'Firstname author product']
        self.header_database_component = ['Name component','Name material','Type material', 'Weight (grams/piece)','Is it pollutant ?','Number of pieces', 'Comment component']
        self.header_database_component_scenario_rate = ['Ref','Name component','Recycle Weight (grams/piece)','Energy recovery Weight (grams/piece)', 'Residual waste Weight (grams/piece)','Is it pollutant ?','Number of pieces', 'Comment component']
        self.header_database_component_scenario_rate_mixed = ['Ref','id_comp','Name component', 'Gain 1', 'Gain 2', 'Relative Weight', 'Residual waste Weight', 'Is it pollutant ?','Scenario','Dismantling - Recycle Weight (grams/piece)','Dismantling - Energy recovery Weight (grams/piece)', 'Dismantling - Residual waste Weight (grams/piece)','Shredding - Recycle Weight (grams/piece)','Shredding - Energy recovery Weight (grams/piece)', 'Shredding - Residual waste Weight (grams/piece)', 'Number of pieces', 'Comment component']
        self.header_hotspots_1 = ['Ref','Name component','Is it pollutant ?','Gain 1','Relative weight','Gain 1 * Relative weight']
        self.header_hotspots_2 = ['Ref', 'Name component', 'Is it pollutant ?', 'Residual waste Weight','Dismantling - Residual waste Weight (grams/piece)','Shredding - Residual waste Weight (grams/piece)','Number of pieces']
        self.header_database_product_manage = ['Ref','Name product', 'Name author product', 'Firstname author product','Action']
        self.header_database_component_manage = ['Ref','Name component','Name material','Name Product','Type material', 'Weight (grams/piece)','Is it pollutant ?','Number of pieces', 'Comment component','Action']
        self.header_database_material_manage = ['Ref','Type material','Name material','Is it pollutant ?','Dismantling - Recycling potential','Dismantling - Energy recovery potential','Dismantling - Residual waste potential','Shredding - Recycling potential','Shredding - Energy recovery potential','Shredding - Residual waste potential','Price material','Action']
        self.header_database_directive_manage = ['Ref','Directive title','Directive comment','Dismantling recycling rate','Dismantling recovery rate','Dismantling residual waste rate','Shredding recycling rate','Shredding recovery rate','Shredding residual waste rate','Mixed recycling rate','Mixed recovery rate','Mixed residual waste rate','Action']
    
    def getdata_database(self,type_database):
        """
        Makes the datamodels for the databases tab (tab that makes us see what we can display in the tab
        """
        self.data_list = []
        ref_cmp = 0
        dict_ligne_database = dict()
        if(type_database.lower()=="product"):
            #--- select
            self.all_product_form = databasemanager.productdatabase.get_all_product()
            for key, value in self.all_product_form.items():
                self.data_list.append((ref_cmp,value['name_product'],value['nameauthor_product'],value['firstname_product'],' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1
        elif(type_database.lower()=="component"):
            #--- select
            self.all_component_form = databasemanager.composedatabase.get_all_component_and_product()
            for key, value in self.all_component_form.items():
                component_code = value['one_component']['code']
                Id_component = value['one_component']['id_component']
                Name_component = value['one_component']['name_component']
                Name_material = value['material_of_component']['name_material']
                Type_material = value['material_of_component']['type_material']
                Weight = str(value['one_component']['weight_component']).replace(",", ".")
                Pollutant = str(value['material_of_component']['pollutant_material'])
                if(Pollutant.lower()=="false"):
                    Pollutant = "No"
                else:
                    Pollutant = "Yes"
                Number_of_pieces =  value['one_compose']['piecenumber_component']
                Comment_component = value['one_component']['comment_component']
                Name_Product = value['one_product']['name_product']
                self.data_list.append((ref_cmp,Name_component,Name_material,Name_Product,Type_material,Weight,Pollutant,Number_of_pieces,Comment_component,' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1                
        elif(type_database.lower()=="material"):
            #--- select
            self.all_material_form = databasemanager.materialdatabase.get_all_material()
            for key, value in self.all_material_form.items():
                if(value['pollutant_material'].lower()=="false"):
                    Pollutant = "No"
                else:
                    Pollutant = "Yes"
                self.data_list.append((ref_cmp,value['type_material'],value['name_material'],Pollutant,value['recdis_material'],value['enerdis_material'],value['wastedis_material'],value['recshr_material'],value['enershr_material'],value['wasteshr_material'],value['price_material'],' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1
        elif(type_database.lower()=="directive"):
            #--- select
            self.all_directive_form = databasemanager.directivedatabase.get_all_directive()
            for key, value in self.all_directive_form.items():
                self.data_list.append((ref_cmp,value['directive_title'],value['directive_comment'],value['dismantling_recycling_rate'],value['dismantling_recovery_rate'],value['dismantling_residual_waste_rate'],value['shredding_recycling_rate'],value['shredding_recovery_rate'],value['shredding_residual_waste_rate'],value['mixed_recycling_rate'],value['mixed_recovery_rate'],value['mixed_residual_waste_rate'],' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1
                
        #set value parent.dict_ligne_database
        self.parent.dict_ligne_database = dict_ligne_database
        #return result       
        return self.data_list
        
    def getdata_product(self):
        """
        gets the data list of all products
        """
        self.data_list = []
        #---product to select
        self.all_product_form = databasemanager.productdatabase.get_all_product()
        for key, value in self.all_product_form.items():
            self.data_list.append((value['name_product'],value['nameauthor_product'],value['firstname_product']))
        return self.data_list
    
    def getdata_component(self,id_product): #Unused
        self.data_list = []
        #---product component of product selected
        self.all_component_form = databasemanager.composedatabase.get_component_by_product(id_product)
        #print("getdata_component",self.all_component_form)
        """
        eg. result self.all_component_form:
        {
            ("resicled_compose", "1657178236.9446831657206274.284218"): {
                "one_compose": {
                    "id_product": 1657178236.944683,
                    "id_component": 1657206274.284218,
                    "piecenumber_component": "6",
                    "database": "resicled_compose",
                    "code": "1657178236.9446831657206274.284218",
                    "exchanges": [],
                },
                "one_product": {
                    "id_product": 1657178236.944683,
                    "name_product": "product 3",
                    "nameauthor_product": "",
                    "firstname_product": "",
                    "database": "resicled_product",
                    "code": "1657178236.944683",
                    "exchanges": [],
                },
                "one_component": {
                    "id_component": 1657206274.284218,
                    "id_material": 20,
                    "name_component": "component 1",
                    "weight_component": "15",
                    "comment_component": "test insert 1",
                    "database": "resicled_component",
                    "code": "1657206274.284218",
                    "exchanges": [],
                },
                "material_of_component": {
                    "id_material": 20,
                    "type_material": "Metals",
                    "name_material": "Aluminium",
                    "recdis_material": "93,00",
                    "enerdis_material": "0,00",
                    "wastedis_material": "7,00",
                    "recshr_material": "91,00",
                    "enershr_material": "0,00",
                    "wasteshr_material": "9,00",
                    "price_material": 370,
                    "pollutant_material": "false",
                    "database": "resicled_material",
                    "code": "20",
                    "exchanges": [],
                },
            }
        }
        """        
        for key, value in self.all_component_form.items():
            Name_component = value['one_component']['name_component']
            Name_material = value['material_of_component']['name_material']
            Type_material = value['material_of_component']['type_material']
            Weight = value['one_component']['weight_component']
            Pollutant = str(value['material_of_component']['pollutant_material'])
            if(Pollutant.lower()=="false"):
                Pollutant = "No"
            else:
                Pollutant = "Yes"
            Number_of_pieces =  value['one_compose']['piecenumber_component']
            Comment_component = value['one_component']['comment_component']
            self.data_list.append((Name_component, Name_material, Type_material, Weight, Pollutant, Number_of_pieces, Comment_component))
        return self.data_list
    
    def getdata_component_scenario_rate(self,id_product,type_scenario: str):
        self.data_list = []
        #---product component of product selected
        self.all_component_form = databasemanager.composedatabase.get_component_by_product(id_product)
        #print("getdata_component",self.all_component_form)
        """
        eg. result self.all_component_form:
        {
            ("resicled_compose", "1657178236.9446831657206274.284218"): {
                "one_compose": {
                    "id_product": 1657178236.944683,
                    "id_component": 1657206274.284218,
                    "piecenumber_component": "6",
                    "strategy_component" : "Dismantling",
                    "database": "resicled_compose",
                    "code": "1657178236.9446831657206274.284218",
                    "exchanges": [],
                },
                "one_product": {
                    "id_product": 1657178236.944683,
                    "name_product": "product 3",
                    "nameauthor_product": "",
                    "firstname_product": "",
                    "database": "resicled_product",
                    "code": "1657178236.944683",
                    "exchanges": [],
                },
                "one_component": {
                    "id_component": 1657206274.284218,
                    "id_material": 20,
                    "name_component": "component 1",
                    "weight_component": "15",
                    "comment_component": "test insert 1",
                    "database": "resicled_component",
                    "code": "1657206274.284218",
                    "exchanges": [],
                },
                "material_of_component": {
                    "id_material": 20,
                    "type_material": "Metals",
                    "name_material": "Aluminium",
                    "recdis_material": "93,00",
                    "enerdis_material": "0,00",
                    "wastedis_material": "7,00",
                    "recshr_material": "91,00",
                    "enershr_material": "0,00",
                    "wasteshr_material": "9,00",
                    "price_material": 370,
                    "pollutant_material": "false",
                    "database": "resicled_material",
                    "code": "20",
                    "exchanges": [],
                },
            }
        }
        """  
        
        #set dict_scenario_mixed case scenario mixed. Content component_code and type scenario
        dict_scenario_mixed = dict() 
        if(type_scenario.lower()=="mixed" and (0 in self.parent.combo_scenario)):
            for key_ligne, widget_obj in self.parent.combo_scenario.items():
                currentdata_selected = widget_obj.currentData()
                currenttext_selected = widget_obj.currentText()
                component_code = str(currentdata_selected['one_component']['code'])
                dict_scenario_mixed[component_code] = currenttext_selected
            
        
        #init
        combo_scenario = dict() 
        cmp_index = 0
        Recycle_weight = 0
        Energy_recovery_weight = 0
        Residual_waste_weight = 0
        self.sum_weight_mixed = 0
        self.sum_weight = 0
        self.sum_Recycle_weight = 0
        self.sum_Energy_recovery_weight = 0
        self.sum_Residual_waste_weight = 0
        self.recycling_rate = 0
        self.recovery_rate = 0
        self.residual_rate = 0    
        #set value of self.sum_weight_mixed
        for key, value in self.all_component_form.items():
            Weight = str(value['one_component']['weight_component']).replace(",", ".")
            self.sum_weight_mixed = float(self.sum_weight_mixed) + float(Weight)
        #set values of all
        for key, value in self.all_component_form.items():
            component_code = value['one_component']['code']
            Name_component = value['one_component']['name_component']
            Name_material = value['material_of_component']['name_material']
            Type_material = value['material_of_component']['type_material']
            Weight = str(value['one_component']['weight_component']).replace(",", ".")
            Pollutant = str(value['material_of_component']['pollutant_material'])
            if(Pollutant.lower()=="false"):
                Pollutant = "No"
            else:
                Pollutant = "Yes"
            Number_of_pieces =  value['one_compose']['piecenumber_component']
            Comment_component = value['one_component']['comment_component']
            #for dismantling
            recdis_material = str(value['material_of_component']['recdis_material']).replace(",", ".")
            enerdis_material = str(value['material_of_component']['enerdis_material']).replace(",", ".")
            wastedis_material = str(value['material_of_component']['wastedis_material']).replace(",", ".")
            #for shredding
            recshr_material = str(value['material_of_component']['recshr_material']).replace(",", ".")
            enershr_material = str(value['material_of_component']['enershr_material']).replace(",", ".")
            wasteshr_material = str(value['material_of_component']['wasteshr_material']).replace(",", ".")
            #for mixed
            recdis_material = str(value['material_of_component']['recdis_material']).replace(",", ".")
            enerdis_material = str(value['material_of_component']['enerdis_material']).replace(",", ".")
            wastedis_material = str(value['material_of_component']['wastedis_material']).replace(",", ".")
            recshr_material = str(value['material_of_component']['recshr_material']).replace(",", ".")
            enershr_material = str(value['material_of_component']['enershr_material']).replace(",", ".")
            wasteshr_material = str(value['material_of_component']['wasteshr_material']).replace(",", ".")
            scenario = value["one_compose"]["strategy_component"]
            
            if(type_scenario.lower()=="dismantling"): # case dismantling
                Recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                Energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                Residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                self.sum_weight = float(self.sum_weight) + float(Weight)
                self.sum_Recycle_weight = float(self.sum_Recycle_weight) + float(Recycle_weight)
                self.sum_Energy_recovery_weight = float(self.sum_Energy_recovery_weight) + float(Energy_recovery_weight)
                self.sum_Residual_waste_weight = float(self.sum_Residual_waste_weight) + float(Residual_waste_weight)
            elif(type_scenario.lower()=="shredding"): # case shredding
                if(Pollutant == "Yes"):
                    Recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                    Energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                    Residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                else:
                    Recycle_weight = ((float(recshr_material) * float(Weight)) / 100)
                    Energy_recovery_weight = ((float(enershr_material) * float(Weight)) / 100)
                    Residual_waste_weight = ((float(wasteshr_material) * float(Weight)) / 100)
                self.sum_weight = float(self.sum_weight) + float(Weight)
                self.sum_Recycle_weight = float(self.sum_Recycle_weight) + float(Recycle_weight)
                self.sum_Energy_recovery_weight = float(self.sum_Energy_recovery_weight) + float(Energy_recovery_weight)
                self.sum_Residual_waste_weight = float(self.sum_Residual_waste_weight) + float(Residual_waste_weight)
            elif(type_scenario.lower()=="mixed"): # case mixed
                #--- for dismantling ---
                Recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                Energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                Residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                #set values for dismantling
                Recycle_weight_dismantling = Recycle_weight
                Energy_recovery_weight_dismantling = Energy_recovery_weight
                Residual_waste_weight_dismantling = Residual_waste_weight
                #--- for shredding ---
                if(Pollutant == "Yes"):
                    Recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                    Energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                    Residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                    gain_1=0
                    gain_2=0
                else:
                    Recycle_weight = ((float(recshr_material) * float(Weight)) / 100)
                    Energy_recovery_weight = ((float(enershr_material) * float(Weight)) / 100)
                    Residual_waste_weight = ((float(wasteshr_material) * float(Weight)) / 100)
                    gain_1 = (float(recdis_material) - float(recshr_material))/100
                    gain_2 = ((float(recdis_material) + float(enerdis_material)) - (float(recshr_material) + float(enershr_material)))/100
                
                    
                #set values for shredding
                Recycle_weight_shredding = Recycle_weight
                Energy_recovery_weight_shredding = Energy_recovery_weight
                Residual_waste_weight_shredding = Residual_waste_weight
                # --- get value of relative weight
                relative_weight = 0
                if(float(self.sum_weight_mixed)>0):
                    relative_weight = round(float(Weight)/float(self.sum_weight_mixed) * 100,1)
                relative_weight = str(relative_weight)+"%"
                
                #by default select the best scenario or applied scenario selected
                if scenario == "Dismantling":
                    Residual_waste_Weight_most = Residual_waste_weight_dismantling
                    self.sum_weight = float(self.sum_weight) + float(Weight)
                    self.sum_Recycle_weight = float(self.sum_Recycle_weight) + float(Recycle_weight_dismantling)
                    self.sum_Energy_recovery_weight = float(self.sum_Energy_recovery_weight) + float(Energy_recovery_weight_dismantling)
                    self.sum_Residual_waste_weight = float(self.sum_Residual_waste_weight) + float(Residual_waste_weight_dismantling)
                else:
                    Residual_waste_Weight_most = Residual_waste_weight_shredding
            
                    self.sum_weight = float(self.sum_weight) + float(Weight)
                    self.sum_Recycle_weight = float(self.sum_Recycle_weight) + float(Recycle_weight_shredding)
                    self.sum_Energy_recovery_weight = float(self.sum_Energy_recovery_weight) + float(Energy_recovery_weight_shredding)
                    self.sum_Residual_waste_weight = float(self.sum_Residual_waste_weight) + float(Residual_waste_weight_shredding)
                    
            
                """
                self.sum_weight = float(self.sum_weight) + float(Weight)
                self.sum_Recycle_weight = float(self.sum_Recycle_weight) + float(Recycle_weight)
                self.sum_Energy_recovery_weight = float(self.sum_Energy_recovery_weight) + float(Energy_recovery_weight)
                self.sum_Residual_waste_weight = float(self.sum_Residual_waste_weight) + float(Residual_waste_weight)
                """
            
            #add data 
            if(type_scenario.lower()=="dismantling" or type_scenario.lower()=="shredding"): #for dismantling and shredding
                self.data_list.append((component_code,Name_component, Recycle_weight, Energy_recovery_weight, Residual_waste_weight, Pollutant, Number_of_pieces, Comment_component))
            elif(type_scenario.lower()=="mixed"): #for mixed
                self.data_list.append((component_code,Name_component, gain_1, gain_2, relative_weight,Residual_waste_Weight_most, Pollutant,scenario, Recycle_weight_dismantling, Energy_recovery_weight_dismantling, Residual_waste_weight_dismantling, Recycle_weight_shredding, Energy_recovery_weight_shredding, Residual_waste_weight_shredding, Number_of_pieces, Comment_component))
            #increment    
            cmp_index = cmp_index + 1
            
        if(float(self.sum_weight)>0):
            self.recycling_rate = round((float(self.sum_Recycle_weight)*100)/float(self.sum_weight))
            self.recovery_rate = round(((float(self.sum_Energy_recovery_weight) + float(self.sum_Recycle_weight))*100)/float(self.sum_weight))
            self.residual_rate = round((float(self.sum_Residual_waste_weight)*100)/float(self.sum_weight))
        else:
            self.recycling_rate = 0
            self.recovery_rate = 0
            self.residual_rate = 0

         
        self.data_list = [(i+1,)+x for i,x in enumerate(sorted(self.data_list, key = lambda u : u[0]))]
        return self.data_list
    
    
    def getdata_hotspots(self,id_product, type_hotspots: str):
        #['Ref','Name component', 'Gain 1', 'Gain 2', 'Relative Weight', 'Is it pollutant ?','Scenario','Dismantling - Recycle Weight (grams/piece)','Dismantling - Energy recovery Weight (grams/piece)', 'Dismantling - Residual waste Weight (grams/piece)','Shredding - Recycle Weight (grams/piece)','Shredding - Energy recovery Weight (grams/piece)', 'Shredding - Residual waste Weight (grams/piece)', 'Number of pieces', 'Comment component']
        self.data_list_hotspots = []
        data_list_mixed = self.getdata_component_scenario_rate(id_product,"mixed")
        dlhs11=[]
        dlhs12=[]
        for tuple_mixed in data_list_mixed:
            Ref = int(tuple_mixed[0])
            id_comp = tuple_mixed[1]
            Name_component = tuple_mixed[2]
            Gain_1 = tuple_mixed[3]
            Gain_2 = tuple_mixed[4]
            Relative_Weight = tuple_mixed[5]
            Residual_waste_Weight = tuple_mixed[6]
            Is_it_pollutant = tuple_mixed[7]
            Scenario = tuple_mixed[8]
            Dismantling_Recycle_Weight = tuple_mixed[9]
            Dismantling_Energy_recovery_Weight = tuple_mixed[10]
            Dismantling_Residual_waste_Weight = tuple_mixed[11]
            Shredding_Recycle_Weight = tuple_mixed[12]
            Shredding_Energy_recovery_Weight = tuple_mixed[13]
            Shredding_Residual_waste_Weight = tuple_mixed[14]
            Number_of_pieces = tuple_mixed[15]
            Comment_component = tuple_mixed[16]
            
            #case hotspots_1
            if(type_hotspots.lower()=="hotspots_1"): #["Id","Name component","Is it pollutant ?","Gain 1","Relative weight","Gain 1 * Relative weight"]
                Gain_1_Relative_weight = round(float(Gain_1) * float(str(Relative_Weight).replace("%", "")),2)
                if Is_it_pollutant=="Yes":
                    dlhs12.append((Ref, Name_component, Is_it_pollutant, Gain_1, Relative_Weight, Gain_1_Relative_weight))
                else:
                    dlhs11.append((Ref, Name_component, Is_it_pollutant, Gain_1, Relative_Weight, Gain_1_Relative_weight))
            elif(type_hotspots.lower()=="hotspots_2"): #["Ref", "Name component", "Is it pollutant ?","Residual waste Weight (grams/piece)","Number of pieces"]
                if Is_it_pollutant=="Yes":
                    Residual_waste_Weight = Dismantling_Residual_waste_Weight
                else:
                    current_compose = list(databasemanager.composedatabase.get_compose_by_component(id_comp).values())[0]
                    if current_compose["strategy_component"]=="Shredding":
                        Residual_waste_Weight = Shredding_Residual_waste_Weight
                    else:
                        Residual_waste_Weight = Dismantling_Residual_waste_Weight
                self.data_list_hotspots.append((Ref, Name_component, Is_it_pollutant, Residual_waste_Weight, Dismantling_Residual_waste_Weight, Shredding_Residual_waste_Weight, Number_of_pieces))

        # sorting the data
        if type_hotspots.lower()=="hotspots_1":
            #hotspots 1 => sorting by decreasing order of the gain1*rel weight
            dlhs11 = sorted(dlhs11, key = lambda x : (-x[-1],x[0]))
            dlhs12 = sorted(dlhs12, key = lambda x : x[0])
            self.data_list_hotspots= dlhs11+dlhs12
            self.data_list_hotspots = [x[:-1]+(str(x[-1])+"%",) for x in self.data_list_hotspots]
        elif type_hotspots.lower()=="hotspots_2":
            self.data_list_hotspots = sorted(self.data_list_hotspots, key = lambda x : x[3], reverse=True)

        return self.data_list_hotspots
       
    def get_data_guidelines(self):
        data_list=[]
        for _, item in databasemanager.guidelinesdatabase.get_all_guidelines().items():
            data_list.append((item["guideline_number"],item["guideline_name"]))
        return [(elem[1],) for elem in sorted(data_list,key = lambda x:x[0])]
        
    def getdata_component_test(self):
        # use numbers for numeric data to sort properly
        self.data_list = [
            ('ACETIC ACID', 117.9, 16.7, 1.049),
            ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
            ('ACETONE', 56.3, -94.7, 0.791),
            ('ACETONITRILE', 81.6, -43.8, 0.786),
            ('ANISOLE', 154.2, -37.0, 0.995),
            ('BENZYL ALCOHOL', 205.4, -15.3, 1.045),
            ('BENZYL BENZOATE', 323.5, 19.4, 1.112),
            ('BUTYL ALCOHOL NORMAL', 117.7, -88.6, 0.81),
            ('BUTYL ALCOHOL SEC', 99.6, -114.7, 0.805),
            ('BUTYL ALCOHOL TERTIARY', 82.2, 25.5, 0.786),
            ('CHLOROBENZENE', 131.7, -45.6, 1.111),
            ('CYCLOHEXANE', 80.7, 6.6, 0.779),
            ('CYCLOHEXANOL', 161.1, 25.1, 0.971),
            ('CYCLOHEXANONE', 155.2, -47.0, 0.947),
            ('DICHLOROETHANE 1 2', 83.5, -35.7, 1.246),
            ('DICHLOROMETHANE', 39.8, -95.1, 1.325),
            ('DIETHYL ETHER', 34.5, -116.2, 0.715),
            ('DIMETHYLACETAMIDE', 166.1, -20.0, 0.937),
            ('DIMETHYLFORMAMIDE', 153.3, -60.4, 0.944),
            ('DIMETHYLSULFOXIDE', 189.4, 18.5, 1.102),
            ('DIOXANE 1 4', 101.3, 11.8, 1.034),
            ('DIPHENYL ETHER', 258.3, 26.9, 1.066),
            ('ETHYL ACETATE', 77.1, -83.9, 0.902),
            ('ETHYL ALCOHOL', 78.3, -114.1, 0.789),
            ('ETHYL DIGLYME', 188.2, -45.0, 0.906),
            ('ETHYLENE CARBONATE', 248.3, 36.4, 1.321),
            ('ETHYLENE GLYCOL', 197.3, -13.2, 1.114),
            ('FORMIC ACID', 100.6, 8.3, 1.22),
            ('HEPTANE', 98.4, -90.6, 0.684),
            ('HEXAMETHYL PHOSPHORAMIDE', 233.2, 7.2, 1.027),
            ('HEXANE', 68.7, -95.3, 0.659),
            ('ISO OCTANE', 99.2, -107.4, 0.692),
            ('ISOPROPYL ACETATE', 88.6, -73.4, 0.872),
            ('ISOPROPYL ALCOHOL', 82.3, -88.0, 0.785),
            ('METHYL ALCOHOL', 64.7, -97.7, 0.791),
            ('METHYL ETHYLKETONE', 79.6, -86.7, 0.805),
            ('METHYL ISOBUTYL KETONE', 116.5, -84.0, 0.798),
            ('METHYL T-BUTYL ETHER', 55.5, -10.0, 0.74),
            ('METHYLPYRROLIDINONE N', 203.2, -23.5, 1.027),
            ('MORPHOLINE', 128.9, -3.1, 1.0),
            ('NITROBENZENE', 210.8, 5.7, 1.208),
            ('NITROMETHANE', 101.2, -28.5, 1.131),
            ('PENTANE', 36.1, ' -129.7', 0.626),
            ('PHENOL', 181.8, 40.9, 1.066),
            ('PROPANENITRILE', 97.1, -92.8, 0.782),
            ('PROPIONIC ACID', 141.1, -20.7, 0.993),
            ('PROPIONITRILE', 97.4, -92.8, 0.782),
            ('PROPYLENE GLYCOL', 187.6, -60.1, 1.04),
            ('PYRIDINE', 115.4, -41.6, 0.978),
            ('SULFOLANE', 287.3, 28.5, 1.262),
            ('TETRAHYDROFURAN', 66.2, -108.5, 0.887),
            ('TOLUENE', 110.6, -94.9, 0.867),
            ('TRIETHYL PHOSPHATE', 215.4, -56.4, 1.072),
            ('TRIETHYLAMINE', 89.5, -114.7, 0.726),
            ('TRIFLUOROACETIC ACID', 71.8, -15.3, 1.489),
            ('WATER', 100.0, 0.0, 1.0),
            ('XYLENES', 139.1, -47.8, 0.86)
        ]
        return self.data_list