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
from ..databases.database import DatabaseManager

databasemanager = DatabaseManager()

class HotspotsTab(QTabWidget):
    def __init__(self, parent=None):
        super(HotspotsTab, self).__init__(parent)
        
        self.icon = Icon()
        self.form = Form()
        self.style = Style()
        self.combo_scenario = dict()
        
        # --- title ---
        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> HOTSPOTS </h1>')
        self.title.move(10, 50)
        
        
        # --- title select product---
        self.title = QLabel(self)
        self.title.setText('Select a product to view its hotspots : ')
        #---product to select
        self.all_product = databasemanager.productdatabase.get_all_product()
        self.edit_component_product = QComboBox(self)
        self.edit_component_product.addItem("Select a product", userData=None)
        for key_product, value_product in self.all_product.items():
            self.edit_component_product.addItem(str(value_product['name_product']), userData=value_product)
        #self.edit_component_product.setGeometry(10, 120, 120, 30)
        self.edit_component_product.setFrame(False)
        self.product_selection_widget = QWidget(self)
        self.product_selection_layout = QHBoxLayout(self)
        self.product_selection_layout.addWidget(self.title)
        self.product_selection_layout.addWidget(self.edit_component_product)
        self.product_selection_widget.setLayout(self.product_selection_layout)
        self.product_selection_widget.move(10,100)
        

        
        
        # --- title product selected ---
        self.title_component_product = QLabel(self)
        self.title_component_product.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title_component_product.setText('')
        self.title_component_product.setGeometry(10, 140, 1200, 30)
        
        #add signal
        self.edit_component_product.currentIndexChanged.connect(
            self.call_show_table_component_product
        )
        
        #signal update_combobox
        signals.update_combobox.connect(self.update_menu_combobox)
        signals.update_combobox.emit(self.edit_component_product)
        signals.update_component_scenario.connect(self.call_show_table_component_product)
        
    @Slot(object)
    def update_menu_combobox(self, box: QComboBox):
        box = self.edit_component_product
        #---product to select
        self.all_product_form = databasemanager.productdatabase.get_all_product()
        box.clear()
        box.addItem("Select a product")
        for key, value in self.all_product_form.items():
            box.addItem(str(value['name_product']), userData=value)
        
    def call_show_dialog_insert_directive(self):
        self.form.show_dialog_insert_directive(self, "shredding")
        
    @Slot(object)  
    def call_show_table_component_product(self,index):
        # --- title Parts presenting the most interesting potential for dismantling ---
        self.title_table = QLabel(self)
        self.title_table.setText('Parts presenting the most interesting potential for dismantling')
        self.title_table.move(10, 190)
        
        # --- title Parts generating the most residual waste ---
        self.title_table = QLabel(self)
        self.title_table.setText('Parts generating the most residual waste')
        self.title_table.move(10, 530)
        
        product_selected = self.edit_component_product.currentData()
        if (product_selected == None):
            return None
        
        #print("call_show_table_component_product",product_selected.__getitem__('name_product')," id_product==", product_selected.__getitem__('id_product'))
        self.title_component_product.setText('<h1 style=""> '+product_selected.__getitem__('name_product')+' (components list)  </h1>' )
        
        #for hotspots_1
        """#get new values"""
        self.datamodel = Datamodel(self);
        self.data_list = self.datamodel.getdata_hotspots(product_selected.__getitem__('id_product'),"hotspots_1") #self.datamodel.getdata_component()
        self.header = self.datamodel.header_hotspots_1 #self.datamodel.header_component      
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
        self.widget_table_view.setGeometry(10, 210, 1200, 300)
        self.widget_table_view.show()
        
        
        #for hotspots_2
        """#get new values"""
        self.datamodel_2 = Datamodel(self)
        self.data_list_2 = self.datamodel_2.getdata_hotspots(product_selected.__getitem__('id_product'),"hotspots_2") #self.datamodel_2.getdata_component()
        self.header_2 = self.datamodel_2.header_hotspots_2 #self.datamodel_2.header_2_component      
        self.table_model_2 = TableModel(self, self.data_list_2, self.header_2)
        self.table_view_2 = QTableView()
        self.table_view_2.setModel(self.table_model_2)
        self.table_view_2.hideColumn(4)
        self.table_view_2.hideColumn(5)
        # set font
        self.font = QFont("Courier New", 10)
        self.table_view_2.setFont(self.font)
        # set column width to fit contents (set font first!)
        self.table_view_2.resizeColumnsToContents()        
        #display
        self.widget_table_view_2 = QWidget(self)
        self.layout_table_view_2 = QVBoxLayout(self)
        self.layout_table_view_2.addWidget(self.table_view_2)
        self.widget_table_view_2.setLayout(self.layout_table_view_2)
        self.widget_table_view_2.setGeometry(10, 550, 1200, 300)
        self.widget_table_view_2.show()
        
                
        
        
        
        
        