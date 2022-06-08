from .tabs import MainTab
import activity_browser as ab 

######################
# PLUGIN DESCRIPTION #
######################

infos = {
    'name': 'ReSICLED',
    'version': '0.0.2',
    'author': 'Rémy Le Calloch',
    'author_email': 'remy@lecalloch.net',
    'url': 'https://gricad-gitlab.univ-grenoble-alpes.fr/green-scop-demo/ab-plugins/resicled',
    'description': 'Evaluate the recyclability of product Electr(on)ic for improving product design'
}

#######################

class Plugin(ab.Plugin):

    def __init__(self):
        ab.Plugin.__init__(self, infos)
        self.mainTab = MainTab(self)
        self.tabs = [self.mainTab]
    