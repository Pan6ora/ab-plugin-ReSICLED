import sys
from PySide2 import QtCore

import operator
from PySide2.QtCore import *
from ..databases.database import DatabaseManager

databasemanager = DatabaseManager()

class Datamodel(QAbstractTableModel):
    """
    A class that sets the info in databases that need to be printed as table
    """
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        # the solvent data ...
        self.header_component_test = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
        self.header_database_product = ['Name product', 'Name author product', 'Firstname author product']
        self.header_database_component = ['Name component','Name material','Type material', 'Weight (grams/piece)','Is it pollutant ?','Number of pieces', 'Comment component']
        self.header_dismantling = ["Name Component","Recycle weight (gr/piece)","Energy recovery weight (gr/piece)","Residual waste (gr/piece)","Number"]
        self.header_mixed = ["Name Component","Is it pollutant ?","Gain 1", "Gain 2", "Relative weight", "Result", "Recycle weight (g/piece)","Energy recovery weight (gr/piece)","Residual waste (gr/piece)","Number"]
        self.header_hotspots_1 = ["Id","Name","Pollutant","Gain 1","Relative weight","Gain 1*Relative weight"]
        self.header_hotspots_2 = ["Id", "Name", "Pollutant","Residual waste weight (g/piece)","Number of pieces"]

    def getdata_product(self):
        data_list = []
        #---product to select
        self.all_product_form = databasemanager.productdatabase.get_all_product()
        for key, value in self.all_product_form.items():
            data_list.append((value['name_product'],value['nameauthor_product'],value['firstname_product']))
        return data_list
    
    def getdata_component(self,id_product):
        """
        Sets the data for the list of products that are printed in input tab
        """
        data_list = []
        #---product to select
        self.all_component_form = databasemanager.composedatabase.get_component_by_product(id_product)
        print("getdata_component",self.all_component_form)
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
        for _, value in self.all_component_form.items():
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
            data_list.append((Name_component, Name_material, Type_material, Weight, Pollutant, Number_of_pieces, Comment_component))
        return data_list

    def getDismantling_data(self,id_product):
        """
        Sets the data for the dismantling tab table (including values)
        """
        dataList=[]
        print(databasemanager.composedatabase.get_compose_by_product(id_product))
        for _, value in databasemanager.composedatabase.get_component_by_product(id_product).items():
            calculations = DatabaseManager().computeComponentDismantling(value)
            dataList.append((value["one_component"]["name_component"],calculations[0],calculations[1],calculations[2],value["one_compose"]["piecenumber_component"]))
        return dataList

    def getShredding_data(self,id_product):
        data_list = []
        for _, value in databasemanager.composedatabase.get_component_by_product(id_product).items():
            calculations = DatabaseManager().computeComponentShredding(value)
            data_list.append((value["one_component"]["name_component"],calculations[0],calculations[1],calculations[2],value["one_compose"]["piecenumber_component"]))
        return data_list

    def get_mixed_data(self,id_product):
        data_list = []
        for _,value in databasemanager.composedatabase.get_component_by_product(id_product).items():
            pass

    def get_hotspot1_data(self,id_product):
        data_list=[]
        for key, value in enumerate(databasemanager.composedatabase.get_component_by_product(id_product).values()):
            gain = DatabaseManager().computeGain1(value)
            relative_weight = DatabaseManager().relativeWeight(value, databasemanager.composedatabase.get_component_by_product(id_product))
            data_list.append((key+1,value["one_component"]["name_component"],value["material_of_component"]["pollutant_material"],gain,relative_weight,gain*relative_weight))
        return sorted(data_list, key = lambda x :x[5], reverse=True)

    def get_hotspot2_data(self,id_product):
        data_list=[]
        for key, value in enumerate(databasemanager.composedatabase.get_component_by_product(id_product).values()):
            data_list.append((key+1,value["one_component"]["name_component"],value["material_of_component"]["pollutant_material"],DatabaseManager().computeComponentShredding(value)[2],value["one_compose"]["piecenumber_component"]))
        return sorted(data_list, key = lambda x : x[3], reverse=True)

    def getdata_component_test(self):
        """
        Test example function
        """
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