import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config.config import YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES, YOUTUBE_API_VERSION

def get_youtube_service():
    """
    Authenticate and create a YouTube API service.
    Returns:
        googleapiclient.discovery.Resource: Authenticated YouTube API service
    """
    creds = None
    pickle_file = 'youtube.pickle'

    # Load credentials from pickle file if it exists
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save credentials for future use
        with open(pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', YOUTUBE_API_VERSION, credentials=creds) 