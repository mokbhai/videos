# ffmpeg -stream_loop 3 -i ../canva/outputvideo_hd.mp4 -i ../Audio/otaku-p1.mp3 -vf "subtitles=../Videos/otaku-p1.vtt:force_style='Alignment=10,PrimaryColour=&H000FFFFF'" -map 0:v -map 1:a -c:v libx264 -crf 23 -c:a aac -shortest ../Videos/my_video_with_subtitles.mp4

import argparse
import os
import subprocess

# Define paths
video_path = '../canva/outputvideo_hd.mp4'
audio_dir = "../Audio/"
out_path = "../Videos/"

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name for the output files")
args = parser.parse_args()
NAME = args.name

if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

audio_path = os.path.join(audio_dir, NAME + '.mp3')
output_video_with_subtitles_path = os.path.join(out_path, NAME + '_with_subtitles.mp4')
subtitle_file = os.path.join(out_path, NAME + '.vtt')

# Get durations using FFmpeg
def get_duration(file_path):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

video_duration = get_duration(video_path)
audio_duration = get_duration(audio_path)

# If audio is longer than video, calculate the number of loops needed
loops = int(audio_duration // video_duration) + 1 if audio_duration > video_duration else 1

# Combine video and audio, loop video if necessary, and add subtitles in one go
subprocess.run([
    'ffmpeg', '-stream_loop', str(loops), '-i', video_path, '-i', audio_path, '-vf', f"subtitles={subtitle_file}:force_style='Alignment=10,PrimaryColour=&H000FFFFF'", 
    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-shortest', output_video_with_subtitles_path
])

print(f"Output video with subtitles saved to {output_video_with_subtitles_path}")
