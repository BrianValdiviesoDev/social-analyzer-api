from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from schemas.youtube import YoutubeVideoResponse, YoutubeStatsPost, YoutubeVideoStatsPost, YoutubeVideoPost


class YouTubeScrapper:
    def __init__(self, user=''):
        self.user = user
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument('--mute-audio')
        self.chrome = webdriver.Chrome(options=self.options)

    async def getChannelData(self) -> YoutubeStatsPost:

        url = f"https://www.youtube.com/@{self.user}/about"

        # accept cookies
        self.chrome.get(url)
        self.chrome.find_element(By.TAG_NAME, 'button').click()

        response = YoutubeStatsPost()
        '''
        try:
            response['channelName'] = self.chrome.find_element(
                By.CLASS_NAME, 'ytd-channel-name').text
        except:
            response['channelName'] = 'NOT FOUND'
        '''

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.ID, 'subscriber-count'))
        )
        subs_txt = self.chrome.find_element(By.ID, 'subscriber-count')
        try:
            subs = subs_txt.text.split(' ')[0]
            if ',' in subs:
                subs = subs.replace(',', '.')
            subs = float(subs)
            if 'K' in subs_txt.text:
                subs = subs*1000
            elif 'M' in subs_txt.text:
                subs = subs*1000000
            response.subs = subs
        except:
            response.subs = -1

        videos_txt = self.chrome.find_element(By.ID, 'videos-count')
        try:
            videos = videos_txt.text.split(' ')[0]
            response.videos = float(videos)
        except:
            response.videos = -1

        right_column = self.chrome.find_element(
            By.ID, 'right-column')
        metadata = right_column.find_elements(
            By.TAG_NAME, 'yt-formatted-string')

        try:
            initDate = metadata[1].find_elements(By.TAG_NAME, 'span')[1].text
            response.startAt = self.transformDate(initDate)
        except:
            response.startAt = 'NOT FOUND'

        try:
            visualizaciones = metadata[2].text.split(' ')[0].replace(".", "")
            response.views = float(visualizaciones)
        except:
            response.views = -1
        self.chrome.quit()
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

    async def getChannelVideos(self) -> list[YoutubeVideoPost]:
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
                video = YoutubeVideoPost(
                    url=href, title=title, thumbnail=thumbnail)
                videos.append(video)
                next_item = next_item+1

            self.chrome.execute_script(
                "arguments[0].scrollIntoView(true);", inifinityScroll)
            time.sleep(2)
            new_rows = self.chrome.find_elements(
                By.TAG_NAME, 'ytd-rich-grid-row')
            if len(new_rows) == len(prev_rows):
                end_scroll = True
        self.chrome.quit()
        return videos

    async def getVideoStatistics(self, url) -> YoutubeVideoStatsPost:
        response = YoutubeVideoStatsPost(
            views=0, likes=0, comments=0, timestamp=datetime.utcnow())

        # accept cookies
        self.chrome.get(url)
        print(f"OPEN: {url} -> {datetime.now()}")
        dialog = WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.ID, 'dialog'))
        )

        buttons = dialog.find_elements(By.TAG_NAME, 'button')
        button = buttons[len(buttons) - 1]
        button.click()

        longDate = False
        counter = 0
        while not longDate and counter < 10:
            dialog = WebDriverWait(self.chrome, 10).until_not(
                EC.presence_of_element_located((By.ID, 'dialog'))
            )
            description = WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.ID, 'description-inner'))
            )
            time.sleep(2)
            try:
                description.click()
            except:
                print("No se puede hacer click en descripcion: ", description.text)
            info = WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.ID, 'info-container'))
            )
            counter = counter + 1
            spans = info.find_elements(By.TAG_NAME, 'span')
            try:
                txt = spans[2].text
                txt = txt.split(' ')
                if len(txt[len(txt)-1]) > 3:
                    longDate = True
                    date = spans[2].text
                    try:
                        date = self.transformDate(date)
                    except:
                        if ":" in date:
                            date = date.split(': ')[1]
                            date = self.transformDate(date)
                    response.date = date
            except:
                print("No se puede dividir")

        if not longDate:
            print(f"DATE ERROR: {spans[0].text} -> {datetime.now()}")

        spans = info.find_elements(By.TAG_NAME, 'span')

        print(f"ALL SHOWED: -> {datetime.now()}")

        actions = self.chrome.find_element(By.ID, 'actions')
        menu = actions.find_element(By.TAG_NAME, 'ytd-menu-renderer')
        buttons = menu.find_elements(By.TAG_NAME, 'button')
        try:
            likeButton = buttons[0]
            likes_txt = likeButton.get_attribute('aria-label')
            likes_txt = likes_txt.split(' ')
            likes = 0
            for part in likes_txt:
                if part.isdigit():
                    likes = float(part)
                    break
            response.likes = likes
        except:
            likes = -1
            print(f"LIKES ERROR: {buttons[0].text} -> {datetime.now()}")

        try:
            visualizations = spans[0].text
            visualizations = str(visualizations).replace(
                '.', '').replace(',', '.')
            views = visualizations.split(' ')[0]
            views = float(views)
            if 'K' in visualizations:
                views = views*1000
            elif 'M' in visualizations:
                views = views*1000000
            response.views = views
        except:
            visualizations = -1
            print(f"VIEWS ERROR: {spans[0].text} -> {datetime.now()}")
        '''
        try:
            videoDescription = self.chrome.find_element(
                By.TAG_NAME, 'ytd-text-inline-expander').text
        except:
            videoDescription = 'NOT FOUND'
        '''
        comments = 0
        self.chrome.execute_script("window.scrollBy(0, 5000);")
        time.sleep(1)
        self.chrome.execute_script("window.scrollBy(0, 5000);")
        time.sleep(1)

        h2 = self.chrome.find_elements(By.TAG_NAME, 'h2')

        try:
            for e in h2:
                count = e.find_element(By.TAG_NAME, 'yt-formatted-string')
                if count:
                    spans = count.find_elements(By.TAG_NAME, 'span')
                    if len(spans) > 0:
                        comments = spans[0].text
            response.comments = comments
        except:
            comments = -1
            print(f"COMMENTS ERROR:  -> {datetime.now()}")

        print(f"{datetime.now()}==============================")
        print(response)
        print("==============================")
        self.chrome.quit()
        return response
