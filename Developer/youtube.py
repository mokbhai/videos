import os
import pickle
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.errors import HttpError
from requests import Request # type: ignore
from google.auth.transport.requests import Request

VIDEO_FILE = "child-p3_with_subtitles"
CLIENT_SECRETS_FILE = "../google_sec.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

title = "(2) From Little Brat to Supreme Commander: My Unlikely Journey to Leading the Elite Forces."
description = """
In the quiet solitude of my room, 
I left behind a suicide note - a testament of my resolve, a farewell to my past life. 
At the tender age of 10, with hair barely grown, I embarked on a journey that would change my life forever. 
I joined the army, leaving behind the comforts of childhood. Months passed, and against all odds, I rose through the ranks. 
I became a military team instructor, leading an invincible team of female soldiers.
 My age and appearance belied my strength and determination, for I was a force to be reckoned with.

Part 3
Platlist: 
Stay tuned as more parts are coming soon!

See other series: 
The Ordinary Cultivator: https://www.youtube.com/playlist?list=PL_W6A9WF_sWi4a9F8O8Gnx9Bm_TBo4CHm
My Grandpa Rebbeled: https://www.youtube.com/playlist?list=PL_W6A9WF_sWjuO-F8UFDlJWuxz-BRlVFC
https://www.youtube.com/playlist?list=PL_W6A9WF_sWhnY2JiNUWBVRnqKP9ALEP5
.....

If You Need Subtitles, Please Turn on the CC Subtitles in the Lower Right Corner, Enjoy :)

Enjoy the video and don't forget to like, share, and subscribe for more anime, novel and manga content!

NOTE: The plot is purely fictional, please do not bring it into reality

Tags:
#animerecap #manhwaedit #anime #animerecommendations #manhwarecommendation #manga #mangaunboxing #mangacollection #webtoon #manhwarecap #anime #animerecap 
"""

def get_authenticated_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('youtube.pickle'):
        with open('youtube.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('youtube.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def initialize_upload(youtube):
    media = MediaFileUpload("../Videos/" + VIDEO_FILE + ".mp4", mimetype='video/mp4', resumable=True, chunksize=-1)  # maximum chunk size
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["#animerecap", "#manhwaedit", "#anime", "#animerecommendations", "#manhwarecommendation", "#manga", "#mangaunboxing", "#mangacollection", "#webtoon", "#manhwarecap", "#anime", "#animerecap"],
                "categoryId": "1",
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        },
        media_body=media
    )

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    print("Upload Complete!")
    print(response)
    
    # video_id = response['id']  # Extract video ID from the response
    
    # # Create a MediaFileUpload object for the subtitle file
    # subtitle_media = MediaFileUpload("../Videos/" + VIDEO_FILE + ".vtt", mimetype='text/vtt', resumable=True)  # VTT subtitle file
    
    # # Add subtitles to the video
    # request = youtube.captions().insert(
    #     part="snippet",
    #     body={
    #         "snippet": {
    #             "videoId": video_id,  # Use the video ID from the response
    #             "language": "en",
    #             "name": "English subtitles",
    #             "videoSnippet": {
    #                 "categoryId": "1"
    #             },
    #             "selfDeclaredMadeForKids": "No"
    #         }
    #     },
    #     media_body=subtitle_media  # Use the subtitle MediaFileUpload object
    # )

if __name__ == '__main__':
    youtube = get_authenticated_service()
    initialize_upload(youtube)
