import argparse
import asyncio
import re
import edge_tts  # type: ignore
from tqdm import tqdm # type: ignore

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name for the output files")
args = parser.parse_args()

NAME = args.name

with open('../Text/output.txt', 'r') as file:
    TEXT = file.read()

VOICE = "en-US-GuyNeural"

OUTPUT_FILE = "../Audio/" + NAME + ".mp3"
WEBVTT_FILE = "../Audio/" + NAME + ".vtt"

async def amain() -> None:
    """Main function"""
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
        if (line == 'WEBVTT\n'): continue
        srt_content.append(line)

    srt_file_path = re.sub('.vtt$', '.srt', vtt_file_path)
    with open(srt_file_path, 'w') as srt_file:
        srt_file.writelines(srt_content)

    print(f'SRT file has been saved to {srt_file_path}')

if __name__ == "__main__":
    asyncio.run(amain())
