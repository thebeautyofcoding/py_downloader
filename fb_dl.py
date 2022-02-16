from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import youtube_dl
import ffmpeg
from datetime import datetime
import re
import sys
import argparse
import requests
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")

# disable the banner "Chrome is being controlled by automated test software"
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
url=input('Facebook-Page: ')
# global driver
driver = webdriver.Chrome( options=chrome_options)

driver.get(url)

button=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Alle Cookies gestatten']"))).click()


links = [elem.get_attribute("href") for elem in driver.find_elements(By.TAG_NAME,'a')]
videoLinks=set()
for link in links:
    if '/videos/' in link:
        videoLinks.add(link)

print('VIDEOLINKS',videoLinks)
# excList= ["https://www.facebook.com/NyjahHustonSkate/videos/rome-was-tighttt-next-stop-olympics/4035254959901270/", "https://www.facebook.com/NyjahHustonSkate/videos/yesterdays-send/1401324856907350/"]


   

info=dict()
videoTitleMapping=dict()


def createVideoTitleMapping(slug, index):
   
    videoTitleMapping[index]=slug
 
    jsonVideoTitleMapping=json.dumps(videoTitleMapping, indent=4)
    with open("videoTitles.json", "w") as outfile:
        outfile.write(jsonVideoTitleMapping)
        
def extractTitle(info):
       webpage_url=info['webpage_url']
       slug=webpage_url.split('/')[5]
       return slug
     

for index, videoLink in enumerate(videoLinks):
    input_audio=NULL
    input_video=NULL
    ydl_opts = {'format':'bestvideo/best','outtmpl':'{}.%(ext)s'.format(index)}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoLink])
        info= ydl.extract_info(videoLink, download=False, process=True)
        print('INFO', info)
        slug=extractTitle(info)
        createVideoTitleMapping(slug, index)
        if os.path.isfile('./{}.mp4'.format(index)):
            input_video = ffmpeg.input('./{}.mp4'.format(index))
        else:
            input_video = ffmpeg.input('./{}.webm'.format(index))
        
        
    ydl_opts = {'format':'bestaudio/best','outtmpl':'{}.%(ext)s'.format(index)}
   
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoLink])
        info= ydl.extract_info(videoLink, download=False, process=True)
     
        input_audio = ffmpeg.input('./{}.m4a'.format(index))
        
        
       
    if os.path.isfile('./processed/final_{}.mp4'.format(index)):
        print('File already downloaded')
    else:
        
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output('./processed/final_{}.mp4'.format(index)).run()
# driver.implicitly_wait(2)
# # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
# username_box = driver.find_element_by_xpath('//*[@id ="email"]')
# username_box.send_keys('heinergiehl2005@yahoo.de')

# password_box = driver.find_element_by_xpath('//*[@id ="pass"]')
# password_box.send_keys('Heiner123@')

# WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, "login"))).click()