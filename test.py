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
import videoUpload





tikTokOrFacebook=input('You want to download videos from Facebook or TikTok? Type "Facebook" or "TikTok": ')
if tikTokOrFacebook=='Facebook':
    import fb_dl
else:
 import tik_dl

class  Handler(FileSystemEventHandler):
    print('handler called')
    def on_any_event(self, event):
        if event.is_directory:
            print('HERE')
  
        elif event.event_type == 'created':
            for filename in os.listdir(folder_to_track):
                if '.mp4' in filename:
                    print('number of current threads is ', threading.active_count())
                    src = filename
                    new_dest = folder_destination  + filename
                    vidId= filename.split('.mp4')[0]
                    
                    videoUpload.getVideoMetaData(vidId)
                    shutil.move(f"./processed/{filename}", f"./uploaded/{filename}")
                    # file_size=None
                    # if os.path.isfile(src):
                    #     while file_size != os.path.getsize(src):
                    #         file_size = os.path.getsize(folder_to_track)
                    #         # print('Im WHILE Loop test.py')

                    #     while not file_done:
                    #         try:
                    #             shutil.move(f"./processed/{filename}", f"./uploaded/{filename}")
                    #             file_done = True
                    #         except:
                    #             return True        
                      
                    
                    
            print('createdEvent')   
folder_to_track=os.getcwd()+'\\processed\\'

folder_destination=os.getcwd()+'\\uploaded\\'


event_handler = Handler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)

observer.start()

    
try:
    while True:
     
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()

