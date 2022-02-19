from asyncio.windows_events import NULL
from msilib.schema import Error
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from youtube_dl.utils import UnsupportedError, DownloadError
import os
import json
import youtube_dl
import ffmpeg
from datetime import datetime
import re
import sys
import argparse
import requests
import time
import os.path
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")

# disable the banner "Chrome is being controlled by automated test software"
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
url=input("Facebook-Page: ")
# global driver
driver = webdriver.Chrome( options=chrome_options)

driver.get(url)

button=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Alle Cookies gestatten']"))).click()

driver.implicitly_wait(10)
links=[]
links_videos_dl=[]
titles=[]



SCROLL_PAUSE_TIME = 1
  
videoLinks=set()
videoTitles=set()

info=dict()
videoTitleMapping=dict()


while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    
      
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
   
    
    
    if new_height == last_height:
        
        break
    last_height = new_height
    

links = [elem.get_attribute("href") for elem in driver.find_elements(By.XPATH,"//span/div/a")]
titles=[elem.get_attribute("textContent") for elem in driver.find_elements(By.XPATH,"//span/div/a/span/span")]
for index,link in enumerate(links):
   
    if link and index < 3:
        if url in link:
            videoLinks.add(link)
    
for index,title in enumerate(titles):
    if index < 3:
     videoTitles.add(title)
     
print("LÄNGELINKS", len(videoLinks))
print('LÄNGETITLE', len(videoTitles))
jsonVideoTitleMapping=''
videoTitleMapping=dict()
zipped=zip(videoLinks, videoTitles)
for videoLink, title in zipped:
    input_video=None
    input_audio=None
    # if index+1==len(videoLinks):
    #     break
    print('videoLInksLoop')
    ydl_opts = {"format":"bestvideo/best","outtmpl":"%(id)s.%(ext)s", "ignoreerrors":True}
    try:
            
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            
            ydl.download([videoLink])
            
            info= ydl.extract_info(videoLink, download=False, process=True)
        
            print('INFO!!!', info['id'])
            videoTitleMapping[info['id']]=title
            
            
            

                
                
            if os.path.isfile(f"{info['id']}.mp4"):
                input_video = ffmpeg.input(f"{info['id']}.mp4")
            else:
                input_video = ffmpeg.input(f"{info['id']}.webm")
                    
                    
        ydl_opts = {"format":"bestaudio/best","outtmpl":"%(id)s.%(ext)s", "ignoreerrors":True}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([videoLink])
            print(videoLink)
            info= ydl.extract_info(videoLink, download=False, process=True)
            
            if os.path.isfile(f"{info['id']}.m4a"):
                input_audio = ffmpeg.input(f"{info['id']}.m4a")
            
            
        
            if os.path.isfile(f"./processed/final_{info['id']}.mp4"):
                print("File already downloaded")
            else:
                if input_audio==None:
                    if os.path.isfile(f"{info['id']}.webm"):
                        shutil.move(f"{info['id']}.webm", f"./processed/final_{info['id']}.webm")
                    else:
                        shutil.move(f"{info['id']}.mp4", f"./processed/final_{info['id']}.mp4")
                else:
                    print('prossing')
                    if input_video and input_audio:    
                        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f"./processed/final_{info['id']}.mp4").run()
    except:
        print('failed')
        
        
    finally:
        print('Done')
         
  


with open("videoTitles.json", "w") as file:
    json.dump(videoTitleMapping, file)       
    
        
