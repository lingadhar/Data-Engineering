import pandas as pd
import string
import random
import sqlite3

class data_ingest:
    def __init__(self, file,tgt):
        self._file = file
        self._target = tgt

    #Load the csv file
    def excel_loader(self):
        data = pd.read_csv(self._file)
        return data

    #Customer ID and Product ID generation
    def id_generator(self, size=6, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def cust_prod_id_gen(self):
        data = self.excel_loader()
        custdict = dict()
        for i in list(set(data['ClientName'].tolist())):
            custdict[i] = "CL" + self.id_generator(6)

        proddict = dict()
        for i in list(set(data['ProductName'].tolist())):
            proddict[i] = "PR" + self.id_generator(6)

        data['Cust_id'] = ''
        data['Product_id'] = ''
        for ind, row in data.iterrows():
            data.loc[ind, ['Cust_id']] = custdict[row['ClientName']]
            data.loc[ind, ['Product_id']] = proddict[row['ProductName']]
        return data

    # Creation of dataframes from the csv data file
    def data_ingest(self):
        data = self.cust_prod_id_gen()
        data_product = data[['Product_id','ProductName','ProductType','UnitPrice']]
        data_Invoice = data[['PaymentBillingCode','PaymentDate','PaymentType','Currency']]
        data_customer = data[['Cust_id','ClientName','DeliveryAddress','DeliveryCity','DeliveryPostcode','DeliveryCountry','DeliveryContactNumber']]
        data_PO = data[['OrderNumber','Cust_id','Product_id','PaymentBillingCode','ProductQuantity','TotalPrice']]

        # Dropping duplicates from the required dataframes
        data_customer = data_customer.drop_duplicates()
        data_Invoice = data_Invoice.drop_duplicates()
        data_product = data_product.drop_duplicates()

        # Copy the dataframes to SQLite tables
        try:
            conn = sqlite3.connect(self._target)
            data_product.to_sql('Product', conn, if_exists='append', index=False)
            data_Invoice.to_sql('Invoice', conn, if_exists='append', index=False)
            data_customer.to_sql('Customer', conn, if_exists='append', index=False)
            data_PO.to_sql('Purchase_Order', conn, if_exists='append', index=False)
        except Exception as e:
            raise (str(e))