from PySide2 import QtCore
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel
)
from PySide2.QtCore import Qt


class PresentationTab(QTabWidget):
    def __init__(self, parent=None):
        super(PresentationTab, self).__init__(parent)
        # --- title ---
        title = QLabel(self)
        #title.setMargin(0)
        title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        title.setText('<h1 style=""> RESICLED </h1>')
        title.setTextFormat(Qt.RichText)
        title.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        #moving position
        title.move(10, 50)

        #--- label ---
        label = QLabel(self)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setText('<h3 style=""> Symplified - Recoverry System modelling and Calculation Leading To End-of-life conscious Design </h3>')
        label.setTextFormat(Qt.RichText)
        label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        # moving position
        label.move(10, 100)

        #--- button start ---
        # creating a push button
        self.button = QPushButton("START", self)
        # setting geometry of button
        self.button.setGeometry(200, 150, 100, 40)
        # changing color of button
        self.button.setStyleSheet("background-color : yellow")
        # adding action to a button
        self.button.clicked.connect(self.open_tab(parent))
    
    def open_tab(self, parent):
        """
        #parent.tabs.setTabVisible(2,0)
        label = QLabel(self)
        for tab_name, tab_obj in parent.tabs.items():
            parent.addTab(QPushButton("button "+tab_name), tab_name)
            label.setText('<h3 style="">'+tab_name+'</h3>')
            label.setTextFormat(Qt.RichText)
            label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        """
        parent.tabwidget.setCurrentIndex(4)
        