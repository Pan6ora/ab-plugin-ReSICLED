from PySide2 import QtCore, QtWidgets
from activity_browser.layouts.tabs import PluginTab
from activity_browser.ui.style import horizontal_line, header

from ..views.panel import ResicledTab

class MainTab(PluginTab):
    def __init__(self, plugin, parent=None):
        super(MainTab, self).__init__(plugin=plugin, panel="right", parent=parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addWidget(header("ReSICLED"))
        self.layout.addWidget(horizontal_line())
        
        # START ADD BY TCHAS
        resicledtab = ResicledTab()
        self.layout.addWidget(resicledtab)
        # END ADD BY TCHAS
	
        self.setLayout(self.layout)
        
        
