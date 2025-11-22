import sys
import os
from PIL import Image, ImageSequence

def resize_gif(input_path, output_path, size=(165, 72), rotate=False):
    with Image.open(input_path) as im:
        frames = []
        durations = []
        disposals = []
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert("RGBA")
            if rotate:
                frame = frame.rotate(-90, expand=True)  # -90 = clockwise
            frame = frame.resize(size, Image.Resampling.LANCZOS)
            frames.append(frame)
            durations.append(frame.info.get("duration", 100))
            disposals.append(frame.info.get("disposal", 2))


        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=im.info.get("loop", 0),
            duration=durations,
            disposal=disposals,
            optimize=False,
        )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gif.py input.gif [output.gif] [--rotate]")
        sys.exit(1)

    input_file = sys.argv[1]
    rotate_flag = "--rotate" in sys.argv

    # Handle optional output file argument
    if len(sys.argv) >= 3 and sys.argv[2] != "--rotate":
        output_file = sys.argv[2]
    else:
        base, ext = os.path.splitext(input_file)
        suffix = "_rotated_resized" if rotate_flag else "_resized"
        output_file = f"{base}{suffix}{ext}"

    resize_gif(input_file, output_file, rotate=rotate_flag)
    print(f"Resized GIF saved to {output_file}")
