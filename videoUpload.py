# token.pickle stores the user's credentials from previously successful logins
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import json
from google.auth.transport.requests import Request
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
     
      credentials = pickle.load(token)
from googleapiclient.discovery import build
import time
import httplib2
import random
from urllib.error import HTTPError
httplib2.RETRIES = 1
from apiclient.http import MediaFileUpload

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


credentials=None



# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=[
                "https://www.googleapis.com/auth/youtube.upload"
            ]
        )

        flow.run_local_server(port=3000, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def resumable_upload(insert_request):
 
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print( "Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print ("Video id '%s' was successfully uploaded." % response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HTTPError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print (error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)
      
      
def initialize_upload(youtube, video):
      
  tags = None
  if video.keywords:
    tags = video.keywords.split(",")

  body=dict(
    snippet=dict(
      title=video.title,
      description=video.description,
      tags=tags,
      category=video.categoryId
    ),
    status=dict(
      privacyStatus=video.privacyStatus
    )
  )
  # Call the API's videos.insert method to create and upload the video.
  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    # The chunksize parameter specifies the size of each chunk of data, in
    # bytes, that will be uploaded at a time. Set a higher value for
    # reliable connections as fewer chunks lead to faster uploads. Set a lower
    # value for better recovery on less reliable connections.
    #
    # Setting "chunksize" equal to -1 in the code below means that the entire
    # file will be uploaded in a single HTTP request. (If the upload fails,
    # it will still be retried where it left off.) This is usually a best
    # practice, but if you're using Python older than 2.6 or if you're
    # running on App Engine, you should set the chunksize to something like
    # 1024 * 1024 (1 megabyte).
    media_body=MediaFileUpload(video.filename, chunksize=-1, resumable=True)
  )
  resumable_upload(insert_request)
  return True
        



    
#   argparser.add_argument("--file", required=True, help="Video file to upload")
#   argparser.add_argument("--title", help="Video title", default="Test Title")
#   argparser.add_argument("--description", help="Video description",
#     default="Test Description")
#   argparser.add_argument("--category", default="22",
#     help="Numeric video category. " +
#       "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
#   argparser.add_argument("--keywords", help="Video keywords, comma separated",
#     default="")
#   argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
#     default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
#   args = argparser.parse_args()

#   if not os.path.exists(args.file):
#     exit("Please specify a valid file using the --file= parameter.")
 
class VideoToUpload:
    def __init__(self, title, filename):
        self.title="test title"
        self.description=title
        self.privacyStatus=VALID_PRIVACY_STATUSES[1]
        self.categoryId="22",
        self.keywords=''
        self.filename=filename
        print('title1', self.title)        
directory = os.fsencode('processed')
filenames=list()
data=None
vidToUpload=None
# videosToUpload=list()
data=None
def getVideoMetaData(vidId):
    print('ICHRENNE')
    keys= list()
    
    with open('videoTitles.json', 'r') as f:
        data=json.load(f)
        keys= data.keys()
    print('IDDDD', vidId)    
    title=data[vidId]
    
    youtube= build('youtube', 'v3', credentials=credentials)
    # # app.run(host='localhost', port=3000)1
    # print('gehe ich hier hin',videosToUpload)
    # for vid in videosToUpload:
    #   print('vid', vid)
    for file in os.listdir(directory):
      id=os.fsdecode(file).split('.mp4')[0]
      if id==vidId:
        
        videoToUpload= VideoToUpload(title, f"processed/{os.fsdecode(file)}")
    try:
        # time.sleep(60)
        # print('Waiting 60')
        initialize_upload(youtube, videoToUpload)
        
        
    except HTTPError as e:
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    
  
    
    # zipped=zip(keys,filenames)
    
        
    # for key, file in zipped:
    #     print('file', file)
    #     if key in file:
        
    #         videoToUpload= VideoToUpload(data[key], f"processed/{file}")
            
    #         videosToUpload.append(videoToUpload)
    #         print('videosToUpload', videosToUpload)
                
                
                
# getVideoMetaData()


      