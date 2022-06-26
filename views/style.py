from PySide2 import QtCore
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QLineEdit, QDialog, QApplication, QDoubleSpinBox, QFrame
)

class Style(QDialog):
    def __init__(self, parent=None):
        super(Style, self).__init__(parent)
        
    def horizontal_line(self,parent=None):
        line = QFrame(parent)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        return line
        