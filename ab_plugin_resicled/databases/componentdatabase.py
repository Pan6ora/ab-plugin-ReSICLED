import os
import json
import sys
import brightway2 as bw
from brightway2 import *
from bw2data import *
from datetime import datetime
from ..tools.tool import Tool
from .materialdatabase import Materialdatabase

class Componentdatabase:
    def __init__(self, parent=None):
        # --init
        self.tool = Tool()
        self.materialdatabase = Materialdatabase()
        # database name
        self.name_database = self.tool.prefix_name_database + "component"
        # instance of database
        self.db = bw.Database(self.name_database)

    def get_all_component(self):
        return self.db.load()

    def get_one_component(self, key):
        dico = self.db.load()
        key = (self.name_database, str(key))
        if(dico != None and dico.__contains__(key)):
            return dico.__getitem__(key)

    def get_all_material_of_component(self, id_component_param):
        dict_component = self.get_one_component(id_component_param)
        if(dict_component != None and dict_component.__contains__("id_material")):
            return self.materialdatabase.get_one_material(dict_component.__getitem__("id_material"))
    
    def get_all_component_of_material(self, id_material_param):
        result_dict = dict()
        dico = self.db.load()
        for key, value in dico.items():
            str_id_component = str(value["id_component"])
            str_id_material = str(value["id_material"])
            if str_id_material == str(id_material_param):
                result_dict[key] = value
        return result_dict

    def insert_one_component(self, dict_component: dict):
        self.dt = datetime.now()
        self.id_component = dict_component["id_component"]
        self.id_material = dict_component["id_material"]
        self.name_component = dict_component["name_component"]
        self.weight_component = dict_component["weight_component"]
        self.comment_component = dict_component["comment_component"]
        # new component
        self.new_component = {
            "id_component": self.id_component,
            "id_material": self.id_material,
            "name_component": self.name_component,
            "weight_component": self.weight_component,
            "comment_component": self.comment_component,
        }
        # save data
        dico = self.db.load()
        dico.__setitem__(
            (self.name_database, str(self.id_component)), self.new_component
        )
        self.db.write(dico)
        
    def insert_one_material(self, dict_material: dict):
        self.dt = datetime.now()
        dict_material["id_material"] = datetime.timestamp(self.dt)
        self.materialdatabase.insert_one_material(dict_material)

    def delete_one_component(self, id_component_param):
        # delete component
        dico = self.db.load()
        key = (self.name_database, str(id_component_param))
        if(dico != None and dico.__contains__(key)):
            dico.__delitem__(key)
            self.db.write(dico)
        
    def delete_one_material(self, id_material_param):
        self.materialdatabase.delete_one_material(id_material_param)
        
        
        
        