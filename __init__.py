import activity_browser as ab
from activity_browser.signals import signals

from .plugin.layouts.tabs import LeftTab, RightTab
from .plugin.databases.database import databasemanager
from .metadata import infos

class Plugin(ab.Plugin):

    def __init__(self):
        ab.Plugin.__init__(self, infos)
        self.mainTab = RightTab(self)
        self.leftTab = LeftTab(self)
        self.tabs = [self.mainTab, self.leftTab]
        self.databasemanager = databasemanager

    def initialize(self):
        self.databasemanager.import_databases()
        signals.databases_changed.emit()

    def remove(self):
        self.databasemanager.delete_databases()
        signals.databases_changed.emit()