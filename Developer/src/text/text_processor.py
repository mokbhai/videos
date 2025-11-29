import os
import argparse
import asyncio
import re
import edge_tts
from typing import Optional
from ..utils.media_utils import create_video_from_images, get_media_files
from config.config import (
    TEXT_DIR,
    AUDIO_DIR,
    IMAGES_DIR,
    VIDEOS_DIR,
    DEFAULT_VOICE,
    SUPPORTED_IMAGE_EXTENSIONS
)

class TextToVideoConverter:
    def __init__(
        self,
        voice: str = DEFAULT_VOICE,
        fps: int = 3
    ):
        self.voice = voice
        self.fps = fps

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text
        """
        # Remove common unwanted phrases
        text = text.replace('Save Bookmark', ' ')
        text = text.replace('front pagePC versionbookshelf', ' ')
        text = text.replace('returnfront page', ' ')
        text = text.replace('Turn off the lightsEye protection', ' ')
        text = text.replace('TraditionalbigmiddleSmall', ' ')
        
        # Replace newlines with spaces
        text = text.replace('\n', ' ')
        
        # Replace double quotes with single quotes
        text = text.replace('"', "'")
        
        # Remove multiple spaces
        text = re.sub(' +', ' ', text)
        
        return text.strip()

    async def generate_audio(
        self,
        text: str,
        output_audio_path: str,
        output_subtitle_path: Optional[str] = None
    ) -> None:
        """
        Generate audio from text using edge-tts.
        
        Args:
            text (str): Input text
            output_audio_path (str): Path to save audio file
            output_subtitle_path (str, optional): Path to save subtitle file
        """
        communicate = edge_tts.Communicate(text, self.voice)
        submaker = edge_tts.SubMaker()

        # Generate audio
        with open(output_audio_path, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

        # Generate subtitles if path provided
        if output_subtitle_path:
            with open(output_subtitle_path, "w", encoding="utf-8") as file:
                file.write(submaker.generate_subs())

    def create_video(
        self,
        audio_path: str,
        output_path: str,
        image_dir: str = IMAGES_DIR
    ) -> None:
        """
        Create video from audio and images.
        
        Args:
            audio_path (str): Path to audio file
            output_path (str): Path to save video file
            image_dir (str, optional): Directory containing images
        """
        # Get all images
        image_paths = get_media_files(image_dir, SUPPORTED_IMAGE_EXTENSIONS)
        if not image_paths:
            raise ValueError(f"No images found in {image_dir}")

        # Create video
        video = create_video_from_images(
            image_paths=image_paths,
            audio_path=audio_path,
            fps=self.fps
        )

        # Write video file
        video.write_videofile(output_path, fps=self.fps)
        video.close()

async def main():
    parser = argparse.ArgumentParser(description='Convert text to video')
    parser.add_argument('--name', required=True, help='Output name for files')
    parser.add_argument('--voice', default=DEFAULT_VOICE, help='Voice to use')
    parser.add_argument('--fps', type=int, default=3, help='Frames per second')
    
    args = parser.parse_args()
    
    # Setup paths
    text_path = os.path.join(TEXT_DIR, 'data.txt')
    audio_path = os.path.join(AUDIO_DIR, f"{args.name}.mp3")
    subtitle_path = os.path.join(AUDIO_DIR, f"{args.name}.vtt")
    video_path = os.path.join(VIDEOS_DIR, f"{args.name}.mp4")
    
    # Create converter
    converter = TextToVideoConverter(voice=args.voice, fps=args.fps)
    
    # Read and clean text
    with open(text_path, 'r', encoding='utf-8') as file:
        text = converter._clean_text(file.read())
    
    # Generate audio and subtitles
    await converter.generate_audio(
        text=text,
        output_audio_path=audio_path,
        output_subtitle_path=subtitle_path
    )
    
    # Create video
    converter.create_video(
        audio_path=audio_path,
        output_path=video_path
    )
    
    print(f"Video created successfully: {video_path}")

if __name__ == '__main__':
    asyncio.run(main())