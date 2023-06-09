import os
import json
import sys
import brightway2 as bw
from brightway2 import *
from bw2data import *
from bw2io.package import BW2Package 

from datetime import datetime
from ..tools.tool import Tool

class Materialdatabase():
    def __init__(self, parent=None):
        #--init
        self.tool = Tool()
        
        #database name
        self.name_database = self.tool.prefix_name_database + "materials"
        self.db = bw.Database(self.name_database)
        
    def get_all_material(self):
        return self.db.load()
    
    def get_one_material(self, key):
        dico = self.db.load()
        key = (self.name_database, str(key))
        if(dico != None and dico.__contains__(key)):
            return dico.__getitem__(key)
    
    def get_material_by_attrib(self, name_attrib_param, value_attrib_param):
        result_dict = dict()
        str_name_attrib_param = str(name_attrib_param)
        str_value_attrib_param = str(value_attrib_param)
        dico = self.db.load()
        for key, value in dico.items():
            str_value_attrib = str(value[str_name_attrib_param])
            if str_value_attrib.lower() == str_value_attrib_param.lower():
                result_dict[key] = value
        return result_dict
    
    def insert_one_material(self, dict_material: dict):
        self.dt = datetime.now()
        self.id_material = dict_material["id_material"]
        self.type_material = dict_material["type_material"]
        self.name_material = dict_material["name"]
        self.recdis_material = dict_material["recdis_material"]
        self.enerdis_material = dict_material["enerdis_material"]
        self.wastedis_material = dict_material["wastedis_material"]
        self.recshr_material = dict_material["recshr_material"]
        self.enershr_material = dict_material["enershr_material"]
        self.wasteshr_material = dict_material["wasteshr_material"]
        self.price_material = dict_material["price_material"]
        self.pollutant_material = dict_material["pollutant_material"]
        # new material
        self.new_material = {
            "id_material": self.id_material,
            "type_material": self.type_material,
            "name": self.name_material,
            "recdis_material": self.recdis_material,
            "enerdis_material": self.enerdis_material,
            "wastedis_material": self.wastedis_material,
            "recshr_material": self.recshr_material,
            "enershr_material": self.enershr_material,
            "wasteshr_material": self.wasteshr_material,
            "price_material": self.price_material,
            "pollutant_material": self.pollutant_material,
        }
        # save data
        dico = self.db.load()
        dico.__setitem__((self.name_database, str(self.id_material)), self.new_material)
        self.db.write(dico)
        
    def delete_one_material(self, id_material_param):
        dico = self.db.load()
        key = (self.name_database, str(id_material_param))
        if(dico != None and dico.__contains__(key)):
            dico.__delitem__(key)
            self.db.write(dico)
            
        
        
        