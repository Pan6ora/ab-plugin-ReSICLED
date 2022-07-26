import os
import json
import sys
import brightway2 as bw
from brightway2 import *
from bw2data import *
from bw2io.package import BW2Package

from ...metadata import infos
from datetime import datetime
from ..tools.tool import Tool



class Directivedatabase():
    def __init__(self, parent=None):
        ##print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        #--init
        self.tool = Tool()
        
        #database name
        self.name_database = self.tool.prefix_name_database + "directive"
        
        #-- check if database exist, create if not exist
        if self.name_database not in bw.databases:
            """
            #get table in json file
            self.path_database = self.tool.get_path_database_tables_file('Database_resicled_directive.json')
            self.f = open(self.path_database, "r")
            database_string = self.f.read()
            """
            #Creating/accessing the project
            bw.projects.set_current(self.tool.projects_name_database)
            #Manually creating a database is to have the data in a separate dictionary
            path = bw.projects.request_directory("plugins")
            BW2Package().import_file(path+"/{}/plugin/includes/bw2package/directives.bw2package".format(infos["name"]))
        self.db = bw.Database(self.name_database)
        
    def get_all_directive(self):
        ##print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        return self.db.load()
    
    def get_one_directive(self, key):
        ##print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        dico = self.db.load()
        key = (self.name_database, str(key))
        if(dico != None and dico.__contains__(key)):
            return dico.__getitem__(key)
    
    def get_directive_by_attrib(self, name_attrib_param, value_attrib_param):
        ##print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
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
        ##print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        self.dt = datetime.now()
        self.id_directive = dict_directive["id_directive"] #datetime.timestamp(self.dt)
        self.directive_title = dict_directive["directive_title"]
        self.directive_comment = dict_directive["directive_comment"]
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
            "directive_title": self.directive_title,
            "directive_comment": self.directive_comment,
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
        ##print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        dico = self.db.load()
        key = (self.name_database, str(id_directive_param))
        if(dico != None and dico.__contains__(key)):
            dico.__delitem__(key)
            self.db.write(dico)
            
        
        
        