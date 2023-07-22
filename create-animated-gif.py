import os
import sys
from PIL import Image

def create_animated_gif(png_folder, gif_filename, duration=100):
    # Get a list of all PNG files in the folder
    png_files = [file for file in os.listdir(png_folder) if file.endswith('.png')]

    # Sort the files alphabetically (assuming that the files are named in sequential order)
    png_files.sort()

    # Create a list to store the images for the animated GIF
    images = []

    # Open each PNG file and append it to the images list
    for png_file in png_files:
        image_path = os.path.join(png_folder, png_file)
        image = Image.open(image_path)
        images.append(image)

    # Save the images as an animated GIF
    images[0].save(gif_filename, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)

if __name__ == "__main__":
    # Check if required command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python create_animated_gif.py <png_folder> <gif_filename>")
        print("Example: python create_animated_gif.py HuePagesRendered animated.gif")
        sys.exit(1)

    # Get the command-line arguments
    png_folder = sys.argv[1]
    gif_filename = sys.argv[2]

    # Check if the specified folder exists
    if not os.path.exists(png_folder):
        print(f"Error: The folder '{png_folder}' does not exist.")
        sys.exit(1)

    create_animated_gif(png_folder, gif_filename)
    print(f"Animated GIF '{gif_filename}' created successfully.")
