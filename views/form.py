import sys
from PySide2 import QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QLineEdit, QDialog, 
    QApplication, QDoubleSpinBox, QWidget, QFormLayout, QGridLayout, QComboBox, QRadioButton
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator, QDoubleValidator
from .icon import Icon
from .style import Style
from ..databases.database import DatabaseManager
from ..controllers.signals import signals

databasemanager = DatabaseManager()

class Form(QDialog):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        #set
        self.class_dialog_insert_component = None
        
    def show_dialog(self):
        #app = QApplication(sys.argv)
        dialog = Dialog()
        dialog.exec_()
        
    def show_dialog_insert_product(self, box_product):
        dialog_insert_product= Dialog_insert_product(box_product)
        dialog_insert_product.exec_()
        
    def show_dialog_insert_component(self):
        dialog_insert_component = Dialog_insert_component()
        dialog_insert_component.exec_()
        
    def show_dialog_insert_material(self):
        dialog_insert_material = Dialog_insert_material(self.class_dialog_insert_component)
        dialog_insert_material.exec_()
        
    def show_dialog_alert(self, message):
        dialog_dialog_alert = Dialog_alert()
        dialog_dialog_alert.show_alert_information(message)
        dialog_dialog_alert.exec_()
        
    def show_question(self):
        reply = QMessageBox.question(self, "Question MessageBox", "Do You Like Pyside2", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.label.setText("I Like Pyside2")
        elif reply == QMessageBox.No:
            self.label.setText("I Dont Like Pyside2")


class Dialog_alert(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        
    @Slot(str)
    def show_alert_information(self, message):
        #reply = QMessageBox.information(self, "Info", message)
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.label.setText("OK")
        """
        elif reply == QMessageBox.Cancel:
            self.label.setText("CANCEL")
        """
         
class Dialog_insert_product(QDialog):
    def __init__(self, box_product, parent=None):
        QDialog.__init__(self,parent)
        #-- init
        self.box_product = box_product
        #--- style ---
        style = Style()
        #--- QtWidget ---
        self.widget_product = QWidget()
        self.widget_button = QWidget()
        # The input
        self.edit_name_product = QLineEdit("")
        self.edit_name_autor = QLineEdit("")
        self.edit_firstname_autor = QLineEdit("")
        # form layout
        self.layout_product = QFormLayout()
        self.layout_product.addRow("Name  product: (*)", self.edit_name_product)
        self.layout_product.addRow(style.horizontal_line())
        self.layout_product.addRow(QLabel("---- AUTHOR ----"))
        self.layout_product.addRow("Name : ", self.edit_name_autor)
        self.layout_product.addRow("First name : ", self.edit_firstname_autor)
        self.layout_product.addRow(QLabel("This (*) -> required"))
        self.widget_product.setLayout(self.layout_product)
        # Les boutons
        self.bouton_close = QPushButton("Close")
        self.bouton_save = QPushButton("Save")
        self.bouton_close.setStyleSheet("background-color : red")
        #--- signal button ---
        self.bouton_close.clicked.connect(self.close)
        self.bouton_save.clicked.connect(self.save_insert_product)
        #--- button layout --
        self.layout_button = QGridLayout()
        self.layout_button.addWidget(self.bouton_close,0,0)
        self.layout_button.addWidget(self.bouton_save,0,1)
        self.widget_button.setLayout(self.layout_button)
        #--- Final layout ---
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.widget_product)
        self.layout_main.addWidget(style.horizontal_line())
        self.layout_main.addWidget(self.widget_button)
        self.setLayout(self.layout_main)
        self.setWindowTitle("Form add product")
        
    @Slot(object)
    def update_menu_combobox(self, box: QComboBox):
        #---product to select
        self.all_product_form = databasemanager.productdatabase.get_all_product()
        box.clear()
        box.addItem("Select a product")
        for key, value in self.all_product_form.items():
            box.addItem(str(value['name_product']), userData=value)
        
    def show_alert_information(self, message):
        #reply = QMessageBox.information(self, "Info", message)
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.label.setText("OK")

    def close(self):
        self.accept()
        
    def save_insert_product(self):
        if (len(self.edit_name_product.text()) > 0):
            new_product = {
                "name_product": str(self.edit_name_product.text()),
                "nameauthor_product": str(self.edit_name_autor.text()),
                "firstname_product": str(self.edit_firstname_autor.text())
                }
            #insert in database
            databasemanager.productdatabase.insert_one_product(new_product)
            #signal update_combobox
            signals.update_combobox.connect(self.update_menu_combobox)
            signals.update_combobox.emit(self.box_product)
            #close form
            self.close()
            # show alert
            self.message = "Product added Successfully"
            self.show_alert_information(self.message)
            
            
        
class Dialog_insert_component(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        #--- style ---
        style = Style()
        #--- QtWidget ---
        self.widget_component = QWidget()
        self.widget_component_material = QWidget()
        self.widget_button = QWidget()
        self.widget_button_component_material_add = QWidget()
        
        # The input
        self.edit_name_component = QLineEdit("")
        self.edit_component_weight = QLineEdit("")
        self.edit_component_numberofpieces = QLineEdit("")
        self.edit_component_comments = QLineEdit("")
        self.edit_component_product = QComboBox()
        self.edit_component_isitpollutant = QComboBox()
        self.edit_component_material_polymer = QComboBox()
        self.edit_component_material_metal = QComboBox()
        self.edit_component_material_other = QComboBox()
        self.edit_component_material_personalmaterial = QComboBox()
        
        # init input
        #---product to select
        self.all_product = databasemanager.productdatabase.get_all_product()
        self.edit_component_product.addItem("Select a product", userData=None)
        for key_product, value_product in self.all_product.items():
            self.edit_component_product.addItem(str(value_product['name_product']), userData=value_product)
        #---It is polluant  to select
        self.edit_component_isitpollutant.addItem("Select")
        self.edit_component_isitpollutant.addItems(["Yes","No"])
        #---material_polymer to select
        self.all_material_polymer = databasemanager.materialdatabase.get_material_by_attrib("type_material","Polymers")
        self.edit_component_material_polymer.addItem("Select")
        for key, value in self.all_material_polymer.items():
            self.edit_component_material_polymer.addItem(str(value['name_material']), userData=value)
        #---material_metal to select
        self.all_material_metal = databasemanager.materialdatabase.get_material_by_attrib("type_material","Metals")
        self.edit_component_material_metal.addItem("Select")
        for key, value in self.all_material_metal.items():
            self.edit_component_material_metal.addItem(str(value['name_material']), userData=value)
        #---material_other to select
        self.all_material_other = databasemanager.materialdatabase.get_material_by_attrib("type_material","Other")
        self.edit_component_material_other.addItem("Select")
        for key, value in self.all_material_other.items():
            self.edit_component_material_other.addItem(str(value['name_material']), userData=value)
        #---material_personalmaterial to select
        self.all_material_personalmaterial = databasemanager.materialdatabase.get_material_by_attrib("type_material","Personal")
        self.edit_component_material_personalmaterial.addItem("Select")
        for key, value in self.all_material_personalmaterial.items():
            self.edit_component_material_personalmaterial.addItem(str(value['name_material']), userData=value)
        #add signal
        self.edit_component_material_polymer.currentIndexChanged.connect(
            self.reset_orthers_component_material_polymer
        )
        self.edit_component_material_metal.currentIndexChanged.connect(
            self.reset_orthers_component_material_metal
        )
        self.edit_component_material_other.currentIndexChanged.connect(
            self.reset_orthers_component_material_other
        )
        self.edit_component_material_personalmaterial.currentIndexChanged.connect(
            self.reset_orthers_component_material_personalmaterial
        )
         # validator
        self.validator_int = QIntValidator(self)
        self.validator_double = QDoubleValidator(self)
        self.edit_component_numberofpieces.setValidator(self.validator_int)
        self.edit_component_weight.setValidator(self.validator_double)
        #-- buttons add material
        self.button_component_material_add = QPushButton("Create new material")
        self.layout_button_component_material_add = QGridLayout()
        self.layout_button_component_material_add.addWidget(self.button_component_material_add)
        self.widget_button_component_material_add.setLayout(self.layout_button_component_material_add)
        #--- signal buttons add material
        self.form = Form()
        self.form.class_dialog_insert_component = self
        self.button_component_material_add.clicked.connect(self.form.show_dialog_insert_material)
        # form layout component
        self.layout_component = QFormLayout()
        self.layout_component.addRow("Product: (*)", self.edit_component_product)
        self.layout_component.addRow("Name  component: (*)", self.edit_name_component)
        self.layout_component.addRow(style.horizontal_line())
        self.layout_component.addRow("Weight (grams/piece) :(*) ", self.edit_component_weight)
        #self.layout_component.addRow("Is it pollutant ? : ", self.edit_component_isitpollutant)
        self.layout_component.addRow("Number of pieces :(*) ", self.edit_component_numberofpieces)
        self.layout_component.addRow("Comment : ", self.edit_component_comments)
        self.widget_component.setLayout(self.layout_component)
        # form layout material
        self.layout_component_material = QFormLayout()
        self.layout_component_material.addRow(QLabel("-------Material------- (*)"))
        self.layout_component_material.addRow("Polymer: ", self.edit_component_material_polymer)
        self.layout_component_material.addRow("Metal : ", self.edit_component_material_metal)
        self.layout_component_material.addRow("Other : ", self.edit_component_material_other)
        self.layout_component_material.addRow("Personal data : ", self.edit_component_material_personalmaterial)
        self.widget_component_material.setStyleSheet("border: solid 1px;")
        self.widget_component_material.setLayout(self.layout_component_material)
        #-- buttons close and save
        self.bouton_close = QPushButton("Close")
        self.bouton_save = QPushButton("Save")
        self.bouton_close.setStyleSheet("background-color : red")
        #--- signal button ---
        self.bouton_close.clicked.connect(self.close)
        self.bouton_save.clicked.connect(self.save_insert_component)
        #--- signal select combobox
        #self.edit_component_isitpollutant.currentIndexChanged.connect(self.selectionchange)
        #--- button layout --
        self.layout_button = QGridLayout()
        self.layout_button.addWidget(self.bouton_close,0,0)
        self.layout_button.addWidget(self.bouton_save,0,1)
        self.widget_button.setLayout(self.layout_button)
        #--- Final layout ---
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.widget_component)
        self.layout_main.addWidget(self.widget_component_material)
        self.layout_main.addWidget(self.widget_button_component_material_add)
        self.layout_main.addWidget(QLabel("This (*) -> required"))
        self.layout_main.addWidget(style.horizontal_line())
        self.layout_main.addWidget(self.widget_button)
        self.setLayout(self.layout_main)
        self.setWindowTitle("Form add component")
        
        """
        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem("C")
        self.cb.addItem("C++")
        self.cb.addItems(["Java", "C#", "Python"])
        self.cb.currentIndexChanged.connect(self.selectionchange)
        """
    def reset_orthers_component_material_polymer(self,index):
        #reset selection for
        self.edit_component_material_metal.setCurrentIndex(0)
        self.edit_component_material_other.setCurrentIndex(0)
        self.edit_component_material_personalmaterial.setCurrentIndex(0)
        self.edit_component_material_polymer.setCurrentIndex(index)
        
    def reset_orthers_component_material_metal(self,index):
        #reset selection for
        self.edit_component_material_polymer.setCurrentIndex(0)
        self.edit_component_material_other.setCurrentIndex(0)
        self.edit_component_material_personalmaterial.setCurrentIndex(0)
        self.edit_component_material_metal.setCurrentIndex(index)
    
    def reset_orthers_component_material_other(self,index):
        #reset selection for
        self.edit_component_material_polymer.setCurrentIndex(0)
        self.edit_component_material_metal.setCurrentIndex(0)
        self.edit_component_material_personalmaterial.setCurrentIndex(0)
        self.edit_component_material_other.setCurrentIndex(index)
        
    def reset_orthers_component_material_personalmaterial(self,index):
        #reset selection for
        self.edit_component_material_polymer.setCurrentIndex(0)
        self.edit_component_material_metal.setCurrentIndex(0)
        self.edit_component_material_other.setCurrentIndex(0)
        self.edit_component_material_personalmaterial.setCurrentIndex(index)
        
    @Slot(str)
    def show_alert_information(self, message):
        #reply = QMessageBox.information(self, "Info", message)
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.label.setText("OK")
    
    def close(self):
        self.accept()
        
    def save_insert_component(self):
        id_material = ""
        len_type = self.edit_component_material_polymer.currentIndex() + self.edit_component_material_metal.currentIndex() + self.edit_component_material_other.currentIndex() + self.edit_component_material_personalmaterial.currentIndex()
        if(self.edit_component_material_polymer.currentIndex()>0):
            material_selected = self.edit_component_material_polymer.currentData()
            id_material = material_selected.__getitem__('id_material')
        elif(self.edit_component_material_metal.currentIndex()>0):
            material_selected = self.edit_component_material_metal.currentData()
            id_material = material_selected.__getitem__('id_material')
        elif(self.edit_component_material_other.currentIndex()>0):
            material_selected = self.edit_component_material_other.currentData()
            id_material = material_selected.__getitem__('id_material')
        elif(self.edit_component_material_personalmaterial.currentIndex()>0):
            material_selected = self.edit_component_material_personalmaterial.currentData()
            id_material = material_selected.__getitem__('id_material')
            
        if (self.edit_component_product.currentIndex() > 0 and len(self.edit_name_component.text()) > 0 and len(self.edit_component_weight.text()) > 0 and len(self.edit_component_numberofpieces.text()) > 0 and len_type > 0):
            product_selected = self.edit_component_product.currentData()
            new_component = {
                "id_product": product_selected.__getitem__('id_product'),
                "id_material": id_material,
                "name_component": str(self.edit_name_component.text()),
                "weight_component": self.edit_component_weight.text(),
                "comment_component": str(self.edit_component_comments.text()),
                "piecenumber_component": self.edit_component_numberofpieces.text(),
                }
            #insert in database
            databasemanager.composedatabase.insert_one_component(new_component)
            """#signal update_combobox
            signals.update_combobox.connect(self.update_menu_combobox)
            signals.update_combobox.emit(self.box_product)"""
            #close form
            self.close()
            # show alert
            self.message = "Component added Successfully"
            self.show_alert_information(self.message)
        
        
class Dialog_insert_material(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        #--- init
        self.class_dialog_insert_component = parent
        #--- style ---
        style = Style()
        #--- QtWidget ---
        self.widget_material = QWidget()
        self.widget_button = QWidget()
        # The input
        self.edit_name_material = QLineEdit("")
        self.edit_type_material = QLineEdit("")
        self.edit_recdis_material = QLineEdit("")
        self.edit_recodis_material = QLabel()
        self.edit_enerdis_material = QLineEdit("")
        self.edit_wastedis_material = QLabel()
        self.edit_recshr_material = QLineEdit("")
        self.edit_recoshr_material = QLabel()
        self.edit_enershr_material = QLineEdit("")
        self.edit_wasteshr_material = QLabel()
        self.edit_pollutant_material = QComboBox()
        self.edit_type_material = QComboBox()
        self.edit_price_material = QLineEdit("")
        # init input
        self.edit_pollutant_material.addItem("Select")
        self.edit_pollutant_material.addItems(["Yes","No"])
        self.edit_type_material.addItem("Select")
        self.edit_type_material.addItems(["Polymer","Metal","Other","Personal"])
        # validator
        self.validator_int = QIntValidator(0, 100, self)
        self.edit_recdis_material.setValidator(self.validator_int)
        self.edit_enerdis_material.setValidator(self.validator_int)
        self.edit_recshr_material.setValidator(self.validator_int)
        self.edit_enershr_material.setValidator(self.validator_int)
        # signal
        self.edit_recdis_material.textChanged.connect(self.get_recoverydis)
        self.edit_enerdis_material.textChanged.connect(self.get_recoverydis)
        self.edit_enerdis_material.textChanged.connect(self.get_residualwastedis)
        self.edit_recshr_material.textChanged.connect(self.get_recoveryshr)
        self.edit_enershr_material.textChanged.connect(self.get_recoveryshr)
        self.edit_enershr_material.textChanged.connect(self.get_residualwasteshr)
        # form layout
        self.layout_material = QFormLayout()
        self.layout_material.addRow("Name  Material: (*)", self.edit_name_material)
        self.layout_material.addRow(style.horizontal_line())
        self.layout_material.addRow("Type : (*)", self.edit_type_material)
        self.layout_material.addRow("Is it pollutant ? : (*)", self.edit_pollutant_material)
        self.layout_material.addRow(QLabel("---- RATES After Dismantling ----"))
        self.layout_material.addRow("Recycling (%) : (*)", self.edit_recdis_material)
        self.layout_material.addRow("Energy recovery (%) : (*)", self.edit_enerdis_material)
        self.layout_material.addRow("Recovery (%) : ", self.edit_recodis_material)
        self.layout_material.addRow("Residual waste (%) : ", self.edit_wastedis_material)
        self.layout_material.addRow(QLabel("---- RATES After Shredding ----"))
        self.layout_material.addRow("Recycling (%) : (*)", self.edit_recshr_material)
        self.layout_material.addRow("Energy recovery (%) : (*)", self.edit_enershr_material)
        self.layout_material.addRow("Recovery (%) : ", self.edit_recoshr_material)
        self.layout_material.addRow("Residual waste (%) : ", self.edit_wasteshr_material)
        self.widget_material.setLayout(self.layout_material)
        # Les boutons
        self.bouton_close = QPushButton("Close")
        self.bouton_save = QPushButton("Save")
        self.bouton_close.setStyleSheet("background-color : red")
        #--- signal button ---
        self.bouton_close.clicked.connect(self.close)
        self.bouton_save.clicked.connect(self.save_insert_material)
        #--- button layout --
        self.layout_button = QGridLayout()
        self.layout_button.addWidget(self.bouton_close,0,0)
        self.layout_button.addWidget(self.bouton_save,0,1)
        self.widget_button.setLayout(self.layout_button)
        #--- Final layout ---
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.widget_material)
        self.layout_main.addWidget(QLabel("This (*) -> required"))
        self.layout_main.addWidget(style.horizontal_line())
        self.layout_main.addWidget(self.widget_button)
        self.setLayout(self.layout_main)
        self.setWindowTitle("Form add material")
        
    @Slot(object)
    def update_menu_combobox_component_material(self, class_dialog_insert_component):        
        """self.class_dialog_insert_component.edit_component_material_polymer
        self.class_dialog_insert_component.edit_component_material_metal
        self.class_dialog_insert_component.edit_component_material_other
        self.class_dialog_insert_component.edit_component_material_personalmaterial"""
        #---material_polymer to select
        self.all_material_polymer = databasemanager.materialdatabase.get_material_by_attrib("type_material","Polymers")
        self.class_dialog_insert_component.edit_component_material_polymer.clear()
        self.class_dialog_insert_component.edit_component_material_polymer.addItem("Select")
        for key, value in self.all_material_polymer.items():
            self.class_dialog_insert_component.edit_component_material_polymer.addItem(str(value['name_material']), userData=value)
        #---material_metal to select
        self.all_material_metal = databasemanager.materialdatabase.get_material_by_attrib("type_material","Metals")
        self.class_dialog_insert_component.edit_component_material_metal.clear()
        self.class_dialog_insert_component.edit_component_material_metal.addItem("Select")
        for key, value in self.all_material_metal.items():
            self.class_dialog_insert_component.edit_component_material_metal.addItem(str(value['name_material']), userData=value)
        #---material_other to select
        self.all_material_other = databasemanager.materialdatabase.get_material_by_attrib("type_material","Other")
        self.class_dialog_insert_component.edit_component_material_other.clear()
        self.class_dialog_insert_component.edit_component_material_other.addItem("Select")
        for key, value in self.all_material_other.items():
            self.class_dialog_insert_component.edit_component_material_other.addItem(str(value['name_material']), userData=value)
        #---material_personalmaterial to select
        self.all_material_personalmaterial = databasemanager.materialdatabase.get_material_by_attrib("type_material","Personal")
        self.class_dialog_insert_component.edit_component_material_personalmaterial.clear()
        self.class_dialog_insert_component.edit_component_material_personalmaterial.addItem("Select")
        for key, value in self.all_material_personalmaterial.items():
            self.class_dialog_insert_component.edit_component_material_personalmaterial.addItem(str(value['name_material']), userData=value)
        
    @Slot(str)
    def show_alert_information(self, message):
        #reply = QMessageBox.information(self, "Info", message)
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.label.setText("OK")
    
    def close(self):
        self.accept()
        
    def save_insert_material(self):
        if (len(self.edit_name_material.text()) > 0 and 
            self.edit_type_material.currentIndex() > 0 and 
            self.edit_pollutant_material.currentIndex()> 0 and 
            len(self.edit_recdis_material.text()) > 0 and 
            len(self.edit_enerdis_material.text()) > 0 and 
            len(self.edit_wastedis_material.text()) > 0 and 
            len(self.edit_recshr_material.text()) > 0 and 
            len(self.edit_enershr_material.text()) > 0 and 
            len(self.edit_wasteshr_material.text()) > 0):
            type_material_selected = self.edit_type_material.currentText()
            pollutant_selected = self.edit_pollutant_material.currentText()
            #rename value material
            if(type_material_selected.lower()=="polymer"):
                type_material_selected = "Polymers"
            elif(type_material_selected.lower()=="metal"):
                type_material_selected = "Metals"
            elif(type_material_selected.lower()=="other"):
                type_material_selected = "Other"
            elif(type_material_selected.lower()=="personal"):
                type_material_selected = "Personal"
            # rename value pollutant
            if(pollutant_selected.lower()=="Yes"):
                pollutant_selected = "true"
            else:
                pollutant_selected = "false"
            # new material
            new_material = {
                "type_material": type_material_selected,
                "name_material": str(self.edit_name_material.text()),
                "recdis_material": self.edit_recdis_material.text(),
                "enerdis_material": self.edit_enerdis_material.text(),
                "wastedis_material": self.edit_wastedis_material.text(),
                "recshr_material": self.edit_recshr_material.text(),
                "enershr_material": self.edit_enershr_material.text(),
                "wasteshr_material": self.edit_wasteshr_material.text(),
                "price_material": self.edit_price_material.text(),
                "pollutant_material": pollutant_selected,
                }
            #insert in database
            databasemanager.componentdatabase.insert_one_material(new_material)
            #signal update_combobox
            signals.update_combobox.connect(self.update_menu_combobox_component_material)
            signals.update_combobox.emit(self.class_dialog_insert_component)
            #close form
            self.close()
            # show alert
            self.message = "Material added Successfully"
            self.show_alert_information(self.message)
        
    def get_recoverydis(self, text):
        """ recovery_rate = recycling_rate + Energy_rate """
        rate = str(int(self.edit_recdis_material.text()) + int(self.edit_enerdis_material.text()))
        self.edit_recodis_material.setText(rate)
        #self.edit_recdis_material.adjustSize()
        
    def get_recoveryshr(self, text):
        """ recovery_rate = recycling_rate + Energy_rate """
        rate = str(int(self.edit_recshr_material.text()) + int(self.edit_enershr_material.text()))
        self.edit_recoshr_material.setText(rate)
        
    def get_residualwastedis(self, text):
        """ Residual waste = 100 - energy_recovery_rate  """
        rate = str(100 - (int(self.edit_recdis_material.text()) + int(self.edit_enerdis_material.text())))
        self.edit_wastedis_material.setText(rate)
        
    def get_residualwasteshr(self, text):
        """ Residual waste = 100 - energy_recovery_rate  """
        rate = str(100 - (int(self.edit_recshr_material.text()) + int(self.edit_enershr_material.text())))
        self.edit_wasteshr_material.setText(rate)
        
    
class Dialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setWindowTitle("Saisie de tarif")
        self.__labelLibelle = QLabel("Libellé : ")
        self.__champLibelle = QLineEdit("")
        self.__layoutLibelle = QHBoxLayout()
        self.__layoutLibelle.addWidget(self.__labelLibelle)
        self.__layoutLibelle.addWidget(self.__champLibelle)
        self.__labelPrixHT = QLabel("Prix HT : ")
        self.__champPrixHT = QDoubleSpinBox()
        self.__champPrixHT.setSuffix("€")
        self.__labelTauxTVA = QLabel("TVA : ")
        self.__champTauxTVA = QDoubleSpinBox()
        self.__champTauxTVA.setSuffix("%")
        self.__layoutPrix = QHBoxLayout()
        self.__layoutPrix.addWidget(self.__labelPrixHT)
        self.__layoutPrix.addWidget(self.__champPrixHT)
        self.__layoutPrix.addWidget(self.__labelTauxTVA)
        self.__layoutPrix.addWidget(self.__champTauxTVA)
        self.__boutonAnnuler = QPushButton("Annuler")
        self.__boutonValider = QPushButton("Valider")
        self.__layoutBoutons = QHBoxLayout()
        self.__layoutBoutons.addWidget(self.__boutonAnnuler)
        self.__layoutBoutons.addStretch()
        self.__layoutBoutons.addWidget(self.__boutonValider)
        self.__layoutPrincipal = QVBoxLayout()
        self.__layoutPrincipal.addLayout(self.__layoutLibelle)
        self.__layoutPrincipal.addLayout(self.__layoutPrix)
        self.__layoutPrincipal.addLayout(self.__layoutBoutons)
        self.setLayout(self.__layoutPrincipal)    