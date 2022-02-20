from TikTokApi import TikTokApi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import ssl
import shutil
import json
import os
import urllib.request
context = ssl._create_unverified_context()
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")




# url=input("TikTok-Page: ")
# SCROLL_PAUSE_TIME = 1

# driver = webdriver.Chrome(options=chrome_options)
# driver.implicitly_wait(10)
# driver.get(url)
verifyFP='verify_71a37c19940122ac0989cadd0e62bf3c'
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


user = api.user(username='danyellebutlercoach')
user.as_dict # -> dict of the user_object
# print(user.as_dict)
# print(user.videos())
videos= user.videos()
videos=list(videos)
video=videos[1]
vidDic=video.as_dict
vidCount=vidDic['authorStats']['videoCount']
vidTitleMapping=dict()
if int(vidCount) >1:
    for index, video in enumerate(user.videos(count=int(30))):
        if index <11 and index > 7:
            vidDic=video.as_dict
           
            dlurl=vidDic['video']['downloadAddr']
            with urllib.request.urlopen(dlurl, context=context) as response:
                with open(f"{vidDic['id']}.mp4", 'wb') as tmp_file:
                    vidTitleMapping[vidDic['id']]=vidDic['desc']
                    shutil.copyfileobj(response,tmp_file)
                shutil.move(f"{vidDic['id']}.mp4", f"processed/{vidDic['id']}.mp4")
                    
                    
with open("videoTitles.json", "w") as file:
    json.dump(vidTitleMapping, file)     