from moviepy.editor import * # type: ignore
import random
import os

audioFile =  "video"
fps = 3

audio_dir = "../Audio/"
images_dir = "../Images/imgs/"
out_path = "../Videos/"

# Load your audio file
audio = AudioFileClip(audio_dir + audioFile + ".mp3") # type: ignore

images = [img for img in os.listdir(images_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]

# # Randomize the order of the images
# random.shuffle(images)

clips = []
for image in images:
    image_path = os.path.join(images_dir, image)
    clip = ImageClip(image_path) # type: ignore
    clip = clip.set_duration(audio.duration / len(images))  # Set duration for each clip
    clips.append(clip)


# Concatenate images and set the duration of each image to the duration of the audio divided by the number of images
concat_clip = concatenate_videoclips(clips) # type: ignore

# Combine audio and images
video = concat_clip.set_audio(audio)

# Write the result to a file
video.write_videofile(out_path + audioFile + ".mp4", fps=fps) # fps specifies the frames per second


# Define the source file and destination path
source_file = audio_dir + audioFile + ".vtt"
destination_file = out_path + audioFile + ".vtt"

# Use the os.rename function to move the file
# os.rename(source_file, destination_file)
# os.unlink(audio_dir + audioFile + ".mp3")
# os.unlink(audio_dir + audioFile + ".vtt")
