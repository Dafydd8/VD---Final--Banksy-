from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import csv

chromedriverpath = './chromedriver'
try:
	driver = webdriver.Chrome()
except:
	driver = webdriver.Chrome(chromedriverpath)
	
driver.get("https://banksy-value.com/")

rows = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "clickablerow")))

f = open('banksy_prints_prices.csv', 'w', encoding='utf-8')
f.write('Print name,Edition,Last auctioned,Last avg price,Print value (auto),Print value (expert range)\n')

for row in rows:
    # Obtener todas las etiquetas <td> dentro de la fila actual
	td_elements = row.find_elements(By.TAG_NAME, 'td')
    
    # Extraer el texto de cada <td> y almacenarlo en una lista
	td_textos = []
	for td in td_elements:
		td_textos.append((td.text).replace("⇘\n",""))
    
    # Imprimir el texto de cada <td> para la fila actual
	f.write(",".join(td_textos) + '\n')
		

driver.close()