from PySide2 import QtCore
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QLineEdit, QDialog, QApplication, QDoubleSpinBox, QFrame
)

class Style(QDialog):
    def __init__(self, parent=None):
        super(Style, self).__init__(parent)
        self.style_table_rate = self.get_style_table_rate()
        self.style_good_rate = self.get_style_good_rate()
        self.style_bad_rate = self.get_style_bad_rate()
        self.style_table_rate_border_bottom = self.get_style_table_rate_border_bottom()
        self.style_min_width_100 = self.get_style_min_width_100()
        self.style_min_width_50 = self.get_style_min_width_50()
        
    def horizontal_line(self,parent=None):
        line = QFrame(parent)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        return line
    
    def get_style_table_rate(self):
        return "border-color: black; background-color: #f5f7db;"
    
    def get_style_table_rate_border_bottom(self):
         return "border-bottom-width: 1px; border-right-width: 1px; border-style: solid; border-color: black; background-color: #f5f7db;"
     
    
    def get_style_good_rate(self):
         return "color: green; border-color: green; background-color: #f5f7db;"
    
    def get_style_bad_rate(self):
         return "color: red; border-color: red; background-color: #f5f7db;"
    
    def get_style_min_width_100(self):
        return "min-width: 20em"
    
    def get_style_min_width_50(self):
        return "min-width: 10em"
        
        