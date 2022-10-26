from PySide2.QtCore import QAbstractTableModel
from PySide2.QtCore import *
from ..databases.database import DatabaseManager



class Datamodel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        #sum calculation
        self.parent = parent
        self.databasemanager = DatabaseManager()
        self.sum_weight = 0
        self.sum_recycle_weight = 0
        self.sum_energy_recovery_weight = 0
        self.sum_residual_waste_weight = 0
        self.recycling_rate = 0
        self.recovery_rate = 0
        self.residual_rate = 0
        
        # the solvent data ...
        self.header_component_test = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
        self.header_database_product = ['Name product', 'Name author product', 'Firstname author product']
        self.header_database_component = ['Name component','Name material','Type material', 'Weight (grams/piece)','Is it pollutant ?','Number of pieces', 'Comment component']
        self.header_database_component_scenario_rate = ['Ref','id_comp','Name component','Recycle Weight (grams/piece)','Energy recovery Weight (grams/piece)', 'Residual waste Weight (grams/piece)','Is it pollutant ?','Number of pieces', 'Comment component']
        self.header_database_component_scenario_rate_mixed = ['Ref','id_comp','Name component', 'Gain 1', 'Gain 2', 'Relative Weight', 'Residual waste Weight', 'Is it pollutant ?','Scenario','Recycle Weight (grams/piece)','Energy recovery Weight (grams/piece)', 'Residual waste Weight (grams/piece)','Shredding - Recycle Weight (grams/piece)','Shredding - Energy recovery Weight (grams/piece)', 'Shredding - Residual waste Weight (grams/piece)', 'Number of pieces', 'Comment component']
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
        if(type_database.lower() == "product"):
            #--- select
            self.all_product_form = self.databasemanager.productdatabase.get_all_product()
            for _, value in self.all_product_form.items():
                self.data_list.append((ref_cmp,value['name_product'],value['nameauthor_product'],value['firstname_product'],' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1
        elif(type_database.lower() == "component"):
            #--- select
            self.all_component_form = self.databasemanager.composedatabase.get_all_component_and_product()
            for _, value in self.all_component_form.items():
                name_component = value['one_component']['name_component']
                name_material = value['material_of_component']['name']
                Type_material = value['material_of_component']['type_material']
                Weight = str(value['one_component']['weight_component']).replace(",", ".")
                pollutant = str(value['material_of_component']['pollutant_material'])
                if(pollutant.lower() == "false"):
                    pollutant = "No"
                else:
                    pollutant = "Yes"
                number_of_pieces =  value['one_compose']['piecenumber_component']
                Comment_component = value['one_component']['comment_component']
                Name_Product = value['one_product']['name_product']
                self.data_list.append((ref_cmp,name_component,name_material,Name_Product,Type_material,Weight,pollutant,number_of_pieces,Comment_component,' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1                
        elif(type_database.lower() == "material"):
            #--- select
            self.all_material_form = self.databasemanager.materialdatabase.get_all_material()
            for _, value in self.all_material_form.items():
                if(value['pollutant_material'].lower() == "false"):
                    pollutant = "No"
                else:
                    pollutant = "Yes"
                self.data_list.append((ref_cmp,value['type_material'],value['name'],pollutant,value['recdis_material'],value['enerdis_material'],value['wastedis_material'],value['recshr_material'],value['enershr_material'],value['wasteshr_material'],value['price_material'],' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1
        elif(type_database.lower()=="directive"):
            #--- select
            self.all_directive_form = self.databasemanager.directivedatabase.get_all_directive()
            for _, value in self.all_directive_form.items():
                self.data_list.append((ref_cmp,value['name'],value['comment'],value['dismantling_recycling_rate'],value['dismantling_recovery_rate'],value['dismantling_residual_waste_rate'],value['shredding_recycling_rate'],value['shredding_recovery_rate'],value['shredding_residual_waste_rate'],value['mixed_recycling_rate'],value['mixed_recovery_rate'],value['mixed_residual_waste_rate'],' '))
                dict_ligne_database[ref_cmp] = value
                ref_cmp = ref_cmp + 1
                
        self.parent.dict_ligne_database = dict_ligne_database
        #return result       
        return self.data_list
        
    def getdata_product(self):
        """
        gets the data list of all products
        """
        self.data_list = []
        #---product to select
        self.all_product_form = self.databasemanager.productdatabase.get_all_product()
        for key, value in self.all_product_form.items():
            self.data_list.append((value['name_product'],value['nameauthor_product'],value['firstname_product']))
        return self.data_list
    
    def getdata_component(self,id_product): #Unused
        self.data_list = []
        #---product component of product selected
        self.all_component_form = self.databasemanager.composedatabase.get_component_by_product(id_product)
        for _, value in self.all_component_form.items():
            name_component = value['one_component']['name_component']
            name_material = value['material_of_component']['name']
            Type_material = value['material_of_component']['type_material']
            Weight = value['one_component']['weight_component']
            pollutant = str(value['material_of_component']['pollutant_material'])
            if(pollutant.lower()=="false"):
                pollutant = "No"
            else:
                pollutant = "Yes"
            number_of_pieces =  value['one_compose']['piecenumber_component']
            Comment_component = value['one_component']['comment_component']
            self.data_list.append((name_component, name_material, Type_material, Weight, pollutant, number_of_pieces, Comment_component))
        return self.data_list
    
    def getdata_component_scenario_rate(self,id_product,type_scenario: str):
        self.data_list = []
        #---product component of product selected
        self.all_component_form = self.databasemanager.composedatabase.get_component_by_product(id_product)
        #init 
        cmp_index = 0
        recycle_weight = 0
        energy_recovery_weight = 0
        residual_waste_weight = 0
        self.sum_weight_mixed = 0
        self.sum_weight = 0
        self.sum_recycle_weight = 0
        self.sum_energy_recovery_weight = 0
        self.sum_residual_waste_weight = 0
        self.recycling_rate = 0
        self.recovery_rate = 0
        self.residual_rate = 0    
        #set value of self.sum_weight_mixed
        for _, value in self.all_component_form.items():
            Weight = str(value['one_component']['weight_component']).replace(",", ".")
            self.sum_weight_mixed = float(self.sum_weight_mixed) + float(Weight)
        #set values of all
        for _, value in self.all_component_form.items():
            component_code = value['one_component']['code']
            name_component = value['one_component']['name_component']
            Weight = str(value['one_component']['weight_component']).replace(",", ".")
            pollutant = str(value['material_of_component']['pollutant_material'])
            if(pollutant.lower() == "false"):
                pollutant = "No"
            else:
                pollutant = "Yes"
            number_of_pieces =  value['one_compose']['piecenumber_component']
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
            
            if(type_scenario.lower() == "dismantling"): # case dismantling
                recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                self.sum_weight = float(self.sum_weight) + float(Weight)
                self.sum_recycle_weight = float(self.sum_recycle_weight) + float(recycle_weight)
                self.sum_energy_recovery_weight = float(self.sum_energy_recovery_weight) + float(energy_recovery_weight)
                self.sum_residual_waste_weight = float(self.sum_residual_waste_weight) + float(residual_waste_weight)
            elif(type_scenario.lower() == "shredding"): # case shredding
                if(pollutant == "Yes"):
                    recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                    energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                    residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                else:
                    recycle_weight = ((float(recshr_material) * float(Weight)) / 100)
                    energy_recovery_weight = ((float(enershr_material) * float(Weight)) / 100)
                    residual_waste_weight = ((float(wasteshr_material) * float(Weight)) / 100)
                self.sum_weight = float(self.sum_weight) + float(Weight)
                self.sum_recycle_weight = float(self.sum_recycle_weight) + float(recycle_weight)
                self.sum_energy_recovery_weight = float(self.sum_energy_recovery_weight) + float(energy_recovery_weight)
                self.sum_residual_waste_weight = float(self.sum_residual_waste_weight) + float(residual_waste_weight)
            elif(type_scenario.lower() == "mixed"): # case mixed
                #--- for dismantling ---
                recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                #--- for shredding ---
                if(pollutant == "Yes"):
                    recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                    energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                    residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                    gain_1=0
                    gain_2=0
                else:
                    recycle_weight = ((float(recshr_material) * float(Weight)) / 100)
                    energy_recovery_weight = ((float(enershr_material) * float(Weight)) / 100)
                    residual_waste_weight = ((float(wasteshr_material) * float(Weight)) / 100)
                    gain_1 = (float(recdis_material) - float(recshr_material))/100
                    gain_2 = ((float(recdis_material) + float(enerdis_material)) - (float(recshr_material) + float(enershr_material)))/100
                #set values for shredding
                recycle_weight_shredding = recycle_weight
                energy_recovery_weight_shredding = energy_recovery_weight
                residual_waste_weight_shredding = residual_waste_weight
                # --- get value of relative weight
                relative_weight = 0
                if(float(self.sum_weight_mixed) > 0):
                    relative_weight = round(float(Weight)/float(self.sum_weight_mixed) * 100, 1)
                relative_weight = str(relative_weight)+"%"
                #by default select the best scenario or applied scenario selected
                if scenario == "Dismantling":
                    recycle_weight = ((float(recdis_material) * float(Weight)) / 100)
                    energy_recovery_weight = ((float(enerdis_material) * float(Weight)) / 100)
                    residual_waste_weight = ((float(wastedis_material) * float(Weight)) / 100)
                else:
                    recycle_weight = ((float(recshr_material) * float(Weight)) / 100)
                    energy_recovery_weight = ((float(enershr_material) * float(Weight)) / 100)
                    residual_waste_weight = ((float(wasteshr_material) * float(Weight)) / 100)
                
                Residual_waste_Weight_most = residual_waste_weight
                self.sum_weight = float(self.sum_weight) + float(Weight)
                self.sum_recycle_weight = float(self.sum_recycle_weight) + float(recycle_weight)
                self.sum_energy_recovery_weight = float(self.sum_energy_recovery_weight) + float(energy_recovery_weight)
                self.sum_residual_waste_weight = float(self.sum_residual_waste_weight) + float(residual_waste_weight)
            #add data 
            if(type_scenario.lower() == "dismantling" or type_scenario.lower()=="shredding"): #for dismantling and shredding
                self.data_list.append((component_code, name_component, recycle_weight, energy_recovery_weight, residual_waste_weight, pollutant, number_of_pieces, Comment_component))
            elif(type_scenario.lower() == "mixed"): #for mixed
                self.data_list.append((component_code, name_component, gain_1, gain_2, relative_weight,Residual_waste_Weight_most, pollutant,scenario, recycle_weight, energy_recovery_weight, residual_waste_weight, recycle_weight_shredding, energy_recovery_weight_shredding, residual_waste_weight_shredding, number_of_pieces, Comment_component))
            #increment    
            cmp_index = cmp_index + 1
        if(float(self.sum_weight) > 0):
            self.recycling_rate = round((float(self.sum_recycle_weight)*100)/float(self.sum_weight))
            self.recovery_rate = round(((float(self.sum_energy_recovery_weight) + float(self.sum_recycle_weight))*100)/float(self.sum_weight))
            self.residual_rate = round((float(self.sum_residual_waste_weight)*100)/float(self.sum_weight))
        else:
            self.recycling_rate = 0
            self.recovery_rate = 0
            self.residual_rate = 0
        self.data_list = [(i + 1, )+x for i, x in enumerate(sorted(self.data_list, key = lambda u : u[0]))]
        return self.data_list

    def getdata_hotspots(self, id_product, type_hotspots: str):
        self.data_list_hotspots = []
        data_list_mixed = self.getdata_component_scenario_rate(id_product,"mixed")
        dlhs11=[]
        dlhs12=[]
        for tuple_mixed in data_list_mixed:
            ref = int(tuple_mixed[0])
            name_component = tuple_mixed[2]
            gain_1 = tuple_mixed[3]
            relative_weight = tuple_mixed[5]
            is_it_pollutant = tuple_mixed[7]
            dismantling_residual_waste_weight = tuple_mixed[11]
            shredding_residual_waste_weight = tuple_mixed[14]
            number_of_pieces = tuple_mixed[15]
            #case hotspots_1
            if(type_hotspots.lower() == "hotspots_1"):
                gain_1_relative_weight = round(float(gain_1) * float(str(relative_weight).replace("%", "")), 2)
                if is_it_pollutant == "Yes":
                    dlhs12.append((ref, name_component, is_it_pollutant, gain_1, relative_weight, gain_1_relative_weight))
                else:
                    dlhs11.append((ref, name_component, is_it_pollutant, gain_1, relative_weight, gain_1_relative_weight))
            elif(type_hotspots.lower() == "hotspots_2"):
                self.data_list_hotspots.append((ref, name_component, is_it_pollutant, dismantling_residual_waste_weight, dismantling_residual_waste_weight, shredding_residual_waste_weight, number_of_pieces))
        # sorting the data
        if type_hotspots.lower() == "hotspots_1":
            #hotspots 1 => sorting by decreasing order of the gain1*rel weight
            dlhs11 = sorted(dlhs11, key = lambda x : (-x[-1], x[0]))
            dlhs12 = sorted(dlhs12, key = lambda x : x[0])
            self.data_list_hotspots = dlhs11+dlhs12
            self.data_list_hotspots = [x[:-1]+(str(x[-1])+"%",) for x in self.data_list_hotspots]
        elif type_hotspots.lower() == "hotspots_2":
            self.data_list_hotspots = sorted(self.data_list_hotspots, key = lambda x : x[3], reverse=True)
        return self.data_list_hotspots
       
    def get_data_guidelines(self):
        data_list = []
        for _, item in self.databasemanager.guidelinesdatabase.get_all_guidelines().items():
            data_list.append((item["guideline_number"], item["name"]))
        return [(elem[1], ) for elem in sorted(data_list, key = lambda x:x[0])]
