from PySide2 import QtCore, QtWidgets
from activity_browser.ui.style import horizontal_line, header

class MainTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainTab, self).__init__(parent)        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addWidget(header("ReSICLED"))
        self.layout.addWidget(horizontal_line())
        self.setLayout(self.layout)