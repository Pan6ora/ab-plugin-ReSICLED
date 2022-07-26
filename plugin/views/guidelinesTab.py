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



class GuidelinesTab(QTabWidget):
    def __init__(self, parent= None):
        super(GuidelinesTab,self).__init__(parent)
        self.icon = Icon()
        self.form=Form()
        self.style= Style()
        self.databasemanager = DatabaseManager()

        # --- comboboxes ---
        self.cb1_items = ["All", "Reduce", "Depollution", "Re-use / remanufacture / repair", "Recycle / recover after dismantling (RAD)", 'Recycle / recover after shredding (RAS)', "Energy recovery"]
        self.cb2_items = ["All", "Material / composant / substance", "Links", "Architecture"]
        self.cb3_items = ["All", "Superficial", "Deep"]
        self.cb4_items = ["All", "Polymer", "Metal", "Electric"]
        
        #--- title ---
        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> GUIDELINES </h1>')
        self.title.move(10,50)

        

        self.recov_strat_widget = QWidget(self)
        self.recov_strat_layout = QHBoxLayout(self)
        self.cb1_title = QLabel(self)
        self.cb1_title.setText('Recovery strategy :')
        self.recov_strat_layout.addWidget(self.cb1_title)
        self.cb1 = QComboBox(self)
        for elem in self.cb1_items:
            self.cb1.addItem(elem, userData=elem)
        self.cb1.currentIndexChanged.connect(self.update_table)
        self.recov_strat_layout.addWidget(self.cb1)
        self.recov_strat_layout.setAlignment(Qt.AlignRight)
        self.recov_strat_widget.setLayout(self.recov_strat_layout)

        self.design_widget = QWidget(self)
        self.design_layout = QHBoxLayout(self)
        self.cb2_title = QLabel(self)
        self.cb2_title.setText("Design Parameters : ")
        self.design_layout.addWidget(self.cb2_title)
        self.cb2 = QComboBox(self)
        for elem in self.cb2_items:
            self.cb2.addItem(elem,userData = elem)
        self.cb2.currentIndexChanged.connect(self.update_table)
        self.design_layout.addWidget(self.cb2)
        self.design_layout.setAlignment(Qt.AlignRight)
        self.design_widget.setLayout(self.design_layout)

        self.position_widget = QWidget(self)
        self.position_layout = QHBoxLayout(self)
        self.cb3_title = QLabel(self)
        self.cb3_title.setText("Position of part / assembly \n in product architecture")
        self.position_layout.addWidget(self.cb3_title)
        self.cb3 = QComboBox(self)
        for elem in self.cb3_items:
            self.cb3.addItem(elem,userData=elem)
        self.cb3.currentIndexChanged.connect(self.update_table)
        self.position_layout.addWidget(self.cb3)
        self.position_layout.setAlignment(Qt.AlignRight)
        self.position_widget.setLayout(self.position_layout)

        self.part_type_widget=QWidget(self)
        self.part_type_layout = QHBoxLayout(self)
        self.cb4_title = QLabel(self)
        self.cb4_title.setText("part type : ")
        self.part_type_layout.addWidget(self.cb4_title)
        self.cb4 = QComboBox(self)
        for elem in self.cb4_items:
            self.cb4.addItem(elem, userData = elem)
        self.cb4.currentIndexChanged.connect(self.update_table)
        self.part_type_layout.addWidget(self.cb4)
        self.part_type_layout.setAlignment(Qt.AlignRight)
        self.part_type_widget.setLayout(self.part_type_layout)
       
        self.comboboxes_widget = QWidget(self)
        self.menu_layout = QGridLayout(self)
        self.menu_layout.addWidget(self.cb1_title,0,0)
        self.menu_layout.addWidget(self.cb1,0,1)
        self.menu_layout.addWidget(self.cb2_title,1,0)
        self.menu_layout.addWidget(self.cb2,1,1)
        self.menu_layout.addWidget(self.cb3_title,2,0)
        self.menu_layout.addWidget(self.cb3,2,1)
        self.menu_layout.addWidget(self.cb4_title,3,0)
        self.menu_layout.addWidget(self.cb4,3,1)
        self.comboboxes_widget.setLayout(self.menu_layout)
        self.comboboxes_widget.move(200,10)
        self.comboboxes_widget.show()

        #default, showing all guidelines
        self.datamodel = Datamodel()
        self.data_list = self.datamodel.get_data_guidelines()
        self.table_model= TableModel(self,self.data_list,[""])
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.font=QFont("Courrier New", 10)
        self.table_view.setFont(self.font)
        self.table_view.resizeColumnsToContents()
        self.widget_table_view = QWidget(self)
        self.layout_table_view = QVBoxLayout(self)
        self.layout_table_view.addWidget(self.table_view)
        self.widget_table_view.setLayout(self.layout_table_view)
        self.widget_table_view.setGeometry(10, 150, 800, 500)
        self.widget_table_view.show()

    
    def update_guidelines_cb1(self):
        # Updating the list visibility based on if we want to see any guideline or not
        self.criteria_1 = self.cb1.currentData()
        for i in range(self.table_model.rowCount(self)):
            value = self.databasemanager.guidelinesdatabase.get_one_guideline(i+1)
            if self.criteria_1=="All":
                pass
            elif self.criteria_1=="Reduce":
                if value["recovery_strategy"]!="Reduce" and value["recovery_strategy"]!="All":
                    self.table_view.hideRow(i)
            elif self.criteria_1=="Depollution":
                if value["recovery_strategy"]!="Depollution" and value["recovery_strategy"]!="All" and value["recovery_strategy"]!="D&RAD":
                    self.table_view.hideRow(i)
            elif self.criteria_1=="Re-use / remanufacture / repair":
                if value["recovery_strategy"]!="Re-use / remanufacture / repair" and value["recovery_strategy"]!="All":
                    self.table_view.hideRow(i)
            elif self.criteria_1=="Recycle / recover after dismantling (RAD)":
            
                if value["recovery_strategy"]!="Recycle / recover after dismantling (RAD)" and value["recovery_strategy"]!="All" and value["recovery_strategy"]!="RAD&RAS" and value["recovery_strategy"]!="D&RAD":
                    self.table_view.hideRow(i)
            elif self.criteria_1=="Recycle / recover after shredding (RAS)":
                if value["recovery_strategy"]!="Recycle / recover after shredding (RAS)" and value["recovery_strategy"]!="All" and value["recovery_strategy"]!="RAD&RAS":
                    self.table_view.hideRow(i)
            elif self.criteria_1=="Energy recovery":

                if value["recovery_strategy"]!="Energy recovery" and value["recovery_strategy"]!="All":
                    self.table_view.hideRow(i)

    def update_guidelines_cb2(self):
        self.criteria_2 = self.cb2.currentData()
        for i in range(self.table_model.rowCount(self)):
            value =self.databasemanager.guidelinesdatabase.get_one_guideline(i+1)
            if self.criteria_2=="All":
                pass
            elif self.criteria_2=="Material / composant / substance":
                if value["design_parameters"]!="Material / composant / substance" and value["design_parameters"]!="M&L" and value["design_parameters"]!="M&A" and value["design_parameters"]!="All":
                    self.table_view.hideRow(i)
            elif self.criteria_2=="Links":
                if value["design_parameters"]!="Links" and value["design_parameters"]!="M&L" and value["design_parameters"]!="L&A" and value["design_parameters"]!="All":
                    self.table_view.hideRow(i)
            elif self.criteria_2=="Architecture":
                if value["design_parameters"]!="Architecture" and value["design_parameters"]!="M&A" and value["design_parameters"]!="L&A" and value["design_parameters"]!="All":
                    self.table_view.hideRow(i)

    def update_guidelines_cb3(self): 
        self.criteria_3 = self.cb3.currentData()
        for i in range(self.table_model.rowCount(self)):
            value =self.databasemanager.guidelinesdatabase.get_one_guideline(i+1)
            if self.criteria_3=="All":
                pass
            elif self.criteria_3=="Superficial":
                if value["assembly_position"]!="Superficial" and value["assembly_position"]!="All":
                    self.table_view.hideRow(i)
            elif self.criteria_3=="Deep":
                if value["assembly_position"]!="Deep" and value["assembly_position"]!="All":
                    self.table_view.hideRow(i)
    
    def update_guidelines_cb4(self):
        self.criteria_4 = self.cb4.currentData()
        for i in range(self.table_model.rowCount(self)):
            value =self.databasemanager.guidelinesdatabase.get_one_guideline(i+1)
            if self.criteria_4=="All":
                pass
            elif self.criteria_4 =="Polymer":
                if value["part_type"]!="Polymer" and value["part_type"]!="P&M" and value["part_type"]!="All":
                    self.table_view.hideRow(i)
            elif self.criteria_4=="Metal":
                if value["part_type"]!="Metal" and value["part_type"]!="P&M" and value["part_type"]!="All":
                    self.table_view.hideRow(i)
            elif self.criteria_4=="Electric":
                if value["part_type"]!="Electr." and value["part_type"]!="All":
                    self.table_view.hideRow(i)

    def update_table(self):
        self.table_model= TableModel(self,self.data_list,[""])
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.update_guidelines_cb1()
        self.update_guidelines_cb2()
        self.update_guidelines_cb3()
        self.update_guidelines_cb4()
        self.font=QFont("Courrier New", 10)
        self.table_view.setFont(self.font)
        self.table_view.resizeColumnsToContents()
        self.widget_table_view = QWidget(self)
        self.layout_table_view = QVBoxLayout(self)
        self.layout_table_view.addWidget(self.table_view)
        self.widget_table_view.setLayout(self.layout_table_view)
        self.widget_table_view.setGeometry(10, 150, 800, 500)
        self.widget_table_view.show()