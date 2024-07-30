#!/bin/python3

# Fonte: https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br"
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "/Users/gabriel.dantas/git/gdantas/machine-learning-studybook/tech-challenge-02/batch-pipeline-b3/Extract"}

chrome_options.add_experimental_option("prefs",prefs)

chrome_options.binary_location = r'./chromedriver'

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
driver.maximize_window()

print("Getting data from:", url)
driver.find_element(By.XPATH, '//a[text()="Download"]').click()

time.sleep(3)

print("Done!")

driver.quit()
