# ffmpeg -i input.mp4 -vf scale=3840:2160 -c:v libx264 -preset slow -crf 21 output_4k.mp4


import os
import pickle
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.errors import HttpError
from requests import Request # type: ignore
from google.auth.transport.requests import Request

VIDEO_FILE = "max-level-learning-p2_with_subtitles"
CLIENT_SECRETS_FILE = "../google_sec.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

title = "(2) Max level understanding: meditated facing wall of Cliff of Pondering for eighty years."
description = """
"Li Qingshan, as a senior disciple of the Yuhua Gate and the prince of the Great Yan Dynasty, was deceived and let go of the Demon Gate Empress. Do you acknowledge your crime?"
"I am willing to give up my senior disciple identity, be imprisoned at the Repentance Cliff, and wipe the stone tablets clean."
"Approved, but you must abolish your cultivation, shatter your roots, and never leave for the rest of your life!"
From then on, Li Qingshan secluded himself at the Repentance Cliff, wiping the stone tablets, and unexpectedly activated the highest level of insight.
【You carefully watched, triggering the highest level of insight, and comprehended the Great River Sword Qi epiphany】
【You carefully watched, triggering the highest level of insight, and understood the Triple Sword Strike】
【You carefully watched, triggering the highest level of insight, and understood the Heavenly Seal】
Decades later, the Immortal Dao Ranking arrived, listing the top experts in the mortal world, with Li Qingshan directly ranking first.
The ranking's evaluation of him - God among mortals!

Part 2

Playlist: 

Stay tuned as more parts are coming soon!

See other series: 
The Ordinary Cultivator: https://www.youtube.com/playlist?list=PL_W6A9WF_sWi4a9F8O8Gnx9Bm_TBo4CHm
My Grandpa Rebbeled: https://www.youtube.com/playlist?list=PL_W6A9WF_sWjuO-F8UFDlJWuxz-BRlVFC
https://www.youtube.com/playlist?list=PL_W6A9WF_sWhnY2JiNUWBVRnqKP9ALEP5
.....

If You Need Subtitles, Please Turn on the CC Subtitles in the Lower Right Corner, Enjoy :)

Enjoy the video and don't forget to like, share, and subscribe for more anime, novel and manga content!

NOTE: The plot is purely fictional, please do not bring it into reality

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
                "tags": [],
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
