fps = 6

audio_dir = "../Audio/"
images_dir = "../Images/1/"
out_path = "../Videos/"

import argparse
import os
import random
import asyncio
import re
import edge_tts  
from moviepy.editor import *  
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
import ffmpeg

if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)
if not os.path.exists(out_path):
    os.makedirs(out_path)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name for the output files")
args = parser.parse_args()

NAME = args.name

with open('../Text/output.txt', 'r') as file:
    TEXT = file.read()

# Check if the text is empty
if not TEXT.strip():
    raise ValueError("The file is empty.")

# TEXT = TEXT.replace('Save Bookmark', ' ')
# TEXT = TEXT.replace('front pagePC versionbookshelf', ' ')
# TEXT = TEXT.replace('returnfront page', ' ')
# TEXT = TEXT.replace('Turn off the lightsEye protection', ' ')
# TEXT = TEXT.replace('TraditionalbigmiddleSmall', ' ')
# TEXT = TEXT.replace('My grandpa rebelled in another world, and I am invincible in the city!', ' ')

# TEXT = TEXT.replace('\n', ' ')
TEXT = TEXT.replace('"', "'")
TEXT = TEXT.replace(',', "")
TEXT = re.sub(' +', ' ', TEXT)

VOICE = "en-US-GuyNeural"

OUTPUT_FILE = audio_dir + NAME + ".mp3"
WEBVTT_FILE = audio_dir + NAME + ".vtt"

async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    submaker = edge_tts.SubMaker()
    pbar = tqdm(total=len(TEXT))
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
                if "data" in chunk:  # Check if the "data" key exists
                    pbar.update(len(chunk["data"]))  # Update the progress bar
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    pbar.close()
    with open(WEBVTT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())

if __name__ == "__main__":
    asyncio.run(amain())

# Load your audio file
print(f"Loading audio file: {NAME}.mp3")
audio = AudioFileClip(audio_dir + NAME + ".mp3")  # type: ignore

images = [img for img in os.listdir(images_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]

# Randomize the order of the images
# random.shuffle(images)

def process_image(image_path):
    clip = ImageClip(image_path)  # type: ignore
    clip = clip.set_duration(5)  # Set duration for each clip to 5 seconds
    return clip

# Use ThreadPoolExecutor to parallelize image processing
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_image, os.path.join(images_dir, image)) for image in images]
    clips = [future.result() for future in futures]

# Cycle through the images until the audio duration is reached
final_clips = []
time = 0
for clip in cycle(clips):
    if time + 5 > audio.duration:
        clip = clip.set_duration(audio.duration-time)  # If the remaining duration is less than 5 seconds, set that as the duration
    final_clips.append(clip)
    time += 5
    if time >= audio.duration:
        break

# Concatenate images and set the duration of each image to the duration of the audio divided by the number of images
concat_clip = concatenate_videoclips(final_clips)  # type: ignore

# Combine audio and images
video = concat_clip.set_audio(audio)

# Write the result to a file
print("Writing video file...")
video.write_videofile(out_path + NAME + ".mp4", fps=fps, threads=4)  # Use 4 threads for writing the video
print("Finished writing video file.")

# Define the source file and destination path
source_file = audio_dir + NAME + ".vtt"
destination_file = out_path + NAME + ".vtt"

# Use the os.rename function to move the file and delete them
os.rename(source_file, destination_file)
# os.unlink(OUTPUT_FILE)
# os.unlink(WEBVTT_FILE)

input_file = out_path + NAME + ".mp4"
output_file = out_path + NAME + "_with_subtitles.mp4"
subtitle_file = out_path + NAME + ".vtt"

ffmpeg.input(input_file).output(output_file, vf='subtitles=' + subtitle_file + ':force_style=\'Alignment=10,PrimaryColour=&H000FFFFF\'').run()
