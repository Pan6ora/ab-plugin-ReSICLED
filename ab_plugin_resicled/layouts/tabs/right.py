from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QComboBox
)
from activity_browser.layouts.tabs import PluginTab
from activity_browser.ui.style import horizontal_line, header

from ...signals import signals
from ...views.PresentationTab import PresentationTab
from ...views.inputTab import InputTab
from ...views.dismantlingTab import DismantlingTab
from ...views.shreddingTab import ShreddingTab
from ...views.mixedTab import MixedTab
from ...views.hotspotsTab import HotspotsTab
from ...views.guidelinesTab import GuidelinesTab

class RightTab(PluginTab):
    def __init__(self, plugin, parent=None):
        super(RightTab, self).__init__(plugin=plugin, panel="right", parent=parent)
        self.tabs = dict([('index1',1),('index2',2)])
        self.tabwidget = QTabWidget()
        self.tabs = {
            "Presentation": PresentationTab(self),
            "Input": InputTab(self),
            "Dismantling": DismantlingTab(self),
            "Shredding": ShreddingTab(self),
            "Mixed": MixedTab(self),
            "HotSpots": HotspotsTab(self),
            "Guidelines": GuidelinesTab(self),
		}
        for tab_name, tab_obj in self.tabs.items():
            self.tabwidget.addTab(tab_obj, tab_name)
            if(tab_name=="Dismantling" or tab_name=="Shredding" or tab_name=="Mixed" or tab_name=="HotSpots"):
                signals.update_combobox.connect(tab_obj.update_menu_combobox)
                signals.update_combobox.emit(QComboBox())
            
        #display tab in layout   
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addWidget(self.tabwidget)
        self.setLayout(self.layout)

