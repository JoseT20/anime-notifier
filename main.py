from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
import time

url = 'https://www.crunchyroll.com/es-es/simulcastcalendar'
driver = webdriver.Chrome('./chromedriver')
driver.get(url)
source_data = driver.page_source
soup = BeautifulSoup(source_data, 'lxml')
today_data = soup.find('li', class_='day active today')
new_episodes = today_data.find_all('li')

for new_episode in new_episodes:
    season_name = new_episode.find('h1', class_='season-name').text.strip()
    episode = new_episode.find('div', class_='episode-label').text.strip()
    release_date = today_data.find('div', class_='specific-date').text.strip()
    release_time = new_episode.find('time', class_='available-time').text.strip()
    link = new_episode.find('div', class_='availability').a['href']

    print(f'Anime: {season_name}')
    print(f'Episode: {episode}')
    print(f'Release Date: {release_date} at {release_time}')
    print(f'Link: {link} \n')


