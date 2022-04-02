#SQLite table creation

import sqlite3
from sqlite3 import Error
from paths import *


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = TGT_FOLDER + "\\"+"abcdb.db"
    
    # create a database connection
    conn = create_connection(database)

    # create tables
    sql_create_Invoice = """CREATE TABLE IF NOT EXISTS Invoice (
                                    PaymentBillingCode varchar(50) PRIMARY KEY,
                                    PaymentDate date NOT NULL,
                                    PaymentType text NOT NULL,
                                    Currency char(5) NOT NULL
                                );"""
    
    sql_create_Product = """CREATE TABLE IF NOT EXISTS Product (
                                    Product_id varchar(50) PRIMARY KEY,
                                    UnitPrice integer NOT NULL,
                                    ProductName text,
                                    ProductType text
                                );"""
    
    sql_create_Customer = """CREATE TABLE IF NOT EXISTS Customer (
                                    Cust_id varchar(50) PRIMARY KEY,
                                    ClientName text,
                                    DeliveryAddress text,
                                    DeliveryCity text,
                                    DeliveryPostcode text,
                                    DeliveryCountry text,
                                    DeliveryContactNumber text
                                );"""
    
    sql_create_Purchase_Order = """CREATE TABLE IF NOT EXISTS Purchase_Order (
                                    OrderNumber varchar(50) PRIMARY KEY,
                                    Cust_id varchar(50),
                                    Product_id varchar(50),
                                    PaymentBillingCode varchar(50),
                                    ProductQuantity int,
                                    TotalPrice int,
                                    FOREIGN KEY (Cust_id) REFERENCES Customer (Cust_id),
                                    FOREIGN KEY (Product_id) REFERENCES Product (Product_id),
                                    FOREIGN KEY (PaymentBillingCode) REFERENCES Invoice (PaymentBillingCode),
                                    FOREIGN KEY (OrderNumber) REFERENCES Purchase_Order (OrderNumber)
                                );"""

    if conn is not None:
        # create Invoice table
        create_table(conn, sql_create_Invoice)
        
        # create Product table
        create_table(conn, sql_create_Product)
        
        # create Customer table
        create_table(conn, sql_create_Customer)

        # create Purchase_Order table
        create_table(conn, sql_create_Purchase_Order)

        
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()