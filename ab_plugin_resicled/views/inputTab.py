from PySide2 import QtCore
from PySide2.QtCore import Slot
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
from ..signals import signals
from ..models.tablemodel import TableModel
from ..models.datamodel import Datamodel
from ..databases.database import databasemanager



class InputTab(QTabWidget):
    def __init__(self, parent=None):
        super(InputTab, self).__init__(parent)
        
        self.icon = Icon()
        self.form = Form()
        style = Style()
        self.databasemanager = databasemanager
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
            self.call_show_dialog_insert_product
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
        self.all_product = self.databasemanager.productdatabase.get_all_product()
        self.edit_component_product = QComboBox(self)
        self.edit_component_product.addItem("Select a product to view its components", userData=None)
        for key_product, value_product in self.all_product.items():
            self.edit_component_product.addItem(str(value_product['name_product']), userData=value_product)
        self.edit_component_product.move(250, 100)
        self.edit_component_product.setFrame(False)
        #add signal
        self.edit_component_product.currentIndexChanged.connect(
            self.call_show_table_component_product
        )
        
        #---line
        self.ligne_local = style.horizontal_line(self)
        self.ligne_local.setGeometry(10, 130, 400, 1)
        
        #--- table
        self.datamodel = Datamodel();
        self.data_list = self.datamodel.getdata_product()
        self.header = self.datamodel.header_database_product
        self.table_model = TableModel(self, self.data_list, self.header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        # set font
        self.font = QFont("Courier New", 10)
        self.table_view.setFont(self.font)
        # set column width to fit contents (set font first!)
        self.table_view.resizeColumnsToContents()
        #display
        self.widget_table_view = QWidget(self)
        self.layout_table_view = QVBoxLayout(self)
        self.layout_table_view.addWidget(self.table_view)
        self.widget_table_view.setLayout(self.layout_table_view)
        self.widget_table_view.setGeometry(10, 170, 1200, 500)
        self.widget_table_view.show()
        
        # --- title ---
        self.title_component_product = QLabel(self)
        self.title_component_product.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title_component_product.setText('')
        self.title_component_product.setGeometry(10, 140, 1200, 30)
        
        #signal update_combobox
        signals.update_combobox.connect(self.update_menu_combobox)
    
    def open_tab(self, parent):
        parent.tabwidget.setCurrentIndex(4)
        
    def call_show_dialog_insert_product(self):
        self.form.show_dialog_insert_product(self.edit_component_product)
        
    def call_show_table_component_product(self,index):
        product_selected = self.edit_component_product.currentData()
        if(product_selected==None):
            return None
        
        self.title_component_product.setText('<h1 style=""> '+product_selected.__getitem__('name_product')+' (components list)  </h1>' )
        self.datamodel = Datamodel();
        self.data_list = self.datamodel.getdata_component(product_selected.__getitem__('id_product'))
        self.header = self.datamodel.header_database_component
        self.table_model = TableModel(self, self.data_list, self.header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        # set font
        self.font = QFont("Courier New", 10)
        self.table_view.setFont(self.font)
        # set column width to fit contents (set font first!)
        self.table_view.resizeColumnsToContents()
        #display
        self.widget_table_view = QWidget(self)
        self.layout_table_view = QVBoxLayout(self)
        self.layout_table_view.addWidget(self.table_view)
        self.widget_table_view.setLayout(self.layout_table_view)
        self.widget_table_view.setGeometry(10, 170, 1200, 500)
        self.widget_table_view.show()
        
    @Slot(object, object)
    def update_table_component_product(self, header_param, data_list_param):
        #---product to select
        self.header = header_param
        self.data_list = data_list_param
        
    @Slot(object)
    def update_menu_combobox(self):
        box = self.edit_component_product
        #---product to select
        self.all_product_form = self.databasemanager.productdatabase.get_all_product()
        try:
            box.clear()
            box.addItem("Select a product to view its components")
            for key, value in self.all_product_form.items():
                box.addItem(str(value['name_product']), userData=value)
        except: 
            pass
            
            
