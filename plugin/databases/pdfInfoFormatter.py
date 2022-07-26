from .database import DatabaseManager

databasemanager = DatabaseManager()

class PdfInfoFormatter:
    """
    A class that stores generic infos that need to be printed in the plugin and added to the result pdf
    """
    def __init__(self):
        self.result_infos=[]          #initialized when first generating the table
        self.directive_text = None
        self.directive_values = None
        self.current_productId = None

    def set_directive(self,text):
        pass

    def setup_infos(self, id_product):
        
        if len(self.result_infos)==0 or id_product!=self.current_productId:
            self.current_productId=id_product
            # since the info is not initialized yet, we have to create the info list :
            infos = []
            for _,values in databasemanager.composedatabase.get_component_by_product(id_product).items():
                if values["material_of_component"]["pollutant_material"]:
                    infos.append(("Dismantling",False))
                else:
                    infos.append(("Shredding",True))
            self.result_infos = infos
    
