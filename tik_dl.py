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
from videoUpload import getVideoMetaData
context = ssl._create_unverified_context()
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")




url=input("TikTok-Account: ")

verifyFP='verify_l00q2i8m_gVL5oYOe_Xbzx_40AD_8qOL_yT4jmjBcrF2U'
api = TikTokApi(custom_verify_fp=verifyFP, use_test_endpoints=True)


user = api.user(username=url)
user.as_dict # -> dict of the user_object

videos= user.videos()
videos=list(videos)
video=videos[1]
vidDic=video.as_dict
vidCount=vidDic['authorStats']['videoCount']
vidDataList=list()



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
            standardTitle='standard title'
            title=input(f'Please provide a title or the default one ("{standardTitle}") will be used: ')
            desc=input(f'Please provide a description or the default one ({vidTitleMapping["description"]}) will be used: ')
            
            tags=input('Please provide tags or none will be used: ')
            if title !='':
                vidTitleMapping['title']=title
            else:
                vidTitleMapping['title']=standardTitle
            if desc !='':     
                vidTitleMapping['description']=desc
            
            if tags!='':   
                vidTitleMapping['tags']=tags
            else:
                vidTitleMapping['tags']=''
            
             
            vidDataList.append(vidTitleMapping)
            with open("videoTitles.json", "w") as file:
                json.dump(vidDataList, file) 
            download(dlurl, vidDic)
            getVideoMetaData(vidTitleMapping['id'])
            shutil.move(f"processed/{vidTitleMapping['id']}.mp4", f"./uploaded/{vidTitleMapping['id']}.mp4")
            
            
    
    
            
            
            
          
           


  
                    
                    
   