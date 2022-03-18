from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
import requests
import time

url = 'https://www.crunchyroll.com/es-es/simulcastcalendar'
driver = webdriver.Chrome('./chromedriver')
driver.get(url)
source_data = driver.page_source
soup = BeautifulSoup(source_data, 'lxml')
new_episodes = soup.find('li', class_='day today active')
print(new_episodes)

