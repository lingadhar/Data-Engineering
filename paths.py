import os
cur=os.getcwd()
SRC_FOLDER = cur
if not os.path.exists('db'):
    os.makedirs('db')
TGT_FOLDER = cur+'\\'+'db'
