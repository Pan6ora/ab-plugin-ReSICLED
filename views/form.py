import sys
from PySide2 import QtCore
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QLineEdit, QDialog, 
    QApplication, QDoubleSpinBox, QWidget, QFormLayout, QGridLayout, QComboBox
)
from PySide2.QtCore import Qt
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
        #-- buttons add material
        self.button_component_material_add = QPushButton("Create new material")
        self.layout_button_component_material_add = QGridLayout()
        self.layout_button_component_material_add.addWidget(self.button_component_material_add)
        self.widget_button_component_material_add.setLayout(self.layout_button_component_material_add)
        #--- signal buttons add material
        self.button_component_material_add.clicked.connect(self.save_insert_component)
        # form layout component
        self.layout_component = QFormLayout()
        self.layout_component.addRow("Product: ", self.edit_component_product)
        self.layout_component.addRow("Name  component: ", self.edit_name_component)
        self.layout_component.addRow(style.horizontal_line())
        self.layout_component.addRow("Weight (grams/piece) : ", self.edit_component_weight)
        self.layout_component.addRow("Is it pollutant ? : ", self.edit_component_isitpollutant)
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