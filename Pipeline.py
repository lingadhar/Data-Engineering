import SQLite_Table_Creation as tab
import DataIngest as di
from paths import *
import os

#Fetch the file name
filename = [f for f in os.listdir(SRC_FOLDER) if '.csv' in f][0]
#Create the db
a = tab.main()
#Ingest the data
b = di.data_ingest(os.path.join(SRC_FOLDER, filename),TGT_FOLDER + "\\"+"abcdb.db")
b.data_ingest()






