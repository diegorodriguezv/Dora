import os
import sys

scriptpath = os.path.dirname(__file__)
dorapath = os.path.abspath(os.path.join(scriptpath, os.path.pardir))
sys.path.insert(0, dorapath)

import dora
