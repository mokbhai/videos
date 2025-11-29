import os
from typing import List, Tuple
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
from config.config import (
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_VIDEO_EXTENSIONS,
    SUPPORTED_AUDIO_EXTENSIONS,
    DEFAULT_FPS
)

def get_media_files(directory: str, extensions: Tuple[str, ...]) -> List[str]:
    """
    Get all media files with specified extensions from a directory.
    
    Args:
        directory (str): Directory path to search
        extensions (tuple): Tuple of file extensions to include
        
    Returns:
        List[str]: List of file paths
    """
    return [
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.lower().endswith(extensions)
    ]

def create_video_from_images(
    image_paths: List[str],
    audio_path: str = None,
    duration_per_image: float = None,
    fps: int = DEFAULT_FPS
) -> VideoFileClip:
    """
    Create a video from a list of images.
    
    Args:
        image_paths (List[str]): List of image file paths
        audio_path (str, optional): Path to audio file
        duration_per_image (float, optional): Duration for each image
        fps (int, optional): Frames per second
        
    Returns:
        VideoFileClip: The created video clip
    """
    # Load audio if provided
    audio = AudioFileClip(audio_path) if audio_path else None
    total_duration = audio.duration if audio else len(image_paths) * (duration_per_image or 3)
    
    # Create image clips
    image_clips = []
    duration = total_duration / len(image_paths)
    
    for img_path in image_paths:
        clip = ImageClip(img_path)
        clip = clip.set_duration(duration)
        image_clips.append(clip)
    
    # Concatenate clips
    video = concatenate_videoclips(image_clips)
    
    # Add audio if provided
    if audio:
        video = video.set_audio(audio)
    
    return video

def merge_videos(video_paths: List[str], output_path: str, fps: int = DEFAULT_FPS) -> None:
    """
    Merge multiple videos into one.
    
    Args:
        video_paths (List[str]): List of video file paths
        output_path (str): Output file path
        fps (int, optional): Frames per second
    """
    clips = [VideoFileClip(path) for path in video_paths]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, fps=fps)
    
    # Clean up
    for clip in clips:
        clip.close()
    final_clip.close()

def extract_frames(video_path: str, output_dir: str, fps: int = 1) -> List[str]:
    """
    Extract frames from a video file.
    
    Args:
        video_path (str): Path to video file
        output_dir (str): Directory to save frames
        fps (int, optional): Number of frames per second to extract
        
    Returns:
        List[str]: List of paths to extracted frames
    """
    os.makedirs(output_dir, exist_ok=True)
    video = VideoFileClip(video_path)
    frame_paths = []
    
    for t in range(0, int(video.duration), fps):
        frame = video.get_frame(t)
        frame_path = os.path.join(output_dir, f"frame_{t}.jpg")
        Image.fromarray(frame).save(frame_path)
        frame_paths.append(frame_path)
    
    video.close()
    return frame_paths 