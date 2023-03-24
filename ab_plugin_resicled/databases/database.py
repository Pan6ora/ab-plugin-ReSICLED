import brightway2 as bw
from bw2io.package import BW2Package
import pkg_resources

import time

from activity_browser.settings import project_settings

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

        path = pkg_resources.resource_filename(__name__, '../includes/bw2package')
        for db_name in self.included_databases:
            if db_name not in bw.databases:
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


