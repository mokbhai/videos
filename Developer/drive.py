import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tqdm import tqdm
import mimetypes

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = "../google_sec.json"

class TqdmUploadCallback(MediaFileUpload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progressbar = tqdm(total=100)

    def progress(self):
        self.progressbar.update(super().progress() * 100)  # Call the superclass's progress method

    def __del__(self):
        self.progressbar.close()


def get_file_type(file_path):
    return mimetypes.guess_type(file_path)[0]


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
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
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Call the Drive v3 API
    service = build('drive', 'v3', credentials=creds)

    file_name = input("File name: ")
    
    # Upload a video file
    file_metadata = {'name': file_name, 'mimeType': 'video/mp4'}

    # file_metadata = {'name': 'every-one-has-4-skills.mp3', 'mimeType': 'audio/mpeg'}
    
    # file_metadata = {'name': '8.png', 'mimeType': 'image/png'}

    media = TqdmUploadCallback('../Videos/' + file_name, mimetype='video/mp4', resumable=True)

    # media = TqdmUploadCallback('../Audio/every-one-has-4-skills.mp3', mimetype='audio/mpeg', resumable=True)

    # media = TqdmUploadCallback('../Images/8.png', mimetype='image/png', resumable=True)


    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    main()
