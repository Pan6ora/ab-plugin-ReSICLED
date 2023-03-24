from PySide2.QtCore import QObject, Signal

from activity_browser.signals import Signals as ABSignals 


class Signals(ABSignals):
    def __init__(self, parent=None):
        ABSignals.__init__(self, parent)

    add_product = Signal(str)
    alert_information = Signal(str)
    update_combobox = Signal()
    update_table_component_product = Signal(object, object)
    update_component_scenario = Signal(object)
        
    
signals = Signals()
