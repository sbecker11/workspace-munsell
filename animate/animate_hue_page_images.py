import os
import sys
from PIL import Image

def replace_transparent_with_color(image, color):
    # Convert the image to RGBA mode (if not already) to handle alpha transparency
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Get the alpha channel from the image
    alpha = image.split()[-1]

    # Create a new image with the specified background color
    new_image = Image.new('RGBA', image.size, color)

    # Composite the original image over the new background using alpha
    new_image.paste(image, mask=alpha)

    return new_image

def create_animated_gif(png_folder, gif_filename, duration=100, bg=-1, scale=100):
    # Get a list of all PNG files in the folder
    png_files = [file for file in os.listdir(png_folder) if file.endswith('.png')]

    # Sort the files alphabetically (assuming that the files are named in sequential order)
    png_files.sort()

    # Create a list to store the images for the animated GIF
    images = []

    # Open each PNG file, replace the background (if required), and append it to the images list
    for png_file in png_files:
        image_path = os.path.join(png_folder, png_file)
        print(f"Loading image: {image_path}")
        image = Image.open(image_path)

        # Replace transparent background with the specified color (if bg is between 0 and 255)
        if 0 <= bg <= 255:
            background_color = (bg, bg, bg, 255)
            image = replace_transparent_with_color(image, background_color)

        # Scale the image by the given percentage
        if scale != 100:
            new_width = int(image.width * scale / 100)
            new_height = int(image.height * scale / 100)
            image = image.resize((new_width, new_height), Image.LANCZOS)

        images.append(image)

    # Check if the gif_filename has the ".gif" extension
    if not gif_filename.lower().endswith('.gif'):
        print("Error: The output filename must have the '.gif' extension.")
        sys.exit(1)

    # Save the images as an animated GIF
    with open(gif_filename, 'wb') as f:
        for idx, image in enumerate(images):
            # Output the dimensions of each frame
            frame_width, frame_height = image.size
            print(f"Frame {idx+1}: {frame_width}x{frame_height}")

        # Save all frames as an animated GIF
        images[0].save(f, save_all=True, append_images=images[1:], optimize=True, duration=duration, loop=0)

    print(f"Animated GIF '{gif_filename}' created successfully.")

if __name__ == "__main__":
    # Check if required command-line arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python animate_hue_page_images.py <png_folder> <gif_filename> [--bg <0-255>] [--scale <percentage>]")
        print("Example: python animate_hue_page_images.py excel_file_long/hue_page_images excel_file_long/hue_pages_animated.gif --bg 128 --scale 50")
        print("Example: python animate_hue_page_images.py excel_file_macro/hue_page_images excel_file_macro/hue_pages_animated.gif --bg 128 --scale 50")
        sys.exit(1)

    # Get the command-line arguments
    png_folder = sys.argv[1]
    gif_filename = sys.argv[2]

    # Check if the specified folder exists
    if not os.path.exists(png_folder):
        print(f"Error: The folder '{png_folder}' does not exist.")
        sys.exit(1)

    # Extract optional parameters
    bg = -1
    scale = 100
    if "--bg" in sys.argv:
        bg_index = sys.argv.index("--bg") + 1
        if bg_index < len(sys.argv):
            bg = int(sys.argv[bg_index])
            if not (0 <= bg <= 255):
                print("Error: The background color must be between 0 and 255.")
                sys.exit(1)
        else:
            print("Error: Missing value for --bg option.")
            sys.exit(1)

    if "--scale" in sys.argv:
        scale_index = sys.argv.index("--scale") + 1
        if scale_index < len(sys.argv):
            scale = int(sys.argv[scale_index])
            if scale <= 0:
                print("Error: The scale percentage must be greater than 0.")
                sys.exit(1)
        else:
            print("Error: Missing value for --scale option.")
            sys.exit(1)

    create_animated_gif(png_folder, gif_filename, duration=100, bg=bg, scale=scale)
    print(f"Animated GIF '{gif_filename}' created successfully.")
