import sys
import os

from net_connection.core_classes import CoreClasses


# исполнять при старте программы
def init_core():
    CoreClasses.reg_core_classes(os.path.dirname(sys.modules[__name__].__file__))
