import email_alert
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date

print(f'Would you like to get updates on free or premium episodes?')
episode_type = input('>').upper()
print(f'Enter your email:')
email = input('>')

url_free = 'https://www.crunchyroll.com/simulcastcalendar?filter=free'
url_premium = 'https://www.crunchyroll.com/simulcastcalendar?filter=premium'


def new_episodes_alert():
    date_today = date.today().strftime("%b-%d-%Y")
    dir_name = 'Anime Releases'

    if not os.path.exists(dir_name):
        os.mkdir('Anime Releases')
        print(f'Directory "{dir_name}" Created.\n')

    file_path = f'{dir_name}/{episode_type}-{date_today}.txt'
    file_exists = os.path.exists(file_path)

    if file_exists:
        print(f"An email was already sent to you with today's newest {episode_type} episodes.")
    else:
        driver_service = Service(executable_path=ChromeDriverManager(log_level=0).install())
        driver = webdriver.Chrome(service=driver_service)

        if episode_type == 'FREE':
            driver.get(url_free)
        else:
            driver.get(url_premium)

        source_data = driver.page_source
        soup = BeautifulSoup(source_data, 'lxml')
        today_data = soup.find('li', class_='day active today')
        new_episodes = today_data.find_all('li')

        if not new_episodes:
            print(f'No {episode_type} episodes releasing today.')
        else:
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
                file_name = os.path.basename(f.name)

            email_alert.email_alert(f'{date_today} Crunchyroll {episode_type} Releases', 'Txt file attached...', str(email), file_data, file_name)
            print(f'Check your email for episode updates!\n')


if __name__ == '__main__':
    while True:
        new_episodes_alert()
        time_wait = 24
        time.sleep(time_wait * 3600)
