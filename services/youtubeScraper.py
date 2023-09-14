from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from models.socialSource import YoutubeStatistics
from datetime import datetime


class YouTubeScrapper:
    def __init__(self, user):
        self.user = user
        self.options = Options()
        self.options.add_argument("--headless")
        self.chrome = webdriver.Chrome(options=self.options)

    async def getChannelData(self) -> dict:

        url = f"https://www.youtube.com/@{self.user}/about"

        # accept cookies
        self.chrome.get(url)
        self.chrome.find_element(By.TAG_NAME, 'button').click()

        response = {
            "channelName": '',
            "subs": 0,
            "videos": 0,
            "visualizations": 0,
            "startAt": '',
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            response['channelName'] = self.chrome.find_element(
                By.CLASS_NAME, 'ytd-channel-name').text
        except:
            response['channelName'] = 'NOT FOUND'

        try:
            subs_txt = self.chrome.find_element(By.ID, 'subscriber-count').text
            subs_txt = subs_txt.split(' ')[0]
            response['subs'] = float(subs_txt)
            if 'K' in subs_txt:
                subs = subs*1000
            elif 'M' in subs_txt:
                subs = subs*1000000
        except:
            response['subs'] = -1

        try:
            videos_txt = self.chrome.find_element(By.ID, 'videos-count').text
            response['videos'] = float(videos_txt.split(' ')[0])
        except:
            response['videos'] = -1

        right_column = self.chrome.find_element(
            By.ID, 'right-column')
        metadata = right_column.find_elements(
            By.TAG_NAME, 'yt-formatted-string')

        try:
            initDate = metadata[1].find_elements(By.TAG_NAME, 'span')[1].text
            response["startAt"] = self.transformDate(initDate)
        except:
            response['startAt'] = 'NOT FOUND'

        try:
            visualizaciones = metadata[2].text.split(' ')[0].replace(".", "")
            response['visualizations'] = float(visualizaciones)
        except:
            response['visualizations'] = -1
        print(response)
        return response

    def transformDate(self, fecha_str):
        months = {
            'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
            'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
            'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
        }

        date = fecha_str.split()
        day = date[0]
        month = date[1].lower()
        year = date[2]

        month = months.get(month, month)

        result = datetime.strptime(
            f'{day} {month} {year}', '%d %b %Y').strftime('%Y-%m-%d')

        return result

    def getChannelVideos(self, channelName):
        url = f"https://www.youtube.com/results?search_query={channelName}&sp=EgIQAQ%253D%253D"

        # accept cookies
        self.driver.get(url)
        self.driver.find_element(By.TAG_NAME, 'button').click()

        video_links = []
        while len(video_links) < 3:
            items = self.driver.find_elements(By.ID, 'dismissible')
            for i in items:
                if channelName in i.text:
                    urls = i.find_elements(By.TAG_NAME, 'a')
                    for a in urls:
                        if 'video-title' in a.get_attribute('id'):
                            href = a.get_attribute('href')
                            video_links.append(href)
            print("LINKS: ", len(video_links))
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        for url in video_links:
            print("-> ", url)
            self.driver.get(url)
            title = self.driver.find_element(By.ID, 'title').text
            print(title)
            metadata = self.driver.find_element(By.ID, 'info-container').text
            print(metadata)
