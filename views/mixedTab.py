from logging import setLogRecordFactory
from PySide2 import QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QToolBar,
    QStyle, QVBoxLayout, QTabWidget, QFrame, QLabel, QGridLayout, QComboBox,
    QWidget, QTableView, QWidget
)
from PySide2.QtGui import QFont 
from PySide2.QtCore import Qt

from ..databases.pdfInfoFormatter import PdfInfoFormatter
from .icon import Icon
from .style import Style
from .form import Form
from ..models.datamodel import Datamodel
from ..models.tablemodel import TableModel
from ..controllers.signals import signals
from ..databases.database import DatabaseManager

databasemanager = DatabaseManager()


class MixedTab(QTabWidget):
    def __init__(self,parent=None):
        super(MixedTab, self).__init__(parent)
        self.icon = Icon()
        self.form = Form()
        self.style = Style()

        # Title
        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> MIXED </h1>')
        self.title.move(10,50)

        self.all_products = databasemanager.productdatabase.get_all_product()
        self.edit_component_product = QComboBox(self)
        self.edit_component_product.addItem("Select a product", userData = None)
        for _, value in self.all_products.items():
            self.edit_component_product.addItem(str(value["name_product"]), userData = value)
        self.edit_component_product.move(250, 100)
        self.edit_component_product.setFrame(False)
        self.edit_component_product.currentIndexChanged.connect(
            self.call_show_table_mixed_product
        )

        self.datamodel = Datamodel()
        self.data_list = self.datamodel.getdata_product()
        self.header = self.datamodel.header_database_product
        self.table_model = TableModel(self, self.data_list, self.header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.font = QFont("Courrier New", 10)
        self.table_view.setFont(self.font)
        self.table_view.resizeColumnsToContents()
        self.widget_tableview = QWidget(self)
        self.layout_tableview = QVBoxLayout(self)
        self.layout_tableview.addWidget(self.table_view)
        self.widget_tableview.setLayout(self.layout_tableview)
        self.widget_tableview.setGeometry(10, 170, 800, 500)
        self.widget_tableview.show()
        self.title_product = QLabel(self)
        self.title_product.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title_product.setText("")
        self.title_product.setGeometry(10,140,800,30)

    def open_tab(self,parent):
        parent.tabwidget.setCurrentIndex(7)

    def call_show_table_mixed_product(self):
        selected_product = self.edit_component_product.currentData()
        self.title_product.setText('<h1 style=""> '+ selected_product["name_product"]+" </h1>")
        self.datamodel = Datamodel()
        self.data_list = self.datamodel.get_mixed_data(selected_product["id_product"])
        self.header = self.datamodel.header_mixed
        self.table_model = TableModel(self, self.data_list, self.header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.font = QFont("Courrier New", 10)
        self.table_view.setFont(self.font)
        self.table_view.resizeColumnsToContents()
        self.widget_tableview = QWidget(self)
        self.layout_tableview = QVBoxLayout(self)
        self.layout_tableview.addWidget(self.table_view)
        self.widget_tableview.setLayout(self.layout_tableview)
        self.widget_tableview.setGeometry(10, 170, 800, 500)
        self.widget_tableview.show()
        

    

