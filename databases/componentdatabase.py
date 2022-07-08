import os
import json
import sys
import brightway2 as bw
from brightway2 import *
from bw2data import *
from datetime import datetime
from ..tools.tool import Tool
from .fixtures import Fixture
from .materialdatabase import Materialdatabase

class Componentdatabase:
    def __init__(self, parent=None):
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        # --init
        self.tool = Tool()
        self.fixture = Fixture()
        self.materialdatabase = Materialdatabase()
        # database name
        self.name_database = self.tool.prefix_name_database + "component"
        # instance of database
        self.db = bw.Database(self.name_database)

    def get_all_component(self):
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        return self.db.load()

    def get_one_component(self, key):
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        dico = self.db.load()
        return dico.__getitem__((self.name_database, str(key)))

    def get_all_material_of_component(self, id_component_param):
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        dict_component = self.get_one_component(id_component_param)
        """
        name_attrib_param = "id_material"
        value_attrib_param = dict_component.__getitem__('id_material')
        return self.materialdatabase.get_material_by_attrib(name_attrib_param, value_attrib_param)
        """
        return self.materialdatabase.get_one_material(dict_component.__getitem__("id_material"))

    def insert_one_component(self, dict_component: dict):
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        self.dt = datetime.now()
        self.id_component = dict_component["id_component"] #datetime.timestamp(self.dt)
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
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        self.dt = datetime.now()
        dict_material["id_material"] = datetime.timestamp(self.dt)
        #self.insert_one_component(dict_material)
        self.materialdatabase.insert_one_material(dict_material)

    def delete_one_component(self, id_component_param):
        print("--debug--", self.__class__.__name__, "::",sys._getframe().f_code.co_name)
        # delete all referenced compose
        #self.composedatabase.delete_all_compose_of_component(id_component_param)
        # delete component
        dico = self.db.load()
        dico.__delitem__((self.name_database, str(id_component_param)))
        self.db.write(dico)