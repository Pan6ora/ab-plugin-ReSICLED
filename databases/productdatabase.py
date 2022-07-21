import os
import json
import sys
import brightway2 as bw
from brightway2 import *
from bw2data import *
from datetime import datetime
from ..tools.tool import Tool
from .fixtures import Fixture

class Productdatabase():
    def __init__(self, parent=None):
        #print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        #--init
        self.tool = Tool()
        self.fixture = Fixture()
        #database name
        self.name_database = self.tool.prefix_name_database + "product"
       # instance of database
        self.db = bw.Database(self.name_database)
            
    def get_all_product(self):
        #print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        return self.db.load()
        
    def get_one_product(self, key):
        #print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        dico = self.db.load()
        key = (self.name_database, str(key))
        if(dico != None and dico.__contains__(key)):
            return dico.__getitem__(key)
        
    def insert_one_product(self, dict_product: dict):
        #print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        self.dt = datetime.now()
        self.id_product = datetime.timestamp(self.dt)
        self.name_product = dict_product['name_product']
        self.nameauthor_product = dict_product['nameauthor_product']
        self.firstname_product = dict_product['firstname_product']
        #new product
        self.new_product = {
            "id_product": self.id_product,
            "name_product": self.name_product,
            "nameauthor_product": self.nameauthor_product,
            "firstname_product": self.firstname_product
        }
        #save data
        dico = self.db.load()
        dico.__setitem__((self.name_database, str(self.id_product)), self.new_product)
        self.db.write(dico)
        
    def delete_one_product(self, id_product_param):
        # delete all referenced component
        #self.composedatabase.delete_all_component_of_product(id_product_param)
        # delete product
        dico = self.db.load()
        key = (self.name_database, str(id_product_param))
        if(dico != None and dico.__contains__(key)):
            dico.__delitem__(key)
            self.db.write(dico)
        
        
        