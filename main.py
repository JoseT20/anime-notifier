import email_alert
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
import time

print(f'Would you like to get updates on free or premium episodes?')
episode_type = input('>')

url_free = 'https://www.crunchyroll.com/simulcastcalendar?filter=free'
url_premium = 'https://www.crunchyroll.com/simulcastcalendar?filter=premium'
driver = webdriver.Chrome('./chromedriver')


def new_episodes_alert():
    if episode_type == 'Free':
        driver.get(url_free)
    else:
        driver.get(url_premium)

    source_data = driver.page_source
    soup = BeautifulSoup(source_data, 'lxml')
    date_today = date.today().strftime("%b-%d-%Y")
    today_data = soup.find('li', class_='day active today')
    new_episodes = today_data.find_all('li')
    file_path = f'Anime Releases/{episode_type}-{date_today}.txt'

    for new_episode in new_episodes:
        season_name = new_episode.find('h1', class_='season-name').text.strip()
        episode = new_episode.find('div', class_='episode-label').text.strip()
        release_date = today_data.find('div', class_='specific-date').text.strip()
        release_time = new_episode.find('time', class_='available-time').text.strip()
        link = new_episode.find('div', class_='availability').a['href']

        with open(f'{file_path}', 'a+') as f:
            f.write(f'Anime: {season_name} \n')
            f.write(f'Episode: {episode} \n')
            f.write(f'Release Date: {release_date} at {release_time} \n')
            f.write(f'Link: {link} \n\n')

    with open(f'{file_path}', 'rb') as f:
        file_data = f.read()
        file_name = f.name

    email_alert.email_alert(f'{date_today} Crunchyroll {episode_type} Releases', 'Txt file attached...', 'abraham990522@gmail.com', file_data, file_name)


if __name__ == '__main__':
    while True:
        new_episodes_alert()
        print(f'Check your email for episode updates! \n')
        time_wait = 24
        time.sleep(time_wait * 3600)