#
# Execute this script to copy the cxxtest/*.py files
# and run 2to3 to convert them to Python 3.
#

import glob
import subprocess
import os
import shutil

os.chdir('cxxtest')
for file in glob.glob('*.py'):
    shutil.copyfile(file, '../python3/cxxtest/'+file)
#
os.chdir('../python3/cxxtest')
#
for file in glob.glob('*.py'):
    subprocess.call('2to3 -w '+file, shell=True)

