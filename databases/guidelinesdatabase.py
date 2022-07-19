import brightway2 as bw
from ..tools.tool import Tool
from .fixtures import Fixture

class GuidelinesDatabase:
    def __init__(self,parent = None):
        self.tool = Tool()
        self.fixture = Fixture()

        self.name_database = self.tool.prefix_name_database+"guidelines"
        if self.name_database not in bw.databases:
            bw.projects.set_current(self.tool.projects_name_database)
            self.db = bw.Database(self.name_database)
            self.db.write(self.fixture.db_guidelines)
        else:
            self.db = bw.Database(self.name_database)

    def get_all_guidelines(self):
        return self.db.load()

    def get_one_guideline(self,key):
        return self.get_all_guidelines()[(self.name_database,str(key))]

    # No insertion nor deletion added so far as it's useless (but would be possible adding it to the list of all directives)
