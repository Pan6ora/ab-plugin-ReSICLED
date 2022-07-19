import os
import json
import sys
import brightway2 as bw
from brightway2 import *
from bw2data import *
from datetime import datetime
from ..tools.tool import Tool
from .fixtures import Fixture
from .productdatabase import Productdatabase
from .componentdatabase import Componentdatabase

class Composedatabase:
    def __init__(self, parent=None):
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        # --init
        self.tool = Tool()
        self.fixture = Fixture()
        self.componentdatabase = Componentdatabase()
        self.productdatabase = Productdatabase()
        # database name
        self.name_database = self.tool.prefix_name_database + "compose"
        # instance of database
        self.db = bw.Database(self.name_database)

    def get_all_compose(self):
        return self.db.load()

    def get_one_compose(self, key):
        dico = self.db.load()
        key = (self.name_database, str(key))
        if(dico != None and dico.__contains__(key)):
            return dico.__getitem__(key)

    def get_compose_by_product(self, id_product_param):
        result_dict = dict()
        dico = self.db.load()
        for key, value in dico.items():
            str_id_product = str(value["id_product"])
            if str_id_product == str(id_product_param):
                result_dict[key] = value
        return result_dict

    def get_compose_by_component(self, id_component_param):
        result_dict = dict()
        dico = self.db.load()
        for key, value in dico.items():
            str_id_component = str(value["id_component"])
            if str_id_component == str(id_component_param):
                result_dict[key] = value
        return result_dict

    def get_compose_by_product_and_component(self, id_product_param, id_component_param):
        result_dict = dict()
        dico = self.db.load()
        # dict_material = dico.__getitem__((self.name_database, str(id_material_param)))
        for key, value in dico.items():
            str_id_product = str(value["id_product"])
            str_id_component = str(value["id_component"])
            str_combi = str(str_id_product + str_id_component)
            str_combi_param = str(str(id_product_param) + str(id_component_param))
            if str_combi == str_combi_param:
                result_dict[key] = value
        return result_dict
    
    def get_component_by_product(self, id_product_param):
        result_dict = dict()
        dico = self.db.load()
        # dict_material = dico.__getitem__((self.name_database, str(id_material_param)))
        for key, value in dico.items():
            str_id_product = str(value["id_product"])
            str_id_component = str(value["id_component"])
            str_combi = str(str_id_product + str_id_component)
            if str(id_product_param) == str_id_product:
                result_dict[key] = dict([("one_compose",self.get_one_compose(str_combi)),("one_product",self.productdatabase.get_one_product(str_id_product)),("one_component",self.componentdatabase.get_one_component(str_id_component)),("material_of_component",self.componentdatabase.get_all_material_of_component(str_id_component))]) #value
        return result_dict
    
    def get_all_component_and_product(self):
        result_dict = dict()
        dico = self.db.load()
        # dict_material = dico.__getitem__((self.name_database, str(id_material_param)))
        for key, value in dico.items():
            str_id_product = str(value["id_product"])
            str_id_component = str(value["id_component"])
            str_combi = str(str_id_product + str_id_component)
            result_dict[key] = dict([("one_compose",self.get_one_compose(str_combi)),("one_product",self.productdatabase.get_one_product(str_id_product)),("one_component",self.componentdatabase.get_one_component(str_id_component)),("material_of_component",self.componentdatabase.get_all_material_of_component(str_id_component))]) #value
        return result_dict

    def insert_one_compose(self, dict_compose: dict):
        self.dt = datetime.now()
        self.id_compose = str(dict_compose["id_product"]) + str(dict_compose["id_component"])  # datetime.timestamp(self.dt)
        self.id_product = dict_compose["id_product"]
        self.id_component = dict_compose["id_component"]
        self.piecenumber_component = dict_compose["piecenumber_component"]
        # new product
        self.new_compose = {
            "id_product": self.id_product,
            "id_component": self.id_component,
            "piecenumber_component": self.piecenumber_component,
        }
        # save data
        dico = self.db.load()
        dico.__setitem__((self.name_database, str(self.id_compose)), self.new_compose)
        self.db.write(dico)
        
    def insert_one_component(self, dict_component: dict):
        self.dt = datetime.now()
        dict_component["id_component"] = datetime.timestamp(self.dt)
        self.insert_one_compose(dict_component)
        self.componentdatabase.insert_one_component(dict_component)

    def delete_one_compose(self, id_compose_param):
        dico = self.db.load()
        key = (self.name_database, str(id_compose_param))
        if(dico != None and dico.__contains__(key)):
            dico.__delitem__(key)
            self.db.write(dico)

    def delete_all_component_of_product(self, id_product_param):
        # get all referenced component
        dict_compose = self.get_compose_by_product(id_product_param)
        for key, value in dict_compose.items():
            self.id_component = value["id_component"]
            # delete component
            self.componentdatabase.delete_one_component(self.id_component)
            # delete compose
            self.id_compose = str(id_product_param) + str(self.id_component)
            self.delete_one_compose(self.id_compose)

    def delete_all_compose_of_component(self, id_component_param):
        # get all referenced component
        dict_compose = self.get_compose_by_component(id_component_param)
        for key, value in dict_compose.items():
            # delete compose
            self.id_compose = str(value["id_product"]) + str(id_component_param)
            self.delete_one_compose(self.id_compose)
            
    def delete_one_product(self, id_product_param):
        # delete all referenced component
        self.delete_all_component_of_product(id_product_param)
        # delete product
        self.productdatabase.delete_one_product(id_product_param)
        
    def delete_one_component(self, id_component_param):
        # delete all referenced compose
        self.delete_all_compose_of_component(id_component_param)
        # delete component
        self.componentdatabase.delete_one_component(id_component_param)
        
    def delete_one_material(self, id_material_param):
        dict_component = self.componentdatabase.get_all_component_of_material(id_material_param)
        # delete all referenced component
        for key, value in dict_component.items():
            self.id_component = value["id_component"]
            self.delete_one_component(self.id_component)
        # delete material
        self.componentdatabase.delete_one_material(id_material_param)
        