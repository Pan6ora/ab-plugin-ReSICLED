from .tabs import LeftTab, RightTab
import activity_browser as ab 
from .databases.database import DatabaseManager
from activity_browser.signals import signals

######################
# PLUGIN DESCRIPTION #
######################

infos = {
    'id': 'ReSICLED',
    'name': 'ReSICLED',
    'version': '1.0.0',
    'author': 'Rémy Le Calloch, Brice Notario Bourgade, Elysée Tchassem Noukimi',
    'author_email': '',
    'url': 'https://gricad-gitlab.univ-grenoble-alpes.fr/green-scop/ab-plugins/resicled',
    'description': 'Evaluate the recyclability of product Electr(on)ic for improving product design'
}

#######################

class Plugin(ab.Plugin):

    def __init__(self):
        ab.Plugin.__init__(self, infos)
        self.mainTab = RightTab(self)
        self.leftTab = LeftTab(self)
        self.tabs = [self.mainTab, self.leftTab]
        databasemanager = DatabaseManager()
        signals.databases_changed.emit()

    