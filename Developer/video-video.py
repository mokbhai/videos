import argparse
import os
import ffmpeg

# Define paths
video_path = '../canva/otaku-p1.mp4'
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
output_path = os.path.join(out_path, NAME + '.mp4')

# Get durations using ffmpeg
def get_duration(file_path):
    probe = ffmpeg.probe(file_path)
    return float(probe['format']['duration'])

video_duration = get_duration(video_path)
audio_duration = get_duration(audio_path)

# If audio is longer than video, loop video
if audio_duration > video_duration:
    loops = int(audio_duration // video_duration) + 1
    looped_video_path = os.path.join(out_path, 'looped_video.mp4')
    (
        ffmpeg
        .input(video_path, stream_loop=loops - 1)
        .output(looped_video_path, c='copy')
        .run()
    )
    video_path = looped_video_path

# Combine video and audio
(
    ffmpeg
    .input(video_path)
    .input(audio_path)
    .output(output_path, c_v='copy', c_a='aac', strict='experimental')
    .run()
)
