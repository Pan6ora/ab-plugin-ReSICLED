from PySide2.QtWidgets import (
    QVBoxLayout, QTabWidget, QFrame, QLabel, QComboBox,
    QWidget, QTableView, QWidget
)
from PySide2.QtGui import QFont 
from .icon import Icon
from .form import Form
from .style import Style
from ..models.tablemodel import TableModel
from ..models.datamodel import Datamodel
from ..databases.database import DatabaseManager

databasemanager = DatabaseManager()

class HotspotsTab(QTabWidget):
    def __init__(self,parent = None):
        super(HotspotsTab,self).__init__(parent)
        self.icon = Icon()
        self.form = Form()
        self.style = Style()

        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> HOTSPOTS </h1>')
        self.title.move(10, 50)

        self.all_products = databasemanager.productdatabase.get_all_product()
        self.edit_component_product = QComboBox(self)
        self.edit_component_product.addItem("Select a product", userData=None)
        for _, value in self.all_products.items():
            self.edit_component_product.addItem(str(value["name_product"]), userData = value)
        self.edit_component_product.move(250, 100)
        self.edit_component_product.setFrame(False)
        self.edit_component_product.currentIndexChanged.connect(
            self.call_show_hotspots_product
        )

        self.datamodel = Datamodel()
        self.data_list1 = self.datamodel.getdata_product()
        self.header1 = self.datamodel.header_database_product
        self.table_model1 = TableModel(self,self.data_list1,self.header1)
        self.tableview1 = QTableView()
        self.tableview1.setModel(self.table_model1)
        self.font = QFont("Courrier New", 10)
        self.tableview1.setFont(self.font)
        self.tableview1.resizeColumnsToContents()
        self.tableview_widget1 = QWidget(self)
        self.tableview_layout1 = QVBoxLayout(self)
        self.tableview_layout1.addWidget(self.tableview1)
        self.tableview_widget1.setLayout(self.tableview_layout1)
        self.tableview_widget1.setGeometry(10,170,500,500)
        self.tableview_widget1.show()
        self.title_product=QLabel(self)
        self.title_product.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title_product.setText("")
        self.title_product.setGeometry(10,140,800,30)

        self.data_list2 = self.datamodel.getdata_product()
        self.header2 = self.datamodel.header_database_product
        self.table_model2 = TableModel(self,self.data_list2,self.header2)
        self.tableview2 = QTableView()
        self.tableview2.setModel(self.table_model2)
        self.font = QFont("Courrier New", 10)
        self.tableview2.setFont(self.font)
        self.tableview2.resizeColumnsToContents()
        self.tableview_widget2 = QWidget(self)
        self.tableview_layout2 = QVBoxLayout(self)
        self.tableview_layout2.addWidget(self.tableview2)
        self.tableview_widget2.setLayout(self.tableview_layout2)
        self.tableview_widget2.setGeometry(510,170,500,500)
        self.tableview_widget2.show()

    def open_tab(self, parent):
        parent.tabwidget.setCurrentIndex(8)

    def call_show_hotspots_product(self):
        selected_product = self.edit_component_product.currentData()
        self.title_product.setText('<h1 style=""> ' + selected_product["name_product"] + ' hotspots tables </h1>')
        self.datamodel = Datamodel()
        self.data_list1 = self.datamodel.get_hotspot1_data(selected_product["id_product"])
        self.header1 = self.datamodel.header_hotspots_1
        self.table_model1 = TableModel(self,self.data_list1,self.header1)
        self.tableview1 = QTableView()
        self.tableview1.setModel(self.table_model1)
        self.font = QFont("Courrier New", 10)
        self.tableview1.setFont(self.font)
        self.tableview1.resizeColumnsToContents()
        self.widget_table_view_1 = QWidget(self)
        self.layout_table_view_1 = QVBoxLayout(self)
        self.layout_table_view_1.addWidget(self.tableview1)
        self.widget_table_view_1.setLayout(self.layout_table_view_1)
        self.widget_table_view_1.setGeometry(10,170,500,500)
        self.widget_table_view_1.show()

        self.datamodel = Datamodel()
        self.data_list2 = self.datamodel.get_hotspot2_data(selected_product["id_product"])
        self.header2 = self.datamodel.header_hotspots_2
        self.table_model2 = TableModel(self,self.data_list2,self.header2)
        self.tableview2 = QTableView()
        self.tableview2.setModel(self.table_model2)
        self.font = QFont("Courrier New", 10)
        self.tableview2.setFont(self.font)
        self.tableview2.resizeColumnsToContents()
        self.widget_table_view_2 = QWidget(self)
        self.layout_table_view_2 = QVBoxLayout(self)
        self.layout_table_view_2.addWidget(self.tableview2)
        self.widget_table_view_2.setLayout(self.layout_table_view_2)
        self.widget_table_view_2.setGeometry(510,170,500,500)
        self.widget_table_view_2.show()


    
