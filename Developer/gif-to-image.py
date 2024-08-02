from PIL import Image
from tqdm import tqdm
import os

def gif_to_images(gif_path, output_path):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    frame = Image.open(gif_path)
    nframes = 0
    total_frames = frame.n_frames
    with tqdm(total=total_frames) as pbar:
        while frame:
            frame.save('%s/%s-%s.png' % (output_path, gif_path.split('/')[-1], nframes ), 'PNG')
            nframes += 1
            pbar.update(1)
            try:
                frame.seek( nframes )
            except EOFError:
                break
    return True


gif = "../Gifs/" + "1.gif"
out = "../Images/" + "1"

# Use the function like this:
gif_to_images(gif, out)
