import brightway2 as bw
from bw2io.package import BW2Package
from ..tools.tool import Tool
from ...metadata import infos

class GuidelinesDatabase:
    def __init__(self,parent = None):
        self.tool = Tool()

        self.name_database = self.tool.prefix_name_database+"guidelines"
        if self.name_database not in bw.databases:
            #Manually creating a database is to have the data in a separate dictionary
            path = bw.projects.request_directory("plugins")
            BW2Package().import_file(path+"/{}/plugin/includes/bw2package/guidelines.bw2package".format(infos["name"]))          
        self.db = bw.Database(self.name_database)

    def get_all_guidelines(self):
        return self.db.load()

    def get_one_guideline(self,key):
        return self.get_all_guidelines()[(self.name_database,str(key))]

    # No insertion nor deletion added so far as it's useless (but would be possible adding it to the list of all directives)
