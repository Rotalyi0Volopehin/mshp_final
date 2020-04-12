import os
import exceptions

from net_connection.core_classes import CoreClasses


CoreClasses.reg_core_classes(os.path.dirname(exceptions.__file__))
