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
        # self.options.add_argument("--headless")
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
            subs = subs_txt.split(' ')[0]
            subs = float(subs)
            if 'K' in subs_txt:
                subs = subs*1000
            elif 'M' in subs_txt:
                subs = subs*1000000

            response['subs'] = subs
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

    async def getChannelVideos(self):
        url = f"https://www.youtube.com/@{self.user}/videos"

        # accept cookies
        self.chrome.get(url)
        self.chrome.find_element(By.TAG_NAME, 'button').click()

        inifinityScroll = self.chrome.find_element(By.ID, 'refresh')
        videos = []
        end_scroll = False
        next_item = 0
        while not end_scroll:
            prev_rows = self.chrome.find_elements(
                By.TAG_NAME, 'ytd-rich-grid-row')
            items = self.chrome.find_elements(By.ID, 'dismissible')
            print(f"Hay {len(items)} items")
            while next_item < len(items):
                item = items[next_item]
                thumbnail = ''
                while thumbnail == '':
                    img = item.find_element(
                        By.TAG_NAME, 'img')
                    thumbnail = img.get_property('src')
                    self.chrome.execute_script(
                        "arguments[0].scrollIntoView(true);", img)
                    time.sleep(0.5)

                link = item.find_element(By.ID, 'video-title-link')
                href = link.get_attribute('href')
                title = link.text
                video = {
                    "url": href,
                    "title": title,
                    "thumbnail": thumbnail
                }
                videos.append(video)
                next_item = next_item+1

            print(f"{len(videos)} videos scrapeados")
            print("=================================SCROLL=====================")
            self.chrome.execute_script(
                "arguments[0].scrollIntoView(true);", inifinityScroll)
            print(f"Await...")
            time.sleep(2)
            new_rows = self.chrome.find_elements(
                By.TAG_NAME, 'ytd-rich-grid-row')
            if len(new_rows) == len(prev_rows):
                print(f"FIN DEL SCROLL  -> {prev_rows} - {new_rows}")
                end_scroll = True

        return videos
