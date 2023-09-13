from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def getChannelData(user):
    url = f"https://www.youtube.com/@{user}/about"
    driver = webdriver.Chrome()

    driver.get(url)
    driver.find_element(By.TAG_NAME, 'button').click()

    channelName = driver.find_element(By.CLASS_NAME, 'ytd-channel-name').text

    subs_txt = driver.find_element(By.ID, 'subscriber-count').text
    subs = float(subs_txt.split(' ')[0])
    if 'K' in subs_txt:
        subs = subs*1000

    videos_txt = driver.find_element(By.ID, 'videos-count').text
    videos_count = float(videos_txt.split(' ')[0])
    metadata = driver.find_elements(By.TAG_NAME, 'yt-formatted-string')


    fechaInicio = ''
    visualizaciones = ''
    for m in metadata:
        if 'Se unió' in m.text:
            fechaInicio = m.text
        if 'visualizaciones' in m.text:
            visualizaciones = m.text.split(' ')[0].replace(".", "")
            visualizaciones =float(visualizaciones)

    url = f"https://www.youtube.com/results?search_query={user}&sp=EgIQAQ%253D%253D"

    driver.get(url)
    video_links = []
    while len(video_links) < 3:
        items = driver.find_elements(By.ID, 'dismissible')
        for i in items:
            if channelName in i.text:
                urls = i.find_elements(By.TAG_NAME, 'a')
                for a in urls:
                    if 'video-title' in a.get_attribute('id'):
                        href = a.get_attribute('href')
                        video_links.append(href)
        print ("LINKS: ",len(video_links))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    for url in video_links:
        print("-> ",url)
        driver.get(url)
        title = driver.find_element(By.ID, 'title').text
        print(title)
        metadata = driver.find_element(By.ID, 'info-container').text
        print(metadata)

getChannelData('BettaTech')