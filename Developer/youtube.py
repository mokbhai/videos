import os
import pickle
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.errors import HttpError
from requests import Request # type: ignore

VIDEO_FILE = "4skills"
chapters = "every-one-has-4-skills p1"
CLIENT_SECRETS_FILE = "../google_sec.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

description = """
Awakening Destiny: Mo Xiu's Journey to the Unknown Part - 1

Dive into the world of Shun City First High School where humans are bestowed with extraordinary abilities. Witness the journey of Mo Xiu, a diligent student standing on the brink of awakening his abilities. As the crucial college entrance exam looms, Mo Xiu faces not just academic challenges but also the anxiety of his impending 18th birthday - the day he either awakens his abilities or remains ordinary. Amid the pressure, an unexpected challenge from a classmate brings about a surprising revelation. Watch the story unfold as Mo Xiu navigates through his extraordinary journey towards his destiny. Don't miss out on the full story, subscribe now!

Playlist: https://www.youtube.com/playlist?list=PL_W6A9WF_sWjWb8F_0KQYxHUT7ooajKOX

If You Need Subtitles, Please Turn on the CC Subtitles in the Lower Right Corner, Enjoy :)

Tags:
#animerecap #manhwaedit #anime #animerecommendations #manhwarecommendation #manga #mangaunboxing #mangacollection #webtoon #manhwarecap #anime #animerecap 

Copyright Notice
⚠️ COPYRIGHT NOTICE: All content in this video is the property of MokbhaiMJ. Unauthorized use, reproduction, or commercial display of the content is strictly prohibited without proper authorization.
Call to Action
Enjoy the video and don't forget to like, share, and subscribe for more anime and manga content!
Remember, a good YouTube video description provides context about the video, includes relevant keywords to help users find your video, and encourages viewers to engage with your content.
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
                "title": "Awakening Destiny: Mo Xiu's Journey to the Unknown | | Part - 1 | | MokBhaiMJ",
                "description": description,
                "tags": ["#animerecap", "#manhwaedit", "#anime", "#animerecommendations", "#manhwarecommendation", "#manga", "#mangaunboxing", "#mangacollection", "#webtoon", "#manhwarecap", "#anime", "#animerecap"],
                "categoryId": "1"
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

if __name__ == '__main__':
    youtube = get_authenticated_service()
    initialize_upload(youtube)
