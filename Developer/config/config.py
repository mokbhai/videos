import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "..", "Audio")
IMAGES_DIR = os.path.join(BASE_DIR, "..", "Images", "imgs")
VIDEOS_DIR = os.path.join(BASE_DIR, "..", "Videos")
TEXT_DIR = os.path.join(BASE_DIR, "..", "Text")

# Create directories if they don't exist
for directory in [AUDIO_DIR, IMAGES_DIR, VIDEOS_DIR, TEXT_DIR]:
    os.makedirs(directory, exist_ok=True)

# YouTube settings
YOUTUBE_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "..", "google_sec.json")
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
YOUTUBE_API_VERSION = 'v3'

# Video settings
DEFAULT_FPS = 3
DEFAULT_VIDEO_CATEGORY = "1"
DEFAULT_LANGUAGE = "en"
DEFAULT_VOICE = "en-US-GuyNeural"

# File extensions
SUPPORTED_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg')
SUPPORTED_VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov')
SUPPORTED_AUDIO_EXTENSIONS = ('.mp3', '.wav') 