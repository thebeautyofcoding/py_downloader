import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import videoUpload

class  Handler(FileSystemEventHandler):
    print('handler clalled')
    def on_any_event(self, event):
        if event.is_directory:
            return None
  
        elif event.event_type == 'created':
            for filename in os.listdir(folder_destination):
                if '.mp4' in filename:
                    print(folder_to_track)
                    src = folder_to_track + '\\' +filename
                    new_dest = folder_destination + '\\' + filename
                    videoUpload.getVideoMetaData()
                    print(filename)
            print()   
folder_to_track=os.getcwd()

folder_destination=os.getcwd()+'\\processed\\'


event_handler = Handler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()
    
try:
    while True:
      
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
observer.join()