import os
import pickle
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.errors import HttpError
from requests import Request # type: ignore
from google.auth.transport.requests import Request

VIDEO_FILE = "son-p3_with_subtitles"
CLIENT_SECRETS_FILE = "../google_sec.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

description = """
Awakening Destiny: Mo Xiu's Journey to the Unknown Part - 1

In the face of impending death, an ordinary man chooses an extraordinary path. 'The Unlikely Exorcist: A Countdown to Immortality' is a riveting tale of a terminally ill patient who, instead of succumbing to his fate, embarks on a thrilling journey of exorcism and immortal punishment. Not driven by a noble cause or the desire to protect his country, but lured by the irresistible temptation of risk salary and compensation. As he navigates through this uncharted territory, he encounters a world beyond his wildest imagination. Will he defy the odds and cheat death? Or will he become another pawn in the game of immortality? Dive into this captivating saga to uncover the truth.
This new title and description aim to pique the curiosity of potential readers by highlighting the unique premise of the story and the protagonist's unusual motivation. The description also poses questions that readers might be eager to find the answers to, further encouraging them to read the book.

Playlist: 

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
                "title": "The Unlikely Exorcist: A Countdown to Immortality",
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
