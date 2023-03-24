import brightway2 as bw
from bw2io.package import BW2Package

import time

from activity_browser.settings import project_settings

from ...metadata import infos
from .materialdatabase import Materialdatabase
from .productdatabase import Productdatabase
from .composedatabase import Composedatabase
from .componentdatabase import Componentdatabase
from .directivedatabase import Directivedatabase
from .guidelinesdatabase import GuidelinesDatabase

class DatabaseManager():
    def __init__(self, parent=None):
        self.directivedatabase = Directivedatabase()
        self.productdatabase = Productdatabase()
        self.composedatabase = Composedatabase()
        self.componentdatabase = Componentdatabase()
        
        self.guidelinesdatabase = GuidelinesDatabase()
        self.materialdatabase = Materialdatabase()

        self.included_databases = ["resicled_directives","resicled_guidelines","resicled_materials",]

    def import_databases(self):

        path = bw.projects.request_directory("plugins")
        path = "{}/{}/plugin/includes/bw2package".format(path,infos["name"])
        for db_name in self.included_databases:
            """
            if db_name in bw.databases:
                self.delete_database(db_name)
            """
            self.import_database(path, db_name)

    def delete_databases(self):
       for db_name in self.included_databases:
            if db_name in bw.databases:
                 self.delete_database(db_name)               

    def import_database(self,path,db_name):
        print("Importing {} database".format(db_name))
        BW2Package().import_file("{}/{}.bw2package".format(path,db_name))

    def delete_database(self,db_name):
        print("Removing {} database".format(db_name))
        project_settings.remove_db(db_name)
        del bw.databases[db_name]

databasemanager = DatabaseManager()


