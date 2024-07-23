from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import random
import os

NAME = '561-6000-granpa'
# Load the audio file
audio = AudioFileClip(NAME + '.mp3')

# Load the video files
video_files = [video for video in os.listdir("./canva/") if video.endswith(('.mp4'))]

videos = []

for vf in video_files:
    video = VideoFileClip("./canva/" + vf)
    
    # Check if the video's resolution is below 1080p
    if video.size[1] < 1080:
        # Upscale the video to 1080p
        video = video.resize(height=1080)
    
    videos.append(video)

# Shuffle the videos
random.shuffle(videos)

# Concatenate the videos
video = concatenate_videoclips(videos)

# Get the duration of the audio and video
audio_duration = audio.duration
video_duration = video.duration

# If the total video length is shorter than the audio, loop the videos
if video_duration < audio_duration:
    loops = int(audio_duration // video_duration) + 1
    video = concatenate_videoclips([video]*loops)

# If the audio length is shorter than the video, cut the video to match the audio length
if audio_duration < video_duration:
    video = video.subclip(0, audio_duration)

# Set the audio of the video clip to our audio
video = video.set_audio(audio)
# video.write_videofile("./Videos/" + NAME + ".mp4", codec='libx264', audio_codec='aac', fps=24, bitrate="8000k")

# Load the subtitles
generator = lambda txt: TextClip(txt, font='Arial', fontsize=48, color='orange')
subtitles = SubtitlesClip(NAME + ".srt", generator)

# Overlay the subtitles on the video and set the position to center
final_video = CompositeVideoClip([video, subtitles.set_position('center')])

# Write the result to a file with resolution above or equal to 1080p
final_video.write_videofile("./Videos/" + NAME + ".mov", codec='libx264', audio_codec='aac', fps=24, bitrate="8000k", threads=4)
