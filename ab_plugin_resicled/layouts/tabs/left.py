from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QComboBox
)
from activity_browser.layouts.tabs import PluginTab
from activity_browser.ui.style import horizontal_line, header

from ...signals import signals
from ...views.databaseTab import DatabaseTab

class LeftTab(PluginTab):
    def __init__(self,plugin,parent=None):
        super(LeftTab, self).__init__(plugin=plugin,panel="left", parent=parent)
        self.tabs = dict([('index1',1),('index2',2)])
        self.tabwidget = QTabWidget()
        self.tabs = {
            "Database": DatabaseTab(self),
		}
        for tab_name, tab_obj in self.tabs.items():
            self.tabwidget.addTab(tab_obj, tab_name)
            
        #display tab in layout   
        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addWidget(self.tabwidget)
        self.setLayout(self.layout)