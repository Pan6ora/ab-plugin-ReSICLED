import sys
from PySide2 import QtCore
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QLineEdit, QDialog, 
    QApplication, QDoubleSpinBox, QWidget, QFormLayout, QGridLayout, QComboBox
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator, QDoubleValidator
from .icon import Icon
from .style import Style

class Form(QDialog):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
    def show_dialog(self):
        #app = QApplication(sys.argv)
        dialog = Dialog()
        dialog.exec_()
        
    def show_dialog_insert_product(self):
        dialog_insert_product= Dialog_insert_product()
        dialog_insert_product.exec_()
        
    def show_dialog_insert_component(self):
        dialog_insert_component = Dialog_insert_component()
        dialog_insert_component.exec_()
        
    def show_dialog_insert_material(self):
        dialog_insert_material = Dialog_insert_material()
        dialog_insert_material.exec_()
        
    def show_question(self):
        reply = QMessageBox.question(self, "Question MessageBox", "Do You Like Pyside2", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.label.setText("I Like Pyside2")
        elif reply == QMessageBox.No:
            self.label.setText("I Dont Like Pyside2")
            

class Dialog_insert_product(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
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
        self.layout_product.addRow("Name  product: ", self.edit_name_product)
        self.layout_product.addRow(style.horizontal_line())
        self.layout_product.addRow(QLabel("---- AUTHOR ----"))
        self.layout_product.addRow("Name : ", self.edit_name_autor)
        self.layout_product.addRow("First name : ", self.edit_firstname_autor)
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
    
    def close(self):
        self.accept()
        
    def save_insert_product(self):
        name_product_value= self.edit_name_product.value()
 
       
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
        self.edit_component_product.addItem("Select")
        self.edit_component_isitpollutant.addItem("Select")
        self.edit_component_isitpollutant.addItems(["Yes","No"])
        self.edit_component_material_polymer.addItem("Select")
        self.edit_component_material_metal.addItem("Select")
        self.edit_component_material_other.addItem("Select")
        self.edit_component_material_personalmaterial.addItem("Select")
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
        self.button_component_material_add.clicked.connect(self.form.show_dialog_insert_material)
        # form layout component
        self.layout_component = QFormLayout()
        self.layout_component.addRow("Product: ", self.edit_component_product)
        self.layout_component.addRow("Name  component: ", self.edit_name_component)
        self.layout_component.addRow(style.horizontal_line())
        self.layout_component.addRow("Weight (grams/piece) : ", self.edit_component_weight)
        #self.layout_component.addRow("Is it pollutant ? : ", self.edit_component_isitpollutant)
        self.layout_component.addRow("Number of pieces : ", self.edit_component_numberofpieces)
        self.layout_component.addRow("Comment : ", self.edit_component_comments)
        self.widget_component.setLayout(self.layout_component)
        # form layout material
        self.layout_component_material = QFormLayout()
        self.layout_component_material.addRow(QLabel("-------Material-------"))
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
    
    def close(self):
        self.accept()
        
    def save_insert_component(self):
        name_component_value= self.edit_name_component.value()
        
        
class Dialog_insert_material(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
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
        self.edit_type_material.addItems(["Polymer","Metal","Other"])
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
        self.layout_material.addRow("Name  Material: ", self.edit_name_material)
        self.layout_material.addRow(style.horizontal_line())
        self.layout_material.addRow("Type : ", self.edit_type_material)
        self.layout_material.addRow("Is it pollutant ? : ", self.edit_pollutant_material)
        self.layout_material.addRow(QLabel("---- RATES After Dismantling ----"))
        self.layout_material.addRow("Recycling (%) : ", self.edit_recdis_material)
        self.layout_material.addRow("Energy recovery (%) : ", self.edit_enerdis_material)
        self.layout_material.addRow("Recovery (%) : ", self.edit_recodis_material)
        self.layout_material.addRow("Residual waste (%) : ", self.edit_wastedis_material)
        self.layout_material.addRow(QLabel("---- RATES After Shredding ----"))
        self.layout_material.addRow("Recycling (%) : ", self.edit_recshr_material)
        self.layout_material.addRow("Energy recovery (%) : ", self.edit_enershr_material)
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
        self.layout_main.addWidget(style.horizontal_line())
        self.layout_main.addWidget(self.widget_button)
        self.setLayout(self.layout_main)
        self.setWindowTitle("Form add product")
    
    def close(self):
        self.accept()
        
    def save_insert_material(self):
        name_material_value= self.edit_name_material.value()
        
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
        rate = str(100 - int(self.edit_enerdis_material.text()))
        self.edit_wastedis_material.setText(rate)
        
    def get_residualwasteshr(self, text):
        """ Residual waste = 100 - energy_recovery_rate  """
        rate = str(100 - int(self.edit_enershr_material.text()))
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