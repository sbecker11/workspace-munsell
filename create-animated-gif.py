import os
import sys
from PIL import Image

def replace_transparent_with_grey(image):
    # Convert the image to RGBA mode (if not already) to handle alpha transparency
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Get the alpha channel from the image
    alpha = image.split()[-1]

    # Create a new image with a grey background
    new_image = Image.new('RGBA', image.size, (128, 128, 128, 255))

    # Composite the original image over the grey background using alpha
    new_image.paste(image, mask=alpha)

    return new_image

def create_animated_gif(png_folder, gif_filename, duration=100, replace_transparent=False):
    # Get a list of all PNG files in the folder
    png_files = [file for file in os.listdir(png_folder) if file.endswith('.png')]

    # Sort the files alphabetically (assuming that the files are named in sequential order)
    png_files.sort()

    # Create a list to store the images for the animated GIF
    images = []

    # Open each PNG file, apply transparency replacement (if enabled), and append it to the images list
    for png_file in png_files:
        image_path = os.path.join(png_folder, png_file)
        print(f"Loading image: {image_path}")
        image = Image.open(image_path)

        if replace_transparent:
            image = replace_transparent_with_grey(image)

        images.append(image)

    # Check if the gif_filename has the ".gif" extension
    if not gif_filename.lower().endswith('.gif'):
        print("Error: The output filename must have the '.gif' extension.")
        sys.exit(1)

    # Save the images as an animated GIF
    images[0].save(gif_filename, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)

if __name__ == "__main__":
    # Check if required command-line arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python create_animated_gif.py <png_folder> <gif_filename> [--replace_transparent_with_grey]")
        print("Example: python create_animated_gif.py HuePagesRendered animated.gif --replace_transparent_with_grey")
        sys.exit(1)

    # Get the command-line arguments
    png_folder = sys.argv[1]
    gif_filename = sys.argv[2]

    # Check if the specified folder exists
    if not os.path.exists(png_folder):
        print(f"Error: The folder '{png_folder}' does not exist.")
        sys.exit(1)

    # Check if the "--replace_transparent_with_grey" flag is provided
    replace_transparent = "--replace_transparent_with_grey" in sys.argv

    create_animated_gif(png_folder, gif_filename, replace_transparent=replace_transparent)
    print(f"Animated GIF '{gif_filename}' created successfully.")
