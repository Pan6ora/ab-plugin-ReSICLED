from PySide2 import QtCore
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel
)
from PySide2.QtCore import Qt, QRect
from .icon import Icon


class PresentationTab(QTabWidget):
    def __init__(self, parent=None):
        super(PresentationTab, self).__init__(parent)
        
        #--- logo ---
        icon = Icon()
        pixmap = icon.logo
        label_logo = QLabel(self)
        label_logo.setPixmap(pixmap)
        label_logo.setGeometry(QRect(10, 10, pixmap.width(), pixmap.height()))
        
        #--- init --
        base_height = pixmap.height()
        self.parent_tabwidget = parent.tabwidget

        #--- label ---
        label = QLabel(self)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setText('<h3 style=""> Symplified - Recovery System modelling and Indicator Calculation Leading To End-of-life conscious Design </h3>')
        label.setTextFormat(Qt.RichText)
        label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        # moving position
        label.move(10, 50+int(base_height))

        #--- button start ---
        # creating a push button
        self.button = QPushButton("START", self)
        # setting geometry of button
        self.button.setGeometry(200, 100+int(base_height), 100, 40)
        # changing color of button
        self.button.setStyleSheet("background-color : #9bbb59;")
        # adding action to a button
        self.button.clicked.connect(self.open_tab)
    
    def open_tab(self):
        self.parent_tabwidget.setCurrentIndex(1)
        