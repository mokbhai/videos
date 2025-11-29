import os
import argparse
from typing import Optional, Dict, Any
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from ..utils.auth import get_youtube_service
from config.config import (
    VIDEOS_DIR,
    DEFAULT_LANGUAGE,
    DEFAULT_VIDEO_CATEGORY
)

class YouTubeUploader:
    def __init__(self):
        self.youtube = get_youtube_service()

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        privacy_status: str = "unlisted",
        language: str = DEFAULT_LANGUAGE,
        category_id: str = DEFAULT_VIDEO_CATEGORY,
        tags: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Upload a video to YouTube.
        
        Args:
            video_path (str): Path to video file
            title (str): Video title
            description (str): Video description
            privacy_status (str, optional): Privacy status (private/unlisted/public)
            language (str, optional): Video language
            category_id (str, optional): Video category ID
            tags (list, optional): List of video tags
            
        Returns:
            dict: YouTube API response
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True,
            chunksize=-1
        )

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id,
                "defaultLanguage": language
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        try:
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%")

            print("Upload Complete!")
            return response

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            raise

    def add_subtitles(
        self,
        video_id: str,
        subtitle_path: str,
        language: str = DEFAULT_LANGUAGE,
        name: str = "Subtitles"
    ) -> None:
        """
        Add subtitles to a YouTube video.
        
        Args:
            video_id (str): YouTube video ID
            subtitle_path (str): Path to subtitle file
            language (str, optional): Subtitle language
            name (str, optional): Name of the subtitle track
        """
        if not os.path.exists(subtitle_path):
            raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")

        subtitle_media = MediaFileUpload(
            subtitle_path,
            mimetype='text/vtt',
            resumable=True
        )

        body = {
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": name
            }
        }

        try:
            self.youtube.captions().insert(
                part="snippet",
                body=body,
                media_body=subtitle_media
            ).execute()
            print("Subtitles added successfully!")

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            raise

def main():
    parser = argparse.ArgumentParser(description='Upload video to YouTube')
    parser.add_argument('--video', required=True, help='Video file name')
    parser.add_argument('--title', help='Video title')
    parser.add_argument('--description', help='Video description')
    parser.add_argument('--privacy', default='unlisted', help='Privacy status')
    parser.add_argument('--subtitles', help='Path to subtitle file')
    
    args = parser.parse_args()
    
    video_path = os.path.join(VIDEOS_DIR, args.video)
    if not video_path.endswith('.mp4'):
        video_path += '.mp4'
    
    uploader = YouTubeUploader()
    
    # Upload video
    response = uploader.upload_video(
        video_path=video_path,
        title=args.title or os.path.splitext(args.video)[0],
        description=args.description or "",
        privacy_status=args.privacy
    )
    
    # Add subtitles if provided
    if args.subtitles and response:
        uploader.add_subtitles(
            video_id=response['id'],
            subtitle_path=args.subtitles
        )

if __name__ == '__main__':
    main() 