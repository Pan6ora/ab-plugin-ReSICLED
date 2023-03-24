import activity_browser as ab
from activity_browser.signals import signals

from .layouts.tabs import LeftTab, RightTab
from .databases.database import databasemanager

class Plugin(ab.Plugin):

    def __init__(self):
        infos = {
            'name': "ReSICLED",
        }
        ab.Plugin.__init__(self, infos)
        self.databasemanager = databasemanager

    def load(self):
        self.mainTab = RightTab(self)
        self.leftTab = LeftTab(self)
        self.tabs = [self.mainTab, self.leftTab]
        self.databasemanager.import_databases()
        signals.databases_changed.emit()

    def close(self):
        pass

    def remove(self):
        try:
            self.databasemanager.delete_databases()
            signals.databases_changed.emit()
        except:
            print("Plugin-ReSICLED: no database to remove")