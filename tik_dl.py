from ast import arg
from TikTokApi import TikTokApi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import ssl
import shutil
import json
import os
import urllib.request
from threading import Thread
import sys
context = ssl._create_unverified_context()
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")




url=input("TikTok-Account: ")
# SCROLL_PAUSE_TIME = 1

# driver = webdriver.Chrome(options=chrome_options)
# driver.implicitly_wait(10)
# driver.get(url)
verifyFP='verify_71639d688d207a308842f7d4ec6d2013'
api = TikTokApi(custom_verify_fp=verifyFP, use_test_endpoints=True)

# while True:
#     last_height = driver.execute_script("return document.body.scrollHeight")
    
      
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


#     time.sleep(SCROLL_PAUSE_TIME)
#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
   
    
    
#     if new_height == last_height:
        
#         break
#     last_height = new_height


user = api.user(username=url)
user.as_dict # -> dict of the user_object
# print(user.as_dict)
# print(user.videos())
videos= user.videos()
videos=list(videos)
video=videos[1]
vidDic=video.as_dict
vidCount=vidDic['authorStats']['videoCount']
vidDataList=list()


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


def download(dlurl,vidDic):
    
    with urllib.request.urlopen(dlurl, context=context) as response:
        with open(f"{vidDic['id']}.mp4", 'wb') as tmp_file:
            
            
            shutil.copyfileobj(response,tmp_file)
        shutil.move(f"{vidDic['id']}.mp4", f"processing/{vidDic['id']}.mp4")
        
        for filename in os.listdir(os.getcwd()+'\\processing\\'):
            shutil.move(f"processing/{filename}", f"processed/{filename}")
        
        
        

     
if int(vidCount) >1:
    for index, video in enumerate(user.videos(count=int(30))):
        if index <11 and index > 7:
            vidDic=video.as_dict
            dlurl=vidDic['video']['downloadAddr']
            vidTitleMapping=dict()
            vidTitleMapping['id']=vidDic['id']
            vidTitleMapping['description']=vidDic['desc']
            desc=input('Please provide a description or the default one will be used: ')
            title=input('Please provide a title or the default one will be used: ')
            tags=input('Please provide tags or none will be used: ')
            if title !='':
                vidTitleMapping['title']=title
            else:
                vidTitleMapping['title']='standard title'
            if desc !='':     
                vidTitleMapping['description']=desc
            
            if tags!='':   
                vidTitleMapping['tags']=tags
            else:
                vidTitleMapping['tags']=''
            
             
            vidDataList.append(vidTitleMapping)
            downloadThread=Thread(target=download, args=[dlurl, vidDic])
            downloadThread.start()
            
    
    with open("videoTitles.json", "w") as file:
        json.dump(vidDataList, file) 
            
            
            
          
           


  
                    
                    
   