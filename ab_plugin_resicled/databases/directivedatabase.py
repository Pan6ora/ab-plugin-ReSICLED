import os
import json
import sys
import brightway2 as bw
from brightway2 import *
from bw2data import *
from bw2io.package import BW2Package

from datetime import datetime
from ..tools.tool import Tool



class Directivedatabase():
    def __init__(self, parent=None):
        #--init
        self.tool = Tool()
        
        #database name
        self.name_database = self.tool.prefix_name_database + "directives"
        self.db = bw.Database(self.name_database)
        
    def get_all_directive(self):
        return self.db.load()
    
    def get_one_directive(self, key):
        dico = self.db.load()
        key = (self.name_database, str(key))
        if(dico != None and dico.__contains__(key)):
            return dico.__getitem__(key)
    
    def get_directive_by_attrib(self, name_attrib_param, value_attrib_param):
        result_dict = dict()
        str_name_attrib_param = str(name_attrib_param)
        str_value_attrib_param = str(value_attrib_param)
        dico = self.db.load()
        for key, value in dico.items():
            str_value_attrib = str(value[str_name_attrib_param])
            if str_value_attrib.lower() == str_value_attrib_param.lower():
                result_dict[key] = value
        return result_dict
    
    def insert_one_directive(self, dict_directive: dict):
        self.dt = datetime.now()
        self.id_directive = dict_directive["id_directive"]
        self.name = dict_directive["name"]
        self.comment = dict_directive["comment"]
        self.dismantling_recycling_rate = dict_directive["dismantling_recycling_rate"]
        self.dismantling_recovery_rate = dict_directive["dismantling_recovery_rate"]
        self.dismantling_residual_waste_rate = dict_directive["dismantling_residual_waste_rate"]
        self.shredding_recycling_rate = dict_directive["shredding_recycling_rate"]
        self.shredding_recovery_rate= dict_directive["shredding_recovery_rate"]
        self.shredding_residual_waste_rate = dict_directive["shredding_residual_waste_rate"]
        self.mixed_recycling_rate = dict_directive["mixed_recycling_rate"]
        self.mixed_recovery_rate = dict_directive["mixed_recovery_rate"]
        self.mixed_residual_waste_rate = dict_directive["mixed_residual_waste_rate"]
        # new directive
        self.new_directive = {
            "directive_number": self.id_directive,
            "name": self.name,
            "comment": self.comment,
            "dismantling_recycling_rate": self.dismantling_recycling_rate,
            "dismantling_recovery_rate": self.dismantling_recovery_rate,
            "dismantling_residual_waste_rate": self.dismantling_residual_waste_rate,
            "shredding_recycling_rate": self.shredding_recycling_rate,
            "shredding_recovery_rate": self.shredding_recovery_rate,
            "shredding_residual_waste_rate": self.shredding_residual_waste_rate,
            "mixed_recycling_rate": self.mixed_recycling_rate,
            "mixed_recovery_rate": self.mixed_recovery_rate,
            "mixed_residual_waste_rate": self.mixed_residual_waste_rate,
        }
        # save data
        dico = self.db.load()
        dico.__setitem__((self.name_database, str(self.id_directive)), self.new_directive)
        self.db.write(dico)
        
    def delete_one_directive(self, id_directive_param):
        dico = self.db.load()
        key = (self.name_database, str(id_directive_param))
        if(dico != None and dico.__contains__(key)):
            dico.__delitem__(key)
            self.db.write(dico)
            
        
        
        