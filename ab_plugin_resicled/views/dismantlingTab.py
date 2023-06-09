from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QHBoxLayout, QPushButton, QVBoxLayout, QTabWidget,
    QFrame, QLabel, QGridLayout, QComboBox,
    QWidget, QTableView, QWidget
)
from PySide2.QtGui import QFont
from .icon import Icon
from .form import Form
from .style import Style
from ..signals import signals
from ..models.tablemodel import TableModel
from ..models.datamodel import Datamodel
from ..databases.database import databasemanager



class DismantlingTab(QTabWidget):
    """
    The class that runs the Dismantling tab in the plugin (and its dependencies)
    """
    def __init__(self, parent=None):
        """
        Initializing the tab and building the main widgets 
        """
        super(DismantlingTab, self).__init__(parent)
        self.databasemanager = databasemanager
        self.icon = Icon()
        self.form = Form()
        self.style = Style()
        # Title
        self.title = QLabel(self)
        self.title.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title.setText('<h1 style=""> DISMANTLING </h1>')
        self.title.move(10, 50)
        # Product selection combobox's label
        self.title = QLabel(self)
        self.title.setText('Select a product to view its dismantling rates')
        # Product Selection Combobox
        self.all_product = self.databasemanager.productdatabase.get_all_product()
        self.edit_component_product = QComboBox(self)
        self.edit_component_product.addItem("Select a product", userData=None)
        for _, value_product in self.all_product.items():
            self.edit_component_product.addItem(str(value_product['name_product']), userData=value_product)
        # Creating the product selection layout
        self.edit_component_product.setFrame(False)
        self.component_edit_widget = QWidget(self)
        self.component_edit_layout = QHBoxLayout(self)
        self.component_edit_layout.addWidget(self.title)
        self.component_edit_layout.addWidget(self.edit_component_product)
        self.component_edit_widget.setLayout(self.component_edit_layout)
        self.component_edit_widget.move(10,100)
        # Full product and directive rates table
        self.title_recycling_rate = QLabel("Recycling rate")
        self.title_recovery_rate = QLabel("Recovery rate")
        self.title_residual_waste_rate = QLabel("Residual waste rate")
        self.title_product = QLabel("Product")
        self.title_directive = QLabel("Directive")
        self.title_directive_applied = QLabel("Directive applied")
        self.value_recycling_rate_product = QLabel(self)
        self.value_recovery_rate_product = QLabel(self)
        self.value_residual_waste_rate_product = QLabel(self)
        self.value_recycling_rate_directive = QLabel(self)
        self.value_recovery_rate_directive = QLabel(self)
        self.value_residual_waste_rate_directive = QLabel(self)
        self.value_recycling_rate_status = QLabel(self) #GOOD or BAD
        self.value_recovery_rate_status = QLabel(self) #GOOD or BAD
        self.value_residual_waste_rate_status = QLabel(self) #GOOD or BAD
        self.value_directive_applied = QLabel("None")
        self.value_directive_applied.wordWrap()
        # Rates table style
        self.title_recycling_rate.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.title_recovery_rate.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.title_residual_waste_rate.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.title_product.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.title_directive.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.title_directive_applied.setStyleSheet(self.style.style_table_rate_border_bottom + self.style.style_min_width_100)
        self.value_recycling_rate_product.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_recovery_rate_product.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_residual_waste_rate_product.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_recycling_rate_directive.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_recovery_rate_directive.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_residual_waste_rate_directive.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_recycling_rate_status.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_recovery_rate_status.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_residual_waste_rate_status.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_directive_applied.setStyleSheet(self.style.style_table_rate_border_bottom)
        # Directive selection PushButton
        self.button_directive = QPushButton(self.icon.add, "Apply directive", self)
        self.button_directive.clicked.connect(self.call_show_dialog_insert_directive)
        # Displaying the Rate's table
        self.widget_rate_view = QWidget(self)
        self.layout_rate = QGridLayout()
        self.layout_rate.addWidget(self.title_product, 0, 1)
        self.layout_rate.addWidget(self.title_directive, 0, 2)
        self.layout_rate.addWidget(self.button_directive, 0, 3)
        self.layout_rate.addWidget(self.title_directive_applied, 0, 4)
        self.layout_rate.addWidget(self.title_recycling_rate, 1, 0)
        self.layout_rate.addWidget(self.value_recycling_rate_product, 1, 1)
        self.layout_rate.addWidget(self.value_recycling_rate_directive, 1, 2)
        self.layout_rate.addWidget(self.value_recycling_rate_status, 1, 3)
        self.layout_rate.addWidget(self.value_directive_applied, 1, 4, 3, 1)
        self.layout_rate.addWidget(self.title_recovery_rate, 2, 0)
        self.layout_rate.addWidget(self.value_recovery_rate_product, 2, 1)
        self.layout_rate.addWidget(self.value_recovery_rate_directive, 2, 2)
        self.layout_rate.addWidget(self.value_recovery_rate_status, 2, 3)
        self.layout_rate.addWidget(self.title_residual_waste_rate, 3, 0)
        self.layout_rate.addWidget(self.value_residual_waste_rate_product, 3, 1)
        self.layout_rate.addWidget(self.value_residual_waste_rate_directive, 3, 2)
        self.layout_rate.addWidget(self.value_residual_waste_rate_status, 3, 3)
        self.widget_rate_view.setLayout(self.layout_rate)
        self.widget_rate_view.move(10, 180)
        self.widget_rate_view.setStyleSheet(self.style.style_table_rate)
        self.widget_rate_view.show()
        # Selected product's table title
        self.title_component_product = QLabel(self)
        self.title_component_product.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.title_component_product.setText('')
        self.title_component_product.setGeometry(10, 140, 1000, 30)
        self.edit_component_product.currentIndexChanged.connect(self.call_show_table_component_product)
        #signal update_combobox
        signals.update_combobox.connect(self.update_menu_combobox)
        
    @Slot(object)
    def update_menu_combobox(self):
        """
        Updates the product selection combobox
        """
        box = self.edit_component_product
        #---product to select
        self.all_product_form = self.databasemanager.productdatabase.get_all_product()
        try:
            box.clear()
            box.addItem("Select a product")
            for key, value in self.all_product_form.items():
                box.addItem(str(value['name_product']), userData=value)
        except: 
            pass
        
    def call_show_dialog_insert_directive(self):
        """
        Displays the Dismantling choice wizard
        """
        self.form.show_dialog_insert_directive(self, "dismantling")
        
    def call_show_table_component_product(self,index):
        """
        Displays the dismantling scenario table in the tab
        """
        if(index==0):
            self.title_component_product.setText("")
            self.value_recycling_rate_status.setText("")
            self.value_recovery_rate_status.setText("")
            self.value_residual_waste_rate_status.setText("")
            self.value_recycling_rate_product.setText("")
            self.value_recovery_rate_product.setText("")
            self.value_residual_waste_rate_product.setText("")
            self.value_recycling_rate_directive.setText("")
            self.value_recovery_rate_directive.setText("")
            self.value_residual_waste_rate_directive.setText("")
            self.value_directive_applied.setText("None")
        product_selected = self.edit_component_product.currentData()
        if (product_selected == None):
            return None
        self.title_component_product.setText('<h1 style=""> '+product_selected['name_product']+' (components list)  </h1>' )
        self.datamodel = Datamodel()
        self.data_list = self.datamodel.getdata_component_scenario_rate(product_selected['id_product'],"dismantling")
        self.header = self.datamodel.header_database_component_scenario_rate
        self.value_recycling_rate_product.setText(str(self.datamodel.recycling_rate) + "%")
        self.value_recovery_rate_product.setText(str(self.datamodel.recovery_rate) + "%")
        self.value_residual_waste_rate_product.setText(str(self.datamodel.residual_rate) + "%")  
        self.table_model = TableModel(self, self.data_list, self.header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        # set font
        self.font = QFont("Courier New", 10)
        self.table_view.setFont(self.font)
        # set column width to fit contents (set font first!)
        self.table_view.hideColumn(1)
        self.table_view.resizeColumnsToContents()
        #display
        self.widget_table_view = QWidget(self)
        self.layout_table_view = QVBoxLayout(self)
        self.layout_table_view.addWidget(self.table_view)
        self.widget_table_view.setLayout(self.layout_table_view)
        self.widget_table_view.setGeometry(10, 320, 1200, 500)
        self.widget_table_view.show()
        #update rate
        self.value_recycling_rate_status.setText("")
        self.value_recycling_rate_status.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_recovery_rate_status.setText("")
        self.value_recovery_rate_status.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.value_residual_waste_rate_status.setText("")
        self.value_residual_waste_rate_status.setStyleSheet(self.style.style_table_rate_border_bottom)
        self.text_good = "GOOD"
        self.text_bad = "BAD"
        if self.value_recycling_rate_product.text() != "":
            self.int_value_recycling_rate_product = int(self.value_recycling_rate_product.text().replace("%", ""))
        else:
            self.int_value_recycling_rate_product = 0
        if self.value_recovery_rate_product.text() != "":
            self.int_value_recovery_rate_product = int(self.value_recovery_rate_product.text().replace("%", ""))
        else:
            self.int_value_recovery_rate_product = 0
        if self.value_residual_waste_rate_product.text() != "":
            self.int_value_residual_waste_rate_product = int(self.value_residual_waste_rate_product.text().replace("%", ""))
        else:
            self.int_value_residual_waste_rate_product = 0
        if self.value_recycling_rate_directive.text() != "":
            self.int_value_recycling_rate_directive = int(self.value_recycling_rate_directive.text().replace("%", ""))
        else:
            self.int_value_recycling_rate_directive = 0
        if self.value_recovery_rate_directive.text() != "":
            self.int_value_recovery_rate_directive = int(self.value_recovery_rate_directive.text().replace("%", ""))
        else:
            self.int_value_recovery_rate_directive = 0
        if self.value_residual_waste_rate_directive.text() != "":
            self.int_value_residual_waste_rate_directive = int(self.value_residual_waste_rate_directive.text().replace("%", ""))
        else:
            self.int_value_residual_waste_rate_directive = 0
        if(self.int_value_recycling_rate_directive > 0 or self.int_value_recovery_rate_directive > 0 or self.int_value_residual_waste_rate_directive > 0):
            if(self.int_value_recycling_rate_product >= self.int_value_recycling_rate_directive):
                self.value_recycling_rate_status.setText(self.text_good)
                self.value_recycling_rate_status.setStyleSheet(self.style.style_good_rate + self.style.style_table_rate_border_bottom)
            else:
                self.value_recycling_rate_status.setText(self.text_bad)
                self.value_recycling_rate_status.setStyleSheet(self.style.style_bad_rate + self.style.style_table_rate_border_bottom)
            if(self.int_value_recovery_rate_product >= self.int_value_recovery_rate_directive):
                self.value_recovery_rate_status.setText(self.text_good)
                self.value_recovery_rate_status.setStyleSheet(self.style.style_good_rate + self.style.style_table_rate_border_bottom)
            else:
                self.value_recovery_rate_status.setText(self.text_bad)
                self.value_recovery_rate_status.setStyleSheet(self.style.style_bad_rate + self.style.style_table_rate_border_bottom)
            if(self.int_value_residual_waste_rate_product <= self.int_value_residual_waste_rate_directive):
                self.value_residual_waste_rate_status.setText(self.text_good)
                self.value_residual_waste_rate_status.setStyleSheet(self.style.style_good_rate + self.style.style_table_rate_border_bottom)
            else:
                self.value_residual_waste_rate_status.setText(self.text_bad)
                self.value_residual_waste_rate_status.setStyleSheet(self.style.style_bad_rate + self.style.style_table_rate_border_bottom)