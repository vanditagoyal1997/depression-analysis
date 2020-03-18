# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 17:44:10 2020

@author: vandi
"""
import os
from os import path
import shutil

src = "C:\\Users\\vandi\\Documents\\daicwoz_dataset\\"
dst = "C:\\Users\\vandi\\Documents\\daicwoz_dataset\\action_units\\"

for i in range(426,441):
    folder_name=str(i)+"_P\\"
    src_path=src+folder_name
    file=str(i)+"_CLNF_AUs.txt"
    shutil.copy(path.join(src_path, file), dst)