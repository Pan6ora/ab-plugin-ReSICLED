from ctypes import alignment
import sys
from xml.etree.ElementTree import indent
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
from ..signals import signals



class Form(QDialog):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        #set
        self.class_dialog_insert_component = None
        
    def show_dialog(self):
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
        dialog_dialog_alert = Dialog_alert(message)
        dialog_dialog_alert.exec_()
        
    def show_dialog_insert_directive(self, parent_class, type_scenario):
        dialog_insert_directive= Dialog_insert_directive(type_scenario, parent=parent_class)
        dialog_insert_directive.exec_()
        
    def show_dialog_question(self, parent, text_question):
        reply = QMessageBox.question(parent, "Question Message", text_question, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        elif reply == QMessageBox.No:
            return False

    def show_dialog_add_directive(self, parent):
        dialog_add_directive = Dialog_add_directive(parent)
        dialog_add_directive.exec_()

    def show_dialog_change_strategy(self,parent2,item):
        dialog_change_strategy = Dialog_change_strategy(item,parent2)
        dialog_change_strategy.exec_()



class Dialog_alert(QDialog):
    def __init__(self, message, parent=None):
        QDialog.__init__(self, parent)
        self.info_label = QLabel(message)
        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.close)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.info_label)
        self.main_layout.addWidget(self.ok_button, alignment= Qt.AlignRight)
        self.setLayout(self.main_layout)
        self.setWindowTitle("Info")

    def close(self):
        self.accept()
                 
class Dialog_change_strategy(QDialog):
    def __init__(self, item, parent = None):
        QDialog.__init__(self,parent)
        self.item = item
        style = Style()
        self.databasemanager = DatabaseManager()
        self.strategy_change_widget = QWidget(self)
        self.buttons_widget = QWidget(self)

        # Buttons layout 
        close_button = QPushButton("Cancel")
        ok_button = QPushButton("Ok")
        close_button.clicked.connect(self.close)
        ok_button.clicked.connect(self.set_change_strategy)
        self.buttons_layout = QHBoxLayout(self)
        self.buttons_layout.addWidget(close_button)
        self.buttons_layout.addWidget(ok_button)
        self.buttons_widget.setLayout(self.buttons_layout)

        self.strategy_change_layout = QVBoxLayout()
        self.presentation_widget = QLabel("The responsibilitiy to change the strategy is for the designers.\n At least one of the following options should be checked to\n confirm why this element will be dismantled.")
        self.strategy_change_layout.addWidget(self.presentation_widget)
        self.checkbox1_widget = QCheckBox("Sufficient mass",self)
        self.checkbox2_widget = QCheckBox("Easily accessible (superficial)", self)
        self.checkbox3_widget = QCheckBox("Easily dismantled for obtaining mono-materials\n (reversible assembly)",self)
        self.checkbox4_widget = QCheckBox("Compensation of cost (Cost dismantling versus profit of\n the resale of recycled materials)",self)
        self.checkbox5_widget = QCheckBox("Dismantling done anyway (extraction of pollutants)",self)
        self.checkbox6_widget = QCheckBox("Signed agreement with recycler",self)
        self.checkbox7_widget = QWidget(self)
        self.checkbox7_layout = QHBoxLayout(self)
        self.cb7 = QCheckBox("Other",self)
        self.cb7_lineEdit = QLineEdit(self)
        self.checkbox7_layout.addWidget(self.cb7)
        self.checkbox7_layout.addWidget(self.cb7_lineEdit)
        self.checkbox7_widget.setLayout(self.checkbox7_layout)
        self.strategy_change_layout.addWidget(self.checkbox1_widget)
        self.strategy_change_layout.addWidget(self.checkbox2_widget)
        self.strategy_change_layout.addWidget(self.checkbox3_widget)
        self.strategy_change_layout.addWidget(self.checkbox4_widget)
        self.strategy_change_layout.addWidget(self.checkbox5_widget)
        self.strategy_change_layout.addWidget(self.checkbox6_widget)
        self.strategy_change_layout.addWidget(self.checkbox7_widget)
        self.comment_widget = QWidget(self)
        self.comment_layout = QHBoxLayout(self)
        self.comment_label = QLabel("Comment")
        self.comment_lineEdit = QLineEdit(self)
        self.comment_layout.addWidget(self.comment_label)
        self.comment_layout.addWidget(self.comment_lineEdit)
        self.comment_widget.setLayout(self.comment_layout)
        self.strategy_change_layout.addWidget(self.comment_widget)
        self.strategy_change_layout.setAlignment(Qt.AlignLeft)
        self.strategy_change_widget.setLayout(self.strategy_change_layout)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.strategy_change_widget)
        self.main_layout.addWidget(self.buttons_widget)
        self.setLayout(self.main_layout)
        self.setWindowTitle("Change of strategy")


    def set_change_strategy(self):
        current_compose = list(self.databasemanager.composedatabase.get_compose_by_component(self.item).values())[0]
        current_compose_key = list(self.databasemanager.composedatabase.get_compose_by_component(self.item).keys())[0][1]
        if current_compose["strategy_component"].lower()=="shredding":
            new_strategy = "Dismantling"
        else:
            new_strategy = "Shredding"
        self.databasemanager.composedatabase.change_strategy_one_compose(current_compose_key,new_strategy)
        self.close()

    def close(self):
        self.accept()

