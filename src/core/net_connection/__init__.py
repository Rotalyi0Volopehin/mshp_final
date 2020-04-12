import sys
import os

from net_connection.core_classes import CoreClasses


CoreClasses.reg_core_classes(os.path.dirname(sys.modules[__name__].__file__))
