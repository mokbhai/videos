from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.errors import HttpError # type: ignore

VIDEO_FILE = "126"
chapters = "126 to 116"
CLIENT_SECRETS_FILE = "client_secret_429738725753-74dha38siq6q1fhjh8adf5945j0arqtp.apps.googleusercontent.com.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

description = f"""
In this video, we continue the exciting journey of 'My Grandfather Became a General in Another World and I am invincible in the city!' with chapters '{chapters}'. Stay tuned as more parts are coming soon!

Playlist: https://youtube.com/playlist?list=PL_W6A9WF_sWjuO-F8UFDlJWuxz-BRlVFC&si=CRoOTaM-onHt_XDG

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
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build('youtube', 'v3', credentials=credentials)

def initialize_upload(youtube):
    media = MediaFileUpload("./Videos/" + VIDEO_FILE + ".mp4", 
                            mimetype='video/mp4', 
                            resumable=True,
                            chunksize=-1)  # maximum chunk size
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Chapter " + VIDEO_FILE + " My Grandfather Became a General in Another World and I am invincible in the city! | | MJ",
                "description": description,
                "tags": ["#animerecap", "#manhwaedit", "#anime", "#animerecommendations", "#manhwarecommendation", "#manga", "#mangaunboxing", "#mangacollection", "#webtoon", "#manhwarecap", "#anime", "#animerecap"],
                "categoryId": "1"
            },
            "status": {
                "privacyStatus": "public"
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
