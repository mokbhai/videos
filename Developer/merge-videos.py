import argparse
import datetime
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips # type: ignore

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+', help="Input files to be merged")
    return parser.parse_args()

def merge_videos(files):
    clips = [VideoFileClip(f + ".mp4") for f in files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(files[0] + "_merged.mp4")

def merge_vtt_files(files):
    time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})")
    time_format = "%H:%M:%S.%f"
    lines = []
    last_timestamp = None

    for file in files:
        with open(file + ".vtt", 'r') as f:
            file_lines = f.readlines()
            if lines:
                file_lines = file_lines[3:]

            for i, line in enumerate(file_lines):
                match = time_pattern.search(line)
                if match:
                    start = datetime.datetime.strptime(match.group(1), time_format)
                    end = datetime.datetime.strptime(match.group(2), time_format)
                    if last_timestamp:
                        start += last_timestamp
                        end += last_timestamp
                    file_lines[i] = line.replace(match.group(0), f"{start.strftime(time_format)[:-3]} --> {end.strftime(time_format)[:-3]}")
                    last_timestamp = end - start

            lines += file_lines

    with open('merged.vtt', 'w') as f:
        f.writelines(lines)

def main():
    args = parse_args()
    # video_files = [f for f in args.files if f.endswith('.mp4')]
    # vtt_files = [f for f in args.files if f.endswith('.vtt')]

    # if video_files:
    #     merge_videos(video_files)
    # if vtt_files:
    #     merge_vtt_files(vtt_files)

    files = args.files
    merge_videos(files)
    merge_vtt_files(files)


if __name__ == "__main__":
    main()
