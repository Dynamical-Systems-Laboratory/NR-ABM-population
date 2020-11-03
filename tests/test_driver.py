import subprocess

import sys
py_path = '../tools/'
sys.path.insert(0, py_path)

import utils as ut
from colors import *

ut.msg('Workplace loading test', CYAN)
subprocess.call(['python3.6 workplaces_test.py'], shell=True)

ut.msg('School loading test', CYAN)
subprocess.call(['python3.6 schools_test.py'], shell=True)

ut.msg('Hospital loading test', CYAN)
subprocess.call(['python3.6 hospitals_test.py'], shell=True)

ut.msg('Household loading test', CYAN)
subprocess.call(['python3.6 households_test.py'], shell=True)

ut.msg('Agent generation test', CYAN)
subprocess.call(['python3.6 agents_test.py'], shell=True)
