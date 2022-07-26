import activity_browser as ab 

from .plugin.layouts.tabs import LeftTab, RightTab
from .plugin.databases.database import DatabaseManager
from .plugin.signals import signals
from .setup import infos

class Plugin(ab.Plugin):

    def __init__(self):
        ab.Plugin.__init__(self, infos)
        self.mainTab = RightTab(self)
        self.leftTab = LeftTab(self)
        self.tabs = [self.mainTab, self.leftTab]
        databasemanager = DatabaseManager()
        signals.databases_changed.emit()