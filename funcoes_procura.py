import time
from datetime import datetime
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#Para ter a procura sem abrir o browser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pypika import Table, Query
import mysql.connector
from mysql.connector import errorcode 

def procura_por_value(site_url, driver, value_html):
    driver.get(site_url)
    price_element = driver.find_element(By.CLASS_NAME, value_html)
    price_text = price_element.text.strip()
    price_text = price_text.replace('€', '')
    price = float(price_text.replace(',', '.'))
    print(price)
    return price

