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
from threading import Thread
import queue
from slugify import slugify
import threading

from videoUpload import getVideoMetaData
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

button=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Erforderliche und optionale Cookies erlauben']"))).click()

driver.implicitly_wait(10)
links=[]
links_videos_dl=[]
titles=[]



SCROLL_PAUSE_TIME = 2
  
videoLinks=set()
videoTitles=set()

info=dict()
def scrolling():
    while True:
        print('Scrolling down to get all links... \n')
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            time.sleep(1)
            break
        last_height = new_height
    
input_video=None
input_audio=None
links = [elem.get_attribute("href") for elem in driver.find_elements(By.XPATH,"//span/div/a")]
titles=[elem.get_attribute("textContent") for elem in driver.find_elements(By.XPATH,"//span/div/a/span/span")]
for index,link in enumerate(links):
   
    if link and index < 3:
        if url in link:
            videoLinks.add(link)
    

jsonVideoTitleMapping=''
videoTitleMapping=dict()
info=dict()



_thread_target_key, _thread_args_key, _thread_kwargs_key = (
    ('_target', '_args', '_kwargs')
    if sys.version_info >= (3, 0) else
    ('_Thread__target', '_Thread__args', '_Thread__kwargs')
)

class ThreadWithReturn(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None
    
    def run(self):
        target = getattr(self, _thread_target_key)
        if target is not None:
            self._return = target(
                *getattr(self, _thread_args_key),
                **getattr(self, _thread_kwargs_key)
            )
    
    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self._return

videoList=list()

def writeVideoData(videoData):
    with open("videoTitles.json", "w") as file:
         
        videoList.append(videoData)
        
        json.dump(videoList, file, indent=4)
            
        
            
        

def downloadVideo(ydl_opts):
    global videoList
    
   
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        input_video=None
        ydl.download([videoLink])

        info= ydl.extract_info(videoLink, download=False, process=True)
        
        videoTitleMapping=dict()
        slug=info['webpage_url'].split('/')[-3]
        slug=slug.replace('-', ' ')
        videoTitleMapping['id']=info['id']
        standardTitle='standard title'
        title=input(f'Provide a title or keep the default one ("{standardTitle}"): \n')
        
        if title != '':
            videoTitleMapping['title']=title
        else:
             videoTitleMapping['title']='standard title'
        
        desc=input(f'Provide a description or keep the default one ("{slug}"): ')
        if desc != '':
            videoTitleMapping['description']=desc
        else:
            videoTitleMapping['description']=slug
        
        
        
        tags=input('Provide tags (comma-seperated) or keep the default one: ')
        videoTitleMapping['tags']=tags
        
       
        # videoList.append(videoTitleMapping)
       
        if os.path.isfile(f"{info['id']}.mp4"):
            input_video = ffmpeg.input(f"{info['id']}.mp4")
            
            return [info,input_video,videoTitleMapping]
        else:
            input_video = ffmpeg.input(f"{info['id']}.webm")
            return [info,input_video,videoTitleMapping]
            
            
def downloadAudio(ydl_opts):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        
        ydl.download([videoLink])
            
        return ydl.extract_info(videoLink, download=False, process=True)
        

def processing(info, input_video):
    input_audio=None
    if os.path.isfile(f"{info['id']}.m4a"):
            input_audio = ffmpeg.input(f"{info['id']}.m4a")
    
    if os.path.isfile(f"./processing/{info['id']}.mp4"):
        print("File already downloaded")
    else:
        if input_audio==None:
            if os.path.isfile(f"{info['id']}.webm"):
                # shutil.move(f"{info['id']}.webm", f"./merged/{info['id']}.webm")
                shutil.move(f"{info['id']}.webm", f"./processed/{info['id']}.mp4")
            else:
                # shutil.move(f"{info['id']}.mp4", f"./merged/{info['id']}.mp4")
                shutil.move(f"{info['id']}.mp4", f"./processed/{info['id']}.mp4")
        else:
            print('prossing')
            if input_video and input_audio:    
                ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f"./processing/{info['id']}.mp4").run()
                shutil.move(f"./processing/{info['id']}.mp4", f"./processed/{info['id']}.mp4")
                if os.path.isfile(f"{info['id']}.m4a"):
                    os.remove(f"{info['id']}.m4a")
                if os.path.isfile(f"{info['id']}.mp4"):
                    os.remove(f"{info['id']}.mp4")
                
        
        
        getVideoMetaData(info['id'])
        shutil.move(f"processed/{info['id']}.mp4", f"./uploaded/{info['id']}.mp4")         
scrollingThread=Thread(target=scrolling, args=[])
scrollingThread.daemon=True
scrollingThread.start()
scrollingThread.join()
for videoLink in videoLinks:

    ydl_video = {"format":"bestvideo/best","outtmpl":"%(id)s.%(ext)s", "ignoreerrors":True}

    ydl_audio = {"format":"bestaudio/best","outtmpl":"%(id)s.%(ext)s", "ignoreerrors":True}
     
    threads=[ThreadWithReturn(target=downloadAudio, args=[ydl_audio]), ThreadWithReturn(target=downloadVideo, args=[ydl_video ])]   
    
    try:
        
        threads[0].daemon=True
        threads[0].start()
        threads[0].join()
        
        threads[1].daemon=True
        threads[1].start()
        threads[1].join()
        
        writingTh=Thread(target=writeVideoData, args=[threads[1].join()[2]])
        writingTh.start()
        writingTh.join()
        
        th=Thread(target=processing, args=[threads[1].join()[0],threads[1].join()[1]])
        th.daemon=True
        th.start()
        th.join()
        
        
       
        
        
       
  
       
        
        
    except Exception as e:
        print('Error!!: ', e)
        

    



    
    
    
    
        
