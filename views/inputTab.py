from PySide2 import QtCore
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QGridLayout, QComboBox,
    QWidget, QTableView, QWidget
)
from PySide2.QtGui import QFont 
from PySide2.QtCore import Qt
from .icon import Icon
from .form import Form
from .style import Style
from ..controllers.signals import signals
from ..models.tablemodel import TableModel
from ..models.datamodel import Datamodel


class InputTab(QTabWidget):
    def __init__(self, parent=None):
        super(InputTab, self).__init__(parent)
        
        self.icon = Icon()
        self.form = Form()
        style = Style()
        

        # --- title ---
        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> INPUT </h1>')
        self.title.move(10, 50)
        
        
        #--- button add product
        self.button_add_product = QPushButton(self.icon.add, "Add Product", self)
        # moving position
        self.button_add_product.move(10, 100)
        #add signal
        self.button_add_product.clicked.connect(
            #signals.add_product.emit(None)
            self.form.show_dialog_insert_product
        )
        
        #--- button add component
        self.button_add_component = QPushButton(self.icon.add, "Add component", self)
        # moving positions
        self.button_add_component.move(120, 100)
        #add signal
        self.button_add_component.clicked.connect(
            self.form.show_dialog_insert_component
        )
        
        #---product to select
        self.edit_component_product = QComboBox(self)
        self.edit_component_product.addItem("Select a product")
        self.edit_component_product.addItem("eg. product")
        #self.edit_component_product.setGeometry(260, 100, 120, 30)
        self.edit_component_product.move(250, 100)
        self.edit_component_product.setFrame(False)
        
        #---line
        self.ligne_local = style.horizontal_line(self)
        self.ligne_local.setGeometry(10, 130, 400, 1)
        #self.ligne_local.move(10, 110)
        
        #--- table
        self.datamodel = Datamodel();
        self.data_list = self.datamodel.getdata_component()
        self.header = self.datamodel.header_component
        self.table_model = TableModel(self, self.data_list, self.header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        # set font
        self.font = QFont("Courier New", 14)
        self.table_view.setFont(self.font)
        # set column width to fit contents (set font first!)
        self.table_view.resizeColumnsToContents()
        # enable sorting
        self.table_view.setSortingEnabled(True)
        #display
        self.widget_table_view = QWidget(self)
        self.layout_table_view = QVBoxLayout(self)
        self.layout_table_view.addWidget(self.table_view)
        self.widget_table_view.setLayout(self.layout_table_view)
        self.widget_table_view.setGeometry(10, 150, 800, 800)
        self.widget_table_view.show()
             
        
        """#--- QGridLayout grid placement ---
        self.layout = QGridLayout()
        self.layout.addWidget(self.button_add_product, 0 ,0)
        self.layout.addWidget(self.button_add_component, 0 ,1)
        self.setLayout(self.layout)"""
        
        
        """#--- Final layout ---
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(style.horizontal_line())
        self.layout_main.addWidget(self.edit_component_product)
        #self.layout_main.addWidget(self.widget_button)
        self.setLayout(self.layout_main)"""
        

        
    
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
        
    
