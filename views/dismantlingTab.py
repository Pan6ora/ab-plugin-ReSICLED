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

class DismantlingTab(QTabWidget):
    def __init__(self, parent = None):
        super(DismantlingTab, self).__init__(parent)
        self.icon = Icon()
        self.form = Form()
        style = Style()

        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> DISMANTLING </h1>')
        self.title.move(10, 50)

        self.all_products = databasemanager.productdatabase.get_all_product()
        self.edit_component_product = QComboBox(self)
        self.edit_component_product.addItem("Select a product", userData=None)
        for _, value_product in self.all_products.items():
            self.edit_component_product.addItem(str(value_product["name_product"]), 
            userData=value_product)
        self.edit_component_product.move(250, 100)
        self.edit_component_product.setFrame(False)
        self.edit_component_product.currentIndexChanged.connect(
            self.call_show_table_dismantling_product)


        self.datamodel = Datamodel()
        self.data_list = self.datamodel.getdata_product()
        self.header = self.datamodel.header_database_product
        self.table_model = TableModel(self, self.data_list, self.header)
        self.tableview = QTableView()
        self.tableview.setModel(self.table_model)
        self.font = QFont("Courrier New", 10)
        self.tableview.setFont(self.font)
        self.tableview.resizeColumnsToContents()
        self.widget_tableview = QWidget(self)
        self.layout_tableview = QVBoxLayout(self)
        self.layout_tableview.addWidget(self.tableview)
        self.widget_tableview.setLayout(self.layout_tableview)
        self.widget_tableview.setGeometry(10, 170, 800, 500)
        self.widget_tableview.show()
        self.title_product = QLabel(self)
        self.title_product.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title_product.setText("")
        self.title_product.setGeometry(10, 140, 800, 30)

    def open_tab(self, parent):
        parent.tabwidget.setCurrentIndex(5)

    def call_show_table_dismantling_product(self, index):
        selected_product = self.edit_component_product.currentData()
        self.title_product.setText('<h1 style=""> ' + selected_product["name_product"]+' dismantling values </h1>')
        self.datamodel = Datamodel()
        self.data_list = self.datamodel.getDismantling_data(selected_product["id_product"])
        self.header = self.datamodel.header_dismantling
        self.tablemodel = TableModel(self, self.data_list, self.header)
        self.tableview = QTableView()
        self.tableview.setModel(self.tablemodel)
        self.font = QFont("Courier New", 10)
        self.tableview.setFont(self.font)
        self.tableview.resizeColumnsToContents()
        # enable sorting
        #display
        self.widget_table_view = QWidget(self)
        self.layout_table_view = QVBoxLayout(self)
        self.layout_table_view.addWidget(self.tableview)
        self.widget_table_view.setLayout(self.layout_table_view)
        self.widget_table_view.setGeometry(10, 170, 800, 500)
        self.widget_table_view.show()