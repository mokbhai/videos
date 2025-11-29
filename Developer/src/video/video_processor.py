import os
import argparse
from typing import Optional, List, Tuple
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from ..utils.media_utils import extract_frames, merge_videos
from config.config import VIDEOS_DIR, AUDIO_DIR

class VideoProcessor:
    @staticmethod
    def extract_audio(
        video_path: str,
        output_path: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> None:
        """
        Extract audio from video.
        
        Args:
            video_path (str): Path to video file
            output_path (str): Path to save audio file
            start_time (float, optional): Start time in seconds
            end_time (float, optional): End time in seconds
        """
        video = VideoFileClip(video_path)
        audio = video.audio
        
        if start_time is not None or end_time is not None:
            audio = audio.subclip(start_time, end_time)
            
        audio.write_audiofile(output_path)
        video.close()
        audio.close()

    @staticmethod
    def add_audio_to_video(
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> None:
        """
        Add audio to video.
        
        Args:
            video_path (str): Path to video file
            audio_path (str): Path to audio file
            output_path (str): Path to save output video
        """
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        final_video = video.set_audio(audio)
        final_video.write_videofile(output_path)
        
        video.close()
        audio.close()
        final_video.close()

    @staticmethod
    def trim_video(
        video_path: str,
        output_path: str,
        start_time: float,
        end_time: Optional[float] = None
    ) -> None:
        """
        Trim video to specified duration.
        
        Args:
            video_path (str): Path to video file
            output_path (str): Path to save trimmed video
            start_time (float): Start time in seconds
            end_time (float, optional): End time in seconds
        """
        video = VideoFileClip(video_path)
        trimmed = video.subclip(start_time, end_time)
        trimmed.write_videofile(output_path)
        
        video.close()
        trimmed.close()

    @staticmethod
    def extract_frames_to_dir(
        video_path: str,
        output_dir: str,
        fps: int = 1
    ) -> List[str]:
        """
        Extract frames from video to directory.
        
        Args:
            video_path (str): Path to video file
            output_dir (str): Directory to save frames
            fps (int, optional): Frames per second to extract
            
        Returns:
            List[str]: List of paths to extracted frames
        """
        return extract_frames(video_path, output_dir, fps)

    @staticmethod
    def merge_video_list(
        video_paths: List[str],
        output_path: str,
        fps: int = 30
    ) -> None:
        """
        Merge multiple videos into one.
        
        Args:
            video_paths (List[str]): List of video file paths
            output_path (str): Path to save merged video
            fps (int, optional): Frames per second
        """
        merge_videos(video_paths, output_path, fps)

def main():
    parser = argparse.ArgumentParser(description='Video processing tools')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Extract audio command
    extract_parser = subparsers.add_parser('extract-audio', help='Extract audio from video')
    extract_parser.add_argument('video', help='Input video name')
    extract_parser.add_argument('--output', help='Output audio name')
    extract_parser.add_argument('--start', type=float, help='Start time in seconds')
    extract_parser.add_argument('--end', type=float, help='End time in seconds')
    
    # Add audio command
    add_parser = subparsers.add_parser('add-audio', help='Add audio to video')
    add_parser.add_argument('video', help='Input video name')
    add_parser.add_argument('audio', help='Input audio name')
    add_parser.add_argument('--output', help='Output video name')
    
    # Trim video command
    trim_parser = subparsers.add_parser('trim', help='Trim video')
    trim_parser.add_argument('video', help='Input video name')
    trim_parser.add_argument('--output', help='Output video name')
    trim_parser.add_argument('--start', type=float, required=True, help='Start time in seconds')
    trim_parser.add_argument('--end', type=float, help='End time in seconds')
    
    # Merge videos command
    merge_parser = subparsers.add_parser('merge', help='Merge multiple videos')
    merge_parser.add_argument('videos', nargs='+', help='Input video names')
    merge_parser.add_argument('--output', required=True, help='Output video name')
    merge_parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    
    args = parser.parse_args()
    
    if args.command == 'extract-audio':
        video_path = os.path.join(VIDEOS_DIR, args.video)
        if not video_path.endswith('.mp4'):
            video_path += '.mp4'
            
        output_path = os.path.join(AUDIO_DIR, args.output or f"{os.path.splitext(args.video)[0]}.mp3")
        if not output_path.endswith('.mp3'):
            output_path += '.mp3'
            
        VideoProcessor.extract_audio(video_path, output_path, args.start, args.end)
        
    elif args.command == 'add-audio':
        video_path = os.path.join(VIDEOS_DIR, args.video)
        if not video_path.endswith('.mp4'):
            video_path += '.mp4'
            
        audio_path = os.path.join(AUDIO_DIR, args.audio)
        if not audio_path.endswith('.mp3'):
            audio_path += '.mp3'
            
        output_path = os.path.join(VIDEOS_DIR, args.output or f"{os.path.splitext(args.video)[0]}_with_audio.mp4")
        if not output_path.endswith('.mp4'):
            output_path += '.mp4'
            
        VideoProcessor.add_audio_to_video(video_path, audio_path, output_path)
        
    elif args.command == 'trim':
        video_path = os.path.join(VIDEOS_DIR, args.video)
        if not video_path.endswith('.mp4'):
            video_path += '.mp4'
            
        output_path = os.path.join(VIDEOS_DIR, args.output or f"{os.path.splitext(args.video)[0]}_trimmed.mp4")
        if not output_path.endswith('.mp4'):
            output_path += '.mp4'
            
        VideoProcessor.trim_video(video_path, output_path, args.start, args.end)
        
    elif args.command == 'merge':
        video_paths = [os.path.join(VIDEOS_DIR, v) for v in args.videos]
        video_paths = [v if v.endswith('.mp4') else v + '.mp4' for v in video_paths]
        
        output_path = os.path.join(VIDEOS_DIR, args.output)
        if not output_path.endswith('.mp4'):
            output_path += '.mp4'
            
        VideoProcessor.merge_video_list(video_paths, output_path, args.fps)

if __name__ == '__main__':
    main() 