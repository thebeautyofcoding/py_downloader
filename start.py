import re
import sys
import time
import logging
import shutil
import ssl
import urllib.request
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
# import videoUpload
import threading


from threading import Thread



import videoUpload

class  Handler(FileSystemEventHandler):
    
    def on_created(self, event):
        onCreatedMethod()
        
                  
folder_to_track=os.getcwd()+'\\processed\\'

folder_destination=os.getcwd()+'\\uploaded\\'                     

def onCreatedMethod():
    for filename in os.listdir(folder_to_track):
        if '.mp4' in filename:
          
            
            vidId= filename.split('.mp4')[0]
            
            
            videoUpload.getVideoMetaData(vidId)
            
         
            
            
            
            
            if os.path.isfile(f"./processed/{filename}"):
                shutil.move(f"./processed/{filename}", f"./uploaded/{filename}")
            
          
                    
event_handler = Handler()
observer = Observer()                           
def runObserver():           
    
    
    observer.schedule(event_handler, folder_to_track, recursive=True)

    observer.start()
    while True:
        time.sleep(1)
        


if __name__=='__main__':
    background_thread = threading.Thread(target=runObserver, args=())
    background_thread.daemon = True
    background_thread.start()
    tikTokOrFacebook=input('You want to download videos from Facebook or TikTok? Type "Facebook" or "TikTok": ')
    
    
    try:
        while True:
            if tikTokOrFacebook=='Facebook':
                import fb_dl
                
                onCreatedMethod()
                if len(os.listdir(folder_to_track))== 0:
                    break
                
            else:
                import tik_dl
                
                onCreatedMethod()
                if len(os.listdir(folder_to_track))== 0:
                    break
                
            
            
    except KeyboardInterrupt:
        
        observer.stop()
        
        