class Dialog_insert_directive(QDialog):
    def __init__(self, type_scenario, parent=None):
        QDialog.__init__(self,parent)
        #-- init
        self.parent = parent
        self.type_scenario = type_scenario
        self.databasemanager = DatabaseManager()
        #--- style ---
        style = Style()
        #--- QtWidget ---
        self.widget_directive = QWidget()
        self.widget_button = QWidget()
        
        #--- layout 
        self.layout_directive = QVBoxLayout()
        #---directive to select
        self.all_directive_form = self.databasemanager.directivedatabase.get_all_directive()
        self.dict_var = dict()
        for key, value in self.all_directive_form.items():
            # The input
            self.dict_var[key] = QRadioButton(str(value['name']), self)
            # signal
            self.dict_var[key].toggled.connect(self.set_value_directive)
            
            # addWidget
            self.layout_directive.addWidget(self.dict_var[key])
        self.widget_directive.setLayout(self.layout_directive)
        
        # Les boutons
        self.bouton_close = QPushButton("Close")
        self.bouton_save = QPushButton("Save")
        self.bouton_close.setStyleSheet("background-color : red")
        #--- signal button ---
        self.bouton_close.clicked.connect(self.close)
        self.bouton_save.clicked.connect(self.set_insert_directive)
        #--- button layout --
        self.layout_button = QGridLayout()
        self.layout_button.addWidget(self.bouton_close,0,0)
        self.widget_button.setLayout(self.layout_button)
        
        #--- Final layout ---
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.widget_directive)
        self.layout_main.addWidget(style.horizontal_line())
        self.layout_main.addWidget(self.widget_button)
        self.setLayout(self.layout_main)
        self.setWindowTitle("Form add directive")
        
    @Slot(object)
    def update_menu_combobox(self, box: QComboBox):
        #---directive to select
        self.all_directive_form = self.databasemanager.directivedatabase.get_all_directive()
        box.clear()
        box.addItem("Select a directive")
        for key, value in self.all_directive_form.items():
            box.addItem(str(value['name_directive']), userData=value)
            
    def set_value_directive(self):
        #---directive to select
        for key, value in self.dict_var.items():
            radioButton = self.sender()
            if (radioButton.isChecked() and radioButton==value):
                if(str(self.type_scenario).lower()=="dismantling"):
                    self.parent.value_recycling_rate_directive.setText(str(round(float(self.all_directive_form[key]["dismantling_recycling_rate"])*100)) + "%")
                    self.parent.value_recovery_rate_directive.setText(str(round(float(self.all_directive_form[key]["dismantling_recovery_rate"])*100)) + "%")
                    self.parent.value_residual_waste_rate_directive.setText(str(round(float(self.all_directive_form[key]["dismantling_residual_waste_rate"])*100)) + "%")
                elif(str(self.type_scenario).lower()=="shredding"):
                    self.parent.value_recycling_rate_directive.setText(str(round(float(self.all_directive_form[key]["shredding_recycling_rate"])*100)) + "%")
                    self.parent.value_recovery_rate_directive.setText(str(round(float(self.all_directive_form[key]["shredding_recovery_rate"])*100)) + "%")
                    self.parent.value_residual_waste_rate_directive.setText(str(round(float(self.all_directive_form[key]["shredding_residual_waste_rate"])*100)) + "%")
                elif(str(self.type_scenario).lower()=="mixed"):
                    self.parent.value_recycling_rate_directive.setText(str(round(float(self.all_directive_form[key]["mixed_recycling_rate"])*100)) + "%")
                    self.parent.value_recovery_rate_directive.setText(str(round(float(self.all_directive_form[key]["mixed_recovery_rate"])*100)) + "%")
                    self.parent.value_residual_waste_rate_directive.setText(str(round(float(self.all_directive_form[key]["mixed_residual_waste_rate"])*100)) + "%")
                #set
                self.parent.value_directive_applied.setText(self.all_directive_form[key]["name"])
                self.parent.call_show_table_component_product(None)
                            
    def show_alert_information(self, message):
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print("OK")

    def close(self):
        self.accept()
        
    def set_insert_directive(self, value):
        rbtn = self.sender()
        if rbtn.isChecked() == True:
            #self.parent
            print("set_insert_directive",rbtn)
         
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
        self.databasemanager = DatabaseManager()
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
        self.all_product_form = self.databasemanager.productdatabase.get_all_product()
        box.clear()
        box.addItem("Select a product")
        for key, value in self.all_product_form.items():
            box.addItem(str(value['name_product']), userData=value)
        
    def show_alert_information(self, message):
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print("OK")

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
            self.databasemanager.productdatabase.insert_one_product(new_product)
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
        self.databasemanager = DatabaseManager()
        #--- QtWidget ---
        self.widget_component = QWidget()
        self.widget_component_material = QWidget()
        self.widget_button = QWidget()
        self.widget_button_component_material_add = QWidget()
        
        # The input
        self.edit_name_component = QLineEdit("")
        self.edit_component_weight = QLineEdit("")
        self.edit_component_numberofpieces = QLineEdit("1")
        self.edit_component_comments = QLineEdit("")
        self.edit_component_product = QComboBox()
        self.edit_component_isitpollutant = QComboBox()
        self.edit_component_material_polymer = QComboBox()
        self.edit_component_material_metal = QComboBox()
        self.edit_component_material_other = QComboBox()
        self.edit_component_material_personalmaterial = QComboBox()
        
        # init input
        #---product to select
        self.all_product = self.databasemanager.productdatabase.get_all_product()
        self.edit_component_product.addItem("Select a product", userData=None)
        for key_product, value_product in self.all_product.items():
            self.edit_component_product.addItem(str(value_product['name_product']), userData=value_product)
        #---It is polluant  to select
        self.edit_component_isitpollutant.addItem("Select")
        self.edit_component_isitpollutant.addItems(["Yes","No"])
        #---material_polymer to select
        self.all_material_polymer = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Polymers")
        self.edit_component_material_polymer.addItem("Select")
        for key, value in self.all_material_polymer.items():
            self.edit_component_material_polymer.addItem(str(value['name_material']), userData=value)
        #---material_metal to select
        self.all_material_metal = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Metals")
        self.edit_component_material_metal.addItem("Select")
        for key, value in self.all_material_metal.items():
            self.edit_component_material_metal.addItem(str(value['name_material']), userData=value)
        #---material_other to select
        self.all_material_other = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Other")
        self.edit_component_material_other.addItem("Select")
        for key, value in self.all_material_other.items():
            self.edit_component_material_other.addItem(str(value['name_material']), userData=value)
        #---material_personalmaterial to select
        self.all_material_personalmaterial = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Personal")
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
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print("OK")
    
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
            
        if (self.edit_component_product.currentIndex() > 0 and len(self.edit_name_component.text()) > 0 and len(self.edit_component_weight.text()) > 0 and len(self.edit_component_numberofpieces.text()) > 0 and int(self.edit_component_numberofpieces.text()) > 0 and len_type > 0):
            product_selected = self.edit_component_product.currentData()
            # Adding the initial result entry
            if material_selected["pollutant_material"]=="true":
                self.strategy = "Dismantling"
            elif material_selected["pollutant_material"]=="false":
                self.strategy = "Shredding"

            new_component = {
                "id_product": product_selected.__getitem__('id_product'),
                "id_material": id_material,
                "name_component": str(self.edit_name_component.text()),
                "weight_component": self.edit_component_weight.text(),
                "comment_component": str(self.edit_component_comments.text()),
                "piecenumber_component": self.edit_component_numberofpieces.text(),
                "strategy_component" : self.strategy
                }
            #insert in database
            self.databasemanager.composedatabase.insert_one_component(new_component)
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
        self.databasemanager = DatabaseManager()
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
        #---material_polymer to select
        self.all_material_polymer = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Polymers")
        self.class_dialog_insert_component.edit_component_material_polymer.clear()
        self.class_dialog_insert_component.edit_component_material_polymer.addItem("Select")
        for key, value in self.all_material_polymer.items():
            self.class_dialog_insert_component.edit_component_material_polymer.addItem(str(value['name_material']), userData=value)
        #---material_metal to select
        self.all_material_metal = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Metals")
        self.class_dialog_insert_component.edit_component_material_metal.clear()
        self.class_dialog_insert_component.edit_component_material_metal.addItem("Select")
        for key, value in self.all_material_metal.items():
            self.class_dialog_insert_component.edit_component_material_metal.addItem(str(value['name_material']), userData=value)
        #---material_other to select
        self.all_material_other = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Other")
        self.class_dialog_insert_component.edit_component_material_other.clear()
        self.class_dialog_insert_component.edit_component_material_other.addItem("Select")
        for key, value in self.all_material_other.items():
            self.class_dialog_insert_component.edit_component_material_other.addItem(str(value['name_material']), userData=value)
        #---material_personalmaterial to select
        self.all_material_personalmaterial = self.databasemanager.materialdatabase.get_material_by_attrib("type_material","Personal")
        self.class_dialog_insert_component.edit_component_material_personalmaterial.clear()
        self.class_dialog_insert_component.edit_component_material_personalmaterial.addItem("Select")
        for key, value in self.all_material_personalmaterial.items():
            self.class_dialog_insert_component.edit_component_material_personalmaterial.addItem(str(value['name_material']), userData=value)
        
    @Slot(str)
    def show_alert_information(self, message):
        reply = QMessageBox.question(self, "Info", message, QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            print("OK")
    
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
                "name": str(self.edit_name_material.text()),
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
            self.databasemanager.componentdatabase.insert_one_material(new_material)
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

class Dialog_add_directive(QDialog):
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        self.databasemanager = DatabaseManager()
        self.cancel_button = QPushButton("Cancel")
        self.ok_button = QPushButton("Save")
        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.save_inserted_directive)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_widget = QWidget(self)
        self.buttons_widget.setLayout(self.buttons_layout)

        rate_validator = QDoubleValidator(0.,100.,2,parent = self)
        self.edit_name = QLineEdit("")
        self.edit_comment = QLineEdit("")
        self.edit_recycling_rate = QLineEdit("")
        self.edit_recycling_rate.setValidator(rate_validator)
        self.edit_energy_recovery_rate = QLineEdit("")
        self.edit_energy_recovery_rate.setValidator(rate_validator)
        self.directive_add_layout = QFormLayout()
        self.directive_add_layout.addRow("Directive title : (*)",self.edit_name)
        self.directive_add_layout.addRow("Directive comment : ",self.edit_comment)
        self.directive_add_layout.addRow("Recycling rate (in %) : ", self.edit_recycling_rate)
        self.directive_add_layout.addRow("Energy recovery rate (in %) : ", self.edit_energy_recovery_rate)
        self.form_widget = QWidget(self)
        self.form_widget.setLayout(self.directive_add_layout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.form_widget)
        self.mainLayout.addWidget(self.buttons_widget)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Insert new directive")

    def save_inserted_directive(self):
        nb_directives = len(list(self.databasemanager.directivedatabase.get_all_directive().keys()))
        recycling_rate = float(self.edit_recycling_rate.text().replace(",","."))
        energy_recovery_rate = float(self.edit_energy_recovery_rate.text().replace(",","."))
        residual_waste_rate = 100. - (recycling_rate+energy_recovery_rate)
        saved_directive_dict = {
            "id_directive" : nb_directives+1,
            "name" : str(self.edit_name.text()),
            "comment" : str(self.edit_comment.text()),
            "dismantling_recycling_rate": recycling_rate/100.,
            "dismantling_recovery_rate": (100.-residual_waste_rate)/100.,
            "dismantling_residual_waste_rate": residual_waste_rate/100.,
            "shredding_recycling_rate": recycling_rate/100.,
            "shredding_recovery_rate": (100.-residual_waste_rate)/100.,
            "shredding_residual_waste_rate": residual_waste_rate/100.,
            "mixed_recycling_rate": recycling_rate/100.,
            "mixed_recovery_rate": (100.-residual_waste_rate)/100.,
            "mixed_residual_waste_rate": residual_waste_rate/100.
        }
        self.databasemanager.directivedatabase.insert_one_directive(saved_directive_dict)       
        self.close()

    def close(self):
        self.accept()
