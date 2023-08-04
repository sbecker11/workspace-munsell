import os
import pandas as pd
from PIL import Image, ImageDraw
import argparse
from munsell_data_frame import MunsellDataFrame
from munsell_data_frame.constants import PAGE_HUE_NAMES

chip_size = 75
chip_gap = 10

max_rows = None
max_cols = None

hue_page_image_width = None
hue_page_image_height = None

# find all rows with the given page_hue_name from munsell_df
# and return each row decorated with color_chip coordinates on the page_hue_image
def get_page_hue_rows(page_hue_name, munsell_df):
    selected_rows = munsell_df.filter_by_columns({'page_hue_name': page_hue_name })
    page_hue_rows = []
    rows = [item[1] for item in selected_rows.iterrows()]
    for row in rows:
        value_row = int(row['value_row'])
        chroma_column = int(row['chroma_column']) # Use .iloc[0] to get the first (and only) value as an integer
        row_idx = value_row - 1
        col_idx = chroma_column // 2 - 1
        x1 = chip_gap // 2 + col_idx * (chip_size + chip_gap)
        y1 = chip_gap // 2 + row_idx * (chip_size + chip_gap) 
        
        assert (x1 >= chip_gap // 2), "x1 out of range"
        assert (y1 >= chip_gap // 2), "y1 out of range"
        x2 = x1 + chip_size
        y2 = y1 + chip_size
        assert (x2 <= hue_page_image_width - chip_gap // 2), "x2 out of range"
        assert (y2 <= hue_page_image_height - chip_gap // 2), "y2 out of range"

        r = row['r']
        g = row['g']
        b = row['b']
        color_key = row['color_key']
        page_hue_rows.append((x1, y1, x2, y2, r, g, b, color_key, chroma_column, value_row))

    return page_hue_rows

def main(output_image_folder, parquet_file):
    
    munsell_df = MunsellDataFrame.from_parquet(parquet_file)
    
    # create the image folder if it doesn't exist
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)
    
    # get the max cols and rows
    global max_cols
    max_cols = munsell_df.max_column('chroma_column')
    global max_rows
    max_rows = munsell_df.max_column('value_row')

    # compute the image size
    global hue_page_image_width
    hue_page_image_width = max_cols//2 * (chip_size + chip_gap) 
    global hue_page_image_height
    hue_page_image_height = max_rows * (chip_size + chip_gap) 

    # render a page_hue image file for each page_hue_name
    page_hue_number = 1
    for page_hue_name in PAGE_HUE_NAMES:
        hue_page_rows = get_page_hue_rows(page_hue_name, munsell_df)

        image = Image.new('RGBA', (hue_page_image_width, hue_page_image_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        # Draw the filled rectangles on the image
        for x1, y1, x2, y2, r, g, b, color_key, chroma_column, value_row in hue_page_rows:
            color = (r,g,b)
            draw.rectangle([x1, y1, x2, y2], fill=color + (255,))  # Set alpha channel to 255 (opaque)

        # Save the image to a PNG file
        image_file_name = f"{page_hue_number:02.1f}-{page_hue_name}.png"
        image_path = os.path.join(output_image_folder, image_file_name)
        image.save(image_path)

        print(f"Saved image for {page_hue_number} {page_hue_name}: {image_path}")
        page_hue_number += 1

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Create a folder of Munsell Hue Pages from a Munsell Parquet file.')
    parser.add_argument('--o', required=True, help='output Hue Pages image folder')
    parser.add_argument('--p', required=True, help='Input Munsell Parquet file')

    args = parser.parse_args()
    
    output_image_folder = args.o
    parquet_file = args.p

    # Check if the parquet_file exists and is readable
    if not os.path.isfile(parquet_file) or not os.access(parquet_file, os.R_OK):
        print(f"Error: The file {parquet_file} does not exist or is not readable.")
        exit(1)

    main(output_image_folder, parquet_file)
    
    print("done")
