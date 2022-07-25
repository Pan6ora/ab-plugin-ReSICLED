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
from ..controllers.signals import signals
from ..models.tablemodel import TableModel
from ..models.datamodel import Datamodel
from ..databases.database import DatabaseManager
from ..controllers.signals import signals

databasemanager = DatabaseManager()

class DatabaseTab(QTabWidget):
    def __init__(self, parent=None):
        super(DatabaseTab, self).__init__(parent)
        
        self.icon = Icon()
        self.form = Form()
        self.style = Style()
        self.dict_ligne_database = dict()
        self.button_edit_ligne = dict()
        self.button_delete_ligne = dict()
        
        # --- title ---
        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> DATABASE </h1>')
        self.title.move(10, 50)
        
        
        # --- title select database---
        self.title = QLabel(self)
        self.title.setText('Select a database to view its data')
        #---database to select
        self.edit_database = QComboBox(self)
        self.edit_database.addItem("Select a database", userData=None)
        self.edit_database.addItem("Product", userData=None)
        self.edit_database.addItem("Component", userData=None)
        self.edit_database.addItem("Material", userData=None)
        self.edit_database.addItem("Directive", userData=None)
        #self.edit_database.setGeometry(10, 120, 120, 30)
        self.add_entry_button = QPushButton(self.icon.add,"Add new Database entry", self)
        self.add_entry_button.clicked.connect(self.call_show_dialog_action_add_database)
        self.edit_database_widget = QWidget(self)
        self.edit_database_layout = QHBoxLayout(self)
        self.edit_database_layout.addWidget(self.title)
        self.edit_database_layout.addWidget(self.edit_database)
        self.edit_database_layout.addWidget(self.add_entry_button)
        self.edit_database_widget.setLayout(self.edit_database_layout)
        self.edit_database_widget.move(10, 100)
        self.edit_database.setFrame(False)
        
        # --- title database selected ---
        self.title_database = QLabel(self)
        self.title_database.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title_database.setText('')
        self.title_database.setGeometry(10, 140, 1200, 30)
        
        #add signal
        self.edit_database.currentIndexChanged.connect(
            self.call_show_table_database
        )
  
    def call_show_table_database(self,index):
        database_selected = self.edit_database.currentText()
        if (index == 0):
            return None
        
        #print("call_show_table_database",database_selected)
        self.title_database.setText('<h1 style=""> '+ database_selected +' data list  </h1>' )
        #get new values
        self.datamodel = Datamodel(self)
        self.data_list = self.datamodel.getdata_database(database_selected)
        if(database_selected.lower()=="product"):
            self.header = self.datamodel.header_database_product_manage
        elif(database_selected.lower()=="component"):
            self.header = self.datamodel.header_database_component_manage
        elif(database_selected.lower()=="material"):
            self.header = self.datamodel.header_database_material_manage
        elif(database_selected.lower()=="directive"):
            self.header = self.datamodel.header_database_directive_manage
                
        self.table_model = TableModel(self, self.data_list, self.header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        # set font
        self.font = QFont("Courier New", 10)
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
        self.widget_table_view.setGeometry(10, 180, 1200, 500)
        self.widget_table_view.show()
        #set Action for each ligne
        self.button_edit_ligne = dict()
        self.button_delete_ligne = dict()
        self.widget_action = dict()
        self.layout_action = dict()
        self.table_model.sort(0, order=Qt.AscendingOrder) #Order column ref
        self.table_view.setSortingEnabled(False) # disable sorting because column Action isn't sortable
        for key_ligne, widget_obj in self.dict_ligne_database.items():
            ligne_table = key_ligne
            column_table = len(self.header)-1
            #--- button
            self.button_edit_ligne[ligne_table] = QPushButton(self.icon.edit, "Edit", self)
            self.button_delete_ligne[ligne_table] = QPushButton(self.icon.delete, "Delete", self)
            self.button_edit_ligne[ligne_table].setCheckable(True)
            self.button_delete_ligne[ligne_table].setCheckable(True)
            self.button_edit_ligne[ligne_table].setEnabled(False) #remove after work for edit
            #add signal
            self.button_edit_ligne[ligne_table].clicked.connect(
                lambda: self.call_show_dialog_action_edit_database(database_selected)
            )
            self.button_delete_ligne[ligne_table].clicked.connect(
                lambda: self.call_show_dialog_action_delete_database(database_selected)
            )
            #--- set QGridLayout in widget ---
            self.widget_action[ligne_table] = QWidget(self)
            self.layout_action[ligne_table] = QGridLayout()
            self.layout_action[ligne_table].addWidget(self.button_edit_ligne[ligne_table], 0, 0)
            self.layout_action[ligne_table].addWidget(self.button_delete_ligne[ligne_table], 0, 1)
            self.widget_action[ligne_table].setLayout(self.layout_action[ligne_table])
            self.table_view.setColumnWidth(column_table, 200)
            self.table_view.setRowHeight(ligne_table, 50)
            self.table_view.setIndexWidget(self.table_model.index(int(ligne_table), column_table), self.widget_action[ligne_table])
            #self.widget_action[ligne_table].show()
            
            
    def call_show_dialog_action_edit_database(self, database_selected):
        print("database_selected==",database_selected)
        
    def call_show_dialog_action_delete_database(self, database_selected):
        widget_obj = None
        for key_ligne, widget_button in self.button_delete_ligne.items():
            ligne_table = key_ligne
            if(widget_button.isChecked()):
                widget_obj = self.dict_ligne_database[ligne_table]
                widget_button.toggle()
                
        if(widget_obj == None):
            return None
            
        if(database_selected.lower()=="product"):
            #widget_obj== {'id_product': 1657567894.387305, 'name_product': 'procuct 1', 'nameauthor_product': '', 'firstname_product': '', 'database': 'resicled_product', 'code': '1657567894.387305', 'exchanges': []}
            #show confirm dialog
            id_element = widget_obj['id_product']
            name_element = widget_obj['name_product']
            text_question = "Do you want to delete the product << "+name_element+" >> ? All its components will also be deleted !"
            result_bool = self.form.show_dialog_question(self, text_question)
            if(result_bool == True):
                self.all_product = databasemanager.composedatabase.delete_one_product(id_element)
        if(database_selected.lower()=="component"):
            #show confirm dialog
            id_element = widget_obj['one_component']['id_component']
            name_element = widget_obj['one_component']['name_component']
            Name_Product = widget_obj['one_product']['name_product']
            text_question = "Do you want to delete the component << "+name_element+" >> of product << "+Name_Product+" >> ? "
            result_bool = self.form.show_dialog_question(self, text_question)
            if(result_bool == True):
                self.all_product = databasemanager.composedatabase.delete_one_component(id_element)
        if(database_selected.lower() == "material"):
            #show confirm dialog
            id_element = widget_obj['id_material']
            name_element = widget_obj['name_material']
            type_material = widget_obj['type_material']
            id_element = widget_obj['id_material']
            text_question = "Do you want to delete the material << "+name_element+" >>  (" + type_material + ") ? All its components linked will also be deleted ! "
            result_bool = self.form.show_dialog_question(self, text_question)
            if(result_bool == True):
                self.all_product = databasemanager.composedatabase.delete_one_material(id_element)
        if(database_selected.lower() == "directive"):
            #show confirm dialog
            id_element = widget_obj['directive_number']
            name_element = widget_obj['directive_title']
            text_question = "Do you want to delete the directive << "+name_element+" >> ? "
            result_bool = self.form.show_dialog_question(self, text_question)
            if(result_bool == True):
                self.all_product = databasemanager.directivedatabase.delete_one_directive(id_element)
            
        #emit signal   
        signals.update_combobox.emit(QComboBox())    
        #update table view
        self.call_show_table_database(None)  
        
    def call_show_dialog_action_add_database(self):
        if self.edit_database.currentText().lower()=="product":
            self.form.show_dialog_insert_product(QComboBox())
        elif self.edit_database.currentText().lower()=="component":
            self.form.show_dialog_insert_component()
        elif self.edit_database.currentText().lower()=="material":
            self.form.show_dialog_insert_material()
        elif self.edit_database.currentText().lower()=="directive":
            self.form.show_dialog_add_directive(self)
        self.call_show_table_database(None)
            
        
