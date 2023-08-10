import os
from os import path
import sys

proj_dir = path.abspath(path.join(path.dirname(__file__), os.pardir))
if sys.platform == 'win32' and os.getlogin().lower() == 'hassanah':
    data_dir = r'C:\Users\hassanah'
elif sys.platform == 'linux' and os.getlogin().lower() == 'hassanah':
    data_dir = '/home/hassanah/'
else:
    data_dir = path.join(proj_dir, 'data')
data_processed_dir = path.join(proj_dir, 'data-processed')
plot_dir = path.join(proj_dir, 'plots')
utils_dir = path.join(proj_dir, 'utils')
sys.path.append(proj_dir)
