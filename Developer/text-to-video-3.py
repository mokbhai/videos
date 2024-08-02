# ffmpeg -i inputvideo.mp4 -vf "scale=1280:720,fps=30" -c:v libx264 -crf 23 outputvideo_hd.mp4

import argparse
import asyncio
import re
import edge_tts  # type: ignore
from tqdm import tqdm  # type: ignore
import os
import subprocess

# Define paths
video_path = '../canva/outputvideo_hd.mp4'
audio_dir = "../Audio/"
out_path = "../Videos/"
text_file = '../Text/output.txt'

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

# Read text from file
with open(text_file, 'r') as file:
    TEXT = file.read()

VOICE = "en-US-GuyNeural"
OUTPUT_FILE = audio_path
WEBVTT_FILE = subtitle_file

async def generate_audio_and_subtitles():
    """Generate audio and subtitles from text."""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    submaker = edge_tts.SubMaker()
    pbar = tqdm(total=len(TEXT))  # Initialize the progress bar

    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
            if "text" in chunk:  # Check if the "text" key exists
                pbar.update(len(chunk["text"]))  # Update the progress bar

    pbar.close()  # Close the progress bar

    with open(WEBVTT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())

    # Convert VTT to SRT
    vtt_to_srt(WEBVTT_FILE)

def vtt_to_srt(vtt_file_path):
    """Convert VTT subtitle file to SRT format."""
    with open(vtt_file_path, 'r') as vtt_file:
        vtt_content = vtt_file.readlines()

    srt_content = []
    srt_index = 1
    for line in vtt_content:
        if '-->' in line:
            # Convert timestamp format from VTT to SRT
            line = re.sub(r'(\d{2}):(\d{2}):(\d{2}).(\d{3})', r'\1:\2:\3,\4', line)
            srt_content.append(str(srt_index) + '\n')
            srt_index += 1
        if line == 'WEBVTT\n':
            continue
        srt_content.append(line)

    srt_file_path = re.sub('.vtt$', '.srt', vtt_file_path)
    with open(srt_file_path, 'w') as srt_file:
        srt_file.writelines(srt_content)

    print(f'SRT file has been saved to {srt_file_path}')

def get_duration(file_path):
    """Get the duration of a media file using ffprobe."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def combine_video_audio_subtitles():
    """Combine video, audio, and subtitles into a single video file."""
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

if __name__ == "__main__":
    asyncio.run(generate_audio_and_subtitles())
    combine_video_audio_subtitles()