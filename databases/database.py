
from .materialdatabase import Materialdatabase
from .productdatabase import Productdatabase
from .composedatabase import Composedatabase
from .componentdatabase import Componentdatabase

class DatabaseManager():
    def __init__(self, parent=None):
        #super(DatabaseManager, self).__init__(parent)
        self.materialdatabase = Materialdatabase()
        self.productdatabase = Productdatabase()
        self.composedatabase = Composedatabase()
        self.componentdatabase = Componentdatabase()

    @classmethod
    def computeComponentDismantling(self,value : dict)-> tuple:
        """
        Database is the componentdatabase (so it has aMaterial database attribute)
        """
        component_weight = float(value["one_component"]["weight_component"])
        component_material = value["material_of_component"]
        return (component_weight*float(component_material["recdis_material"])/100,component_weight*float(component_material["enerdis_material"])/100,component_weight*float(component_material["wastedis_material"])/100)

    @classmethod
    def computeComponentShredding(self, value : dict) -> tuple:
        component_weight = float(value["one_component"]["weight_component"])
        component_material = value["material_of_component"]
        if component_material["pollutant_material"]=="true":
            # non pollutant
            return (component_weight*float(component_material["recdis_material"])/100,component_weight*float(component_material["enerdis_material"])/100,component_weight*float(component_material["wastedis_material"])/100)
        else:
            #pollutant
            return (component_weight*float(component_material["recshr_material"])/100,component_weight*float(component_material["enershr_material"])/100,component_weight*float(component_material["wasteshr_material"])/100)

    @classmethod
    def computeGain1(self, value : dict):
        if value["material_of_component"]["pollutant_material"]=="false":
            return (value["material_of_component"]["recdis_material"]-value["material_of_component"]["recshr_material"])/100
        else:
            return 0

    @classmethod
    def computeGain2(self,value : dict):
        if value["material_of_component"]["pollutant_material"]=="false":
            return (value["material_of_component"]["recdis_material"]+value["material_of_component"]["enerdis_material"]-value["material_of_component"]["recshr_material"]-value["material_of_component"]["enershr_material"])/100
        else:
            return 0

    @classmethod
    def relativeWeight(self, value,valueDict):
        total_weight = 0
        for _,value2 in valueDict.items():
            total_weight+=float(value2["one_component"]["weight_component"])*int(value2["one_compose"]["piecenumber_component"])
        return float(value["one_component"]["weight_component"])/total_weight
        