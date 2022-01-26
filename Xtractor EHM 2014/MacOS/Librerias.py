# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 03:52:59 2021

@author: VAIO
"""

import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Openpyxl==3.0.3'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'TK-tools==0.12.0'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyMuPDF==1.17.3'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-python==4.3.0.36'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pytesseract==0.3.4'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow==7.2.0'])
