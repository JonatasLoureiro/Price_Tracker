import time
from datetime import datetime
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pypika import Table, Query
import mysql.connector
from mysql.connector import errorcode 
import funcoes_procura


def inicia_browser():
    s = Service(r'D:\chromedriver-win64\chromedriver.exe')
    chromeOptions = Options()

    # Inicializar o Chrome
    driver = webdriver.Chrome(service=s, options=chromeOptions)

    try:
        url = 'https://www.worten.pt/produtos/caixa-pc-nzxt-nzxt-cm-h71ew-02-computer-case-midi-tower-white-mrkean-5056547203522'
        # Encontra o preço
        price = funcoes_procura.procura_por_value(url,driver,'value')
        return price

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        price = None
        return price
    finally:
        driver.quit()


def insert_data(cnx, table_name, price):
    table = Table(table_name)
    q = Query.into(table_name).columns('price','date').insert(price, datetime.now().date())

    try:
        cursor = cnx.cursor()
        cursor.execute(str(q).replace('"', '`'))
        cnx.commit()
        print("Data inserted successfully!")
    
    except Exception as e:
        print(f"An error occurred during data insertion: {str(e)}")



def main():
    try:
        database_connection = mysql.connector.connect(user='root',password='6295',database='prices_log') 

    except mysql.connector.Error as err: #Verifys if an error ocurred during connection
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something went wrong with user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    
    else:
        print("Connection was successful")
        #Gets price from the function
    try:
        price = inicia_browser()
        print("price: " + str(price))

        if price is not None:
            insert_data(database_connection, 'worten', price)
            print("Entrou na insersao de dados na DB")

    finally:
        database_connection.close()
        print("Connection closed!")
    



if __name__ == '__main__':
    main()
    print("Done")